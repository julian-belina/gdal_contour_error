import pathlib

import numpy as np
import pandas as pd
from osgeo import gdal, osr
from osgeo.gdal import Driver
from osgeo.ogr import Feature, FieldDefn, Layer, OFTInteger, wkbPolygon


def test_contours_3x3_example(contourEdges):
    ###
    output_path = pathlib.Path(__file__).parent.joinpath(r"test_raster_3x3.tif")
    output_path_str = str(output_path)

    # Open raster file
    ds = gdal.Open(output_path_str, 0)
    assert isinstance(ds, gdal.Dataset)
    band = ds.GetRasterBand(1)

    # Set spatial reference system
    rasterSRS = osr.SpatialReference()
    _val = rasterSRS.SetFromUserInput(ds.GetProjectionRef())
    assert _val == 0
    # Create layer
    driver: Driver = gdal.GetDriverByName("Memory")
    source: gdal.Dataset = driver.Create("", 0, 0, 0, gdal.GDT_Unknown)
    layer: Layer = source.CreateLayer("", rasterSRS, wkbPolygon)
    field = FieldDefn("DN", OFTInteger)
    layer.CreateField(field)
    # Setup contour function
    args = []
    args.append("ID_FIELD=DN")
    args.append("POLYGONIZE=YES")
    opt = "FIXED_LEVELS="
    for edge in contourEdges:
        opt += str(edge) + ","
    args.append(opt[:-1])
    print("Args: ", args)
    # Determine contours
    result = gdal.ContourGenerateEx(band, layer, options=args)
    layer.CommitTransaction()
    IDs = []
    geoms = []
    for ftrid in range(layer.GetFeatureCount()):
        ftr: Feature = layer.GetFeature(ftrid)
        geom = ftr.GetGeometryRef()
        value = ftr.GetField(0)
        for gi in range(geom.GetGeometryCount()):
            geoms.append(geom.GetGeometryRef(gi).Clone())
            IDs.append(value)
    countour_data_frame = pd.DataFrame(dict(geom=geoms, ID=IDs))

    try:
        assert len(countour_data_frame) == 3
    except AssertionError:
        raise (
            AssertionError(
                " The length of the data frame was "
                + str(len(countour_data_frame))
                + " even though 2 was expected"
            )
        )


if __name__ == "__main__":
    # contourEdges = [
    #     "min",
    #     2,
    #     "max",
    # ]
    # contourEdges = [
    #     "MIN",
    #     2,
    #     "MAX",
    # ]
    contourEdges = [
        1,
        2,
        3,
    ]
    test_contours_3x3_example(contourEdges=contourEdges)
