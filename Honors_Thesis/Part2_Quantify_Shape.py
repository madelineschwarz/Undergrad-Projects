import arcpy
from arcpy import env
from arcpy.sa import*


#Reclassify Extracted Values into a Constant Raster layer
arcpy.env.workspace = r""

Ras = Raster("")


# Extract Scarp like values from ISO result
out_ex = ""
SQL_Clause = "VALUE = 2"

extract = ExtractByAttributes(Ras, SQL_Clause)
extract.save(out_ex)

Raster_lyr = Raster("
Poly_lyr =
MBGPoly_lyr =
elong_ras = " "
length_ras = " "
strike_ras = " "
curl_ras = " "
arcpy.RasterToPolygon_conversion(Raster_lyr,
                                 Poly_lyr,
                                 "NO_SIMPLIFY",
                                  "VALUE")

#Calculate Minimum Bounding Geometry of Polygons

arcpy.MinimumBoundingGeometry_management(Poly_lyr, MBGPoly_lyr,"CONVEX_HULL", "NONE", "", "MBG_FIELDS")

#Join the MBG Shapefile with the initial Polygon Layer
arcpy.JoinField_management(Poly_lyr, "Id", MBGPoly_lyr, "Id",["MBG_Width","MBG_Length","MBG_Orient"])
                           
#Add Fields

arcpy.AddField_management(Poly_lyr, "perimeter", "FLOAT", "", "", "")
arcpy.AddField_management(Poly_lyr, "area", "FLOAT", "", "", "")
arcpy.AddField_management(Poly_lyr, "elongation", "FLOAT", "", "", "")
arcpy.AddField_management(Poly_lyr, "curl", "FLOAT", "", "", "")
arcpy.AddField_management(Poly_lyr, "fibreL", "FLOAT", "", "", "")
                    
# Fill Fields
arcpy.CalculateField_management(Poly_lyr, "perimeter", "!shape.length@meters!", "PYTHON_9.3", "")
arcpy.CalculateField_management(Poly_lyr, "area", "!shape.area@squaremeters!", "PYTHON_9.3", "")
arcpy.CalculateField_management(Poly_lyr, "elongation", "(!area!/(!perimeter!**2))*4*math.pi", "PYTHON_9.3", "")
arcpy.CalculateField_management(Poly_lyr, "fibreL", "(!perimeter!-((!perimeter!**2)-16*!area!)**0.5)/4", "PYTHON_9.3", "")
arcpy.CalculateField_management(Poly_lyr, "curl", "[MBG_Length]/[fibreL]", "VB", "")

#arcpy.CalculateField_management(Poly_lyr, "elongation", "[MBG_Width]/ [MBG_Length]", "VB", "")




#Generate geometric valued rasters
arcpy.PolygonToRaster_conversion(in_features=Poly_lyr, value_field="elongation",
                                 out_rasterdataset=elong_ras,
                                 cell_assignment="MAXIMUM_AREA", priority_field="NONE",cellsize="1")

arcpy.PolygonToRaster_conversion(in_features=Poly_lyr, value_field="MBG_Length",
                                 out_rasterdataset=length_ras,
                                 cell_assignment="MAXIMUM_AREA", priority_field="NONE",
                                 cellsize="1")

arcpy.PolygonToRaster_conversion(in_features=Poly_lyr, value_field="MBG_Orient",
                                 out_rasterdataset=strike_ras,
                                 cell_assignment="MAXIMUM_AREA", priority_field="NONE",
                                 cellsize="1")

arcpy.PolygonToRaster_conversion(in_features=Poly_lyr, value_field="curl",
                                 out_rasterdataset=curl_ras,
                                 cell_assignment="MAXIMUM_AREA", priority_field="NONE",
                                 cellsize="1")
