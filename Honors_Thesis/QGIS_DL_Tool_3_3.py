import os, sys, math, string, random,tempfile
import processing as st
import networkx as nx

#Author: Maddie Schwarz
# This script is dependent on the Geometric Attributes Plugin by Dr. Bjorn Nyberg
#github link: https://github.com/BjornNyberg/Geometric-Attributes-Toolbox/tree/master/geometric_attributes


#Enter Path to DEM raster
rlayer = QgsRasterLayer(r'')

#Enter path to drawn polyline
layer = QgsVectorLayer(r'')

#Enter the desired spacing for transects
tran_dist = 10 #means code will create transects along polyline that are 5 meters apart
tran_width = 40 #means each transect is 50m long

########## NO NEED MODIFY CODE BELOW: ##########################################################

#Create points along input polyling
pt_params = {'INPUT':layer, 'DISTANCE':1,'START_OFFSET':0, 'END_OFFSET':0, 'OUTPUT':'memory:'}
poly_pts = st.run("native:pointsalonglines",pt_params,  feedback=None)
layer = poly_pts['OUTPUT']

#Convert points to path
path_params = {'INPUT':layer,'CLOSE_PATH' : False, 'ORDER_FIELD' : 'distance','GROUP_FIELD' : 'ID','DATE_FORMAT':'','OUTPUT':'memory:'}
pts_to_path = st.run("qgis:pointstopath", path_params, feedback=None)
layer = pts_to_path['OUTPUT']

#Generates Transects along path
tran_width_mod = tran_width/2
tran_params = {'Centerlines': layer,'Distance':tran_width_mod,'Samples':tran_dist,'Densify':0,'Output':'memory:'}
run_tran = processing.run("Algorithms:Transects By Distance", tran_params, feedback=None)
layer = run_tran['Output']

#gives each transect an ID value
pv = layer.dataProvider()
pv.addAttributes([QgsField('ID',QVariant.Int)])
layer.updateFields()
expression1 = QgsExpression('$id')
context = QgsExpressionContext()
context.appendScopes(\
QgsExpressionContextUtils.globalProjectLayerScopes(layer))
with edit(layer):
    for f in layer.getFeatures():
        context.setFeature(f)
        f['ID'] = expression1.evaluate(context)
        layer.updateFeature(f)
        

#Generate points along each transect 
pt_params2 = {'INPUT':layer, 'DISTANCE':1,'START_OFFSET':0, 'END_OFFSET':0, 'OUTPUT':'memory:'}
poly_pts2 = st.run("native:pointsalonglines",pt_params2,  feedback=None)
out_pts2 = poly_pts2['OUTPUT']
QgsProject.instance().addMapLayer(out_pts2)

#Generate new transects from points
path_params2 = {'INPUT':out_pts2,'CLOSE_PATH' : False, 'ORDER_FIELD' : 'distance','GROUP_FIELD' : 'ID','DATE_FORMAT':'','OUTPUT':'memory:'}
pts_to_path2 = st.run("qgis:pointstopath", path_params2, feedback=None)
out_paths2 = pts_to_path2['OUTPUT']
QgsProject.instance().addMapLayer(out_paths2)

fs = QgsFields()

for field in out_paths2.fields():
    fs.append(QgsField(field.name(),field.type()))

bands = rlayer.bandCount() #total band count of raster 'rlayer'
print("number of raster bands: " + str(bands))

for n in range(bands):
    fs.append(QgsField('SampVal_'+ str(n+1),6))

#(writer, dest_id) = self.parameterAsSink(parameters,self.Output,context,fs,2,layer.sourceCrs())

rProv = rlayer.dataProvider()
fet = QgsFeature()

for feature in layer.getFeatures(QgsFeatureRequest()):
    
    geom = feature.geometry()

    if geom.isMultipart():
        geomFeat = geom.asMultiPolyline()[0] #first transect
        #print("This transect has " + str(len(geomFeat)) + " points")
    else:
        geomFeat = geom.asPolyline()
        #print("geom is singlepart")

    rows = [] 
    
    #for field in layer.fields():
        #rows.append(feature[field.name()])
        #print(rows)
        
    for i in range(len(geomFeat)): #for each point in the n transect
        gend = geomFeat[i] #gend equals each QgsPointXY
        #print(gend[0], gend[1])
        for n in range(bands): # sample raster from each QgsPOintXY
            val,res = rProv.sample(QgsPointXY(gend[0], gend[1]), n+1)
            #print(val)
            rows.append(val) #adds sampled raster value to list 'rows'
            
    current_max = sys.float_info.min
    for item in rows:
        current_max = max(current_max,item)
    #print(current_max)
    
    current_min = sys.float_info.max
    for item in rows:
        current_min = min(current_min,item)
    #print(current_min)
    
    displacement = current_max-current_min
    displ_list = []
    displ_list.append(displacement)
    print(displ_list[0])

    fet.setGeometry(geom)
    fet.setAttributes(displ_list)
    #writer.addFeature(fet,QgsFeatureSink.FastInsert)
