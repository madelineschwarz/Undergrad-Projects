
import arcpy
from arcpy import env
from arcpy.sa import*

arcpy.CheckOutExtension("Spatial")

#Specify folder containing data
arcpy.env.workspace = r''
     
# Specify DEM of area with fault scarps
input_DEM = 

#Calculate Slope Map
outSlope = Slope(input_DEM, "DEGREE", 1) 

#specify hillshade sun angle
outHS_Azimuth = 315 
outHS2_Azimuth = 135
#Compute Hillshade layer
outHS = Hillshade(input_DEM, outHS_Azimuth)
outHS2 = Hillshade(input_DEM, outHS2_Azimuth)
#Compute Aspect layer as an integer type

outAspect = Int(Aspect(input_DEM))

#Compute Curvature
#outCurv = Curvature(input_DEM, 1)

#Specify shape and neighboor hood for window algorithm                     
neighborhood = NbrRectangle(3, 3, "CELL")

#Calculate Statistical Variance of Aspect Map
outVar = FocalStatistics(outAspect, neighborhood,"VARIETY","NODATA")

#-----------------------------------------------------------------------------------------
# Reclassify Derivative Raster layers w/ Map Algebra

#define variables
min_slope = outSlope.minimum
max_slope = outSlope.maximum


min_filt_slope = filt_slope.minimum
max_filt_slope = filt_slope.maximum


min_Asp = outAspect.minimum
max_Asp = outAspect.maximum

min_var = outVar.minimum
max_var = outVar.maximum

#Reclassify slope:
#values scaled 1 to 9
Rcl_slope = ((outSlope - min_slope)*254)/(max_slope - min_slope)

Rcl_filt_slope = ((filt_slope - min_filt_slope)*254/(max_filt_slope - min_filt_slope)
                  
Rcl_var = ((outVar - min_var)*254)/(max_var - min_var)
                  
Rcl_asp = ((outAspect - min_Asp)*254)/(max_Asp - min_Asp)

#Reclassify HS 1:
Remap_HS = RemapRange([[0,70,12],[70.00000001,108,11],[108.00000001,134,10],
                      [134.00000001,153,9],[153.00000001,166,8],[166.00000001,175,0],
                      [175.00000001,182,0],[182.00000001,190,0],
                      [190.00000001,210,11],[210.00000001,254,12]])

Doub_hs = Reclassify(outHS,"VALUE", Remap_HS )


#Allow User to Specify Weights
HS_weight = 5  
Slope_Weight = 5
Filt_Slope_Weight = 3                
Aspect_Weight = 1
Var_Weight = -1

#Weight Each layer
HS_Var = (HS_weight*outHS) + (Var_Weight*outVar)
                  
Slope_Var = (Slope_Weight*Rcl_slope) + (Var_Weight*outVar)
                  
Filt_Slope_Var = (Filt_Slope_Weight*Rcl_filt_slope) + (Var_Weight*outVar)
                  
Aspect_Var = (Aspect_Weight*Rcl_asp) + (Var_Weight*outVar)

# Calculate Weighted overlay
WO_spec = HS_Var + Filt_Slope_Var + Aspect_Var
WO_spec.save("WO_1.tif")

# Segmentation using SMS algorithm
out_SMS = "sms_1.tif"                  
arcpy.gp.SegmentMeanShift_sa(WO_spec, out_SMS, "20", "20", "100", "")
out_SMS.save(out_SMS)
                  
# Clustering using ISO Cluster Unsupervised
number_of_classes = 5
out_ISO_spec = "iso_spec1.tif"
arcpy.gp.IsoClusterUnsupervisedClassification_sa(out_SMS, number_of_classes, out_ISO_spec, "20", "10", "")
out_ISO_spec.save(out_ISO_spec)

