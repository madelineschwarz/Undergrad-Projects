import arcpy
from arcpy import env
#Run in ArcGIS python window using execfile(r'file location')

inFolder = "D:\NLSdataV7\TIFF Files" #
arcpy.CheckOutExtension("3D")
arcpy.env.workspace = inFolder

RasterList = arcpy.ListRasters("*", "TIF")

for rasters in RasterList:
    inRaster = arcpy.Describe(rasters).baseName
    inRasterName = inRaster.replace("IslandsDEMv0_2x2m_zmasl_isn2016_","")
    #z_factor = 1
    Output_curvature_raster = inFolder + "\\" + "tile" + inRasterName + "curv"
    Output_profile_curve_raster = inFolder + "\\" + "tile" + inRasterName + "prof"
    Output_plan_curve_raster = inFolder + "\\" + "tile" + inRasterName + "plan"
    arcpy.Curvature_3d(rasters, Output_curvature_raster, "1", Output_profile_curve_raster, Output_plan_curve_raster)