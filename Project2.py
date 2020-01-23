#Reprojects feature classes in a desired folder to the spatial reference of another specified fc

import arcpy
from arcpy import env

inFolder = arcpy.GetParameterAsText(0) #allows user to define in folder
target_projection_data = arcpy.GetParameterAsText(1)
arcpy.env.workspace = inFolder #defines env to desired user folder

out_coordinate_system = arcpy.Describe(target_projection_data).spatialReference #sets output coor sys as desired shapefile's

featureClassList = arcpy.ListFeatureClasses()
try:
    for input_features in featureClassList:
        in_coord = arcpy.Describe(input_features).spatialReference
        if in_coord.Name != out_coordinate_system.Name:
            input_featuresName = input_features.replace(".shp","")
            output_feature_class = inFolder + "\\" + input_featuresName + "_projected2.shp"
            arcpy.Project_management(input_features, output_feature_class, out_coordinate_system)
            arcpy.AddMessage("Successfully Reprojected: " + output_feature_class)
            print ("Successfully Reprojected: " + output_feature_class)
        else:
            arcpy.AddMessage("skipped this feature class; already in proper SR: " + input_features)
            print("skipped this feature class; already in proper SR: " + input_features)
except:
 arcpy.AddError("Projection Failed")
 print ("Projection Failed")
 print (arcpy.GetMessages())
 
#Notes on program: Successfully reprojects data into desired spatiral reference
#Repeats message for each feature class in "inFolder"