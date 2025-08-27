# Run test for gdal 3.10

## Create Environment for gdal 3.10

conda env create --file=requirements-gdal_3_10.yml
conda activate gdal_test_env_3_10

### Test with python file
python test_gdal_3x3.py
--> Two polygons

### Test with gdal cli
gdal_contour -fl 1 -fl 2 -fl 3 test_raster_3x3.tif test_3_10.json
--> 3 geometries
gdal_contour -fl 1 -fl 2 -fl 3 -p test_raster_3x3.tif test_3_10.geojson
--> 3 geometries

# Run test for gdal 3.11

## Create Environment for gdal 3.11

conda env create --file=requirements-gdal_3_11.yml
conda activate gdal_test_env_3_11

### Test with python file
python test_gdal_3x3.py
--> Only one polygon


### Test with gdal cli
gdal_contour -fl 1 -fl 2 -fl 3 test_raster_3x3.tif test_3_11.json
--> 3 geometries
gdal_contour -fl 1 -fl 2 -fl 3 -p test_raster_3x3.tif test_3_11.geojson
--> 2 geometries