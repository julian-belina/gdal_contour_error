# import os
# import pathlib

# import numpy as np
# import pandas as pd
# from osgeo import gdal, osr
# from osgeo.gdal import Driver
# from osgeo.ogr import Feature, FieldDefn, Layer, OFTInteger, wkbPolygon


# def test_Extent_contoursFromRaster():
#     ###
#     contourEdges = [1, 2, 3]
#     # Open raster file
#     path_to_raster_file = pathlib.Path(__file__).parent.joinpath(
#         "urban_land_cover_aachenClipped.tif"
#     )
#     ds = gdal.Open(str(path_to_raster_file), 0)
#     assert isinstance(ds, gdal.Dataset)
#     band = ds.GetRasterBand(1)

#     # Set spatial reference system
#     rasterSRS = osr.SpatialReference()
#     _val = rasterSRS.SetFromUserInput(ds.GetProjectionRef())
#     assert _val == 0

#     # Create layer
#     driver: Driver = gdal.GetDriverByName("Memory")
#     source: gdal.Dataset = driver.Create("", 0, 0, 0, gdal.GDT_Unknown)
#     layer: Layer = source.CreateLayer("", rasterSRS, wkbPolygon)
#     field = FieldDefn("DN", OFTInteger)
#     layer.CreateField(field)

#     # Setup contour function
#     args = []
#     args.append("ID_FIELD=DN")
#     args.append("POLYGONIZE=YES")

#     opt = "FIXED_LEVELS="
#     for edge in contourEdges:
#         opt += str(edge) + ","
#     args.append(opt[:-1])

#     # Determine contours
#     result = gdal.ContourGenerateEx(band, layer, options=args)
#     layer.CommitTransaction()

#     IDs = []
#     geoms = []
#     for ftrid in range(layer.GetFeatureCount()):
#         ftr: Feature = layer.GetFeature(ftrid)
#         geom = ftr.GetGeometryRef()
#         value = ftr.GetField(0)
#         for gi in range(geom.GetGeometryCount()):
#             geoms.append(geom.GetGeometryRef(gi).Clone())
#             IDs.append(value)

#     countour_data_frame = pd.DataFrame(dict(geom=geoms, ID=IDs))

#     ##

#     # assert countour_data_frame.iloc[0].geom.GetSpatialReference().IsSame(ext.srs)
#     try:
#         assert len(countour_data_frame) == 326
#     except AssertionError:
#         raise (
#             AssertionError(
#                 " The length of the data frame was "
#                 + str(len(countour_data_frame))
#                 + " even though 324 was expected"
#             )
#         )
#     try:
#         assert np.isclose(countour_data_frame.iloc[63].geom.Area(), 285000.2699996233)
#     except AssertionError:
#         raise (
#             AssertionError(
#                 " The area was"
#                 + str(countour_data_frame.iloc[63].geom.Area())
#                 + " even though 285000.2699996233 was expected"
#             )
#         )
#     try:
#         assert countour_data_frame.iloc[63].ID == 1
#     except AssertionError:
#         raise (
#             AssertionError(
#                 " The index was"
#                 + str(countour_data_frame.iloc[63].geom.Area())
#                 + " even though 285000.2699996233 was expected"
#             )
#         )


# if __name__ == "__main__":
#     test_Extent_contoursFromRaster()
