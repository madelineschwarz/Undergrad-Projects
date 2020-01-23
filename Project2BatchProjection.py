#Madeline Schwarz
#1/22/2020

#Reprojects feature classes in a desired folder to the spatial reference of another specified fc (similar to Batch Projection Tool)

import arcpy
from arcpy import env

inFolder = arcpy.GetParameterAsText(0)                                              #allows user to define input folder
target_projection_data = arcpy.GetParameterAsText(1)                                #define fc with desired spatial reference
arcpy.env.workspace = inFolder #defines env to desired user folder

out_coordinate_system = arcpy.Describe(target_projection_data).spatialReference     #sets output coordinate system as desired shapefile's

featureClassList = arcpy.ListFeatureClasses() #creates a list of feature classes in input folder
try:
    for input_features in featureClassList:
        in_coord = arcpy.Describe(input_features).spatialReference                  #describes original SR of feature class and sets as a variable
        if in_coord.Name != out_coordinate_system.Name:                             #if fc's SR doesn't match target fc.....
            input_featuresName = input_features.replace(".shp","")                  #remove .shp from fc's original name
            output_feature_class = inFolder + "\\" + input_featuresName + "_projected2.shp"             #defines path and new name of reprojected fc
            arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)       #execute project tool
            arcpy.AddMessage("Successfully Reprojected: " + output_feature_class)                       #print message in arcpy
            print ("Successfully Reprojected: " + output_feature_class)
        else:
            arcpy.AddMessage("skipped this feature class; already in proper SR: " + input_features)     #if fc already in desired SR, print message
            print("skipped this feature class; already in proper SR: " + input_features)
except:
 arcpy.AddError("Projection Failed")
 print ("Projection Failed")
 print (arcpy.GetMessages())
 
#Notes: Successfully reprojects data into desired spatiral reference
        #Repeats message for each feature class in "inFolder"
