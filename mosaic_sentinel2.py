from sentinelsat import SentinelAPI
import geopandas as gpd
from datetime import date, datetime
import folium
from shapely.geometry import MultiPolygon, Polygon
import rasterio
import rasterio.features
import rasterio.warp

import os, sys
import os.path

FOLDER_DATA = "/home/josep/SIGTE/PROJECTES/Compartim_copernicus/projecte_Sentinel2/data"
FOLDER_RGB = "/home/josep/SIGTE/PROJECTES/Compartim_copernicus/projecte_Sentinel2/rgb"
OUTPUT_FOLDER = "/home/josep/SIGTE/PROJECTES/Compartim_copernicus/projecte_Sentinel2/data/"
filelist=os.listdir(FOLDER_RGB)
dirs = os.listdir(FOLDER_DATA)

user = {user}
password = {password}
api = SentinelAPI(user, password, 'https://scihub.copernicus.eu/dhus')


# get geometry of the study area
studyArea = gpd.read_file('shp/girones.shp')
footprint = None
for i in studyArea['geometry']:
    footprint = i

# query to api hub
products = api.query(footprint,
                     date=(date(2019, 11, 20), date(2019, 11, 29)),
                     platformname='Sentinel-2',
                     cloudcoverpercentage=(0, 30))


#api.download_all(products)

for folders in dirs:
    filename = os.listdir(FOLDER_DATA+'/'+folders+'/GRANULE/')
    R10 = 'data/'+folders+'/GRANULE/'+str(filename[0])+'/IMG_DATA/R10m'

    # Open Bands 4, 3 and 2 with Rasterio
    bandnames = os.listdir(FOLDER_DATA+'/'+folders+'/GRANULE/'+filename[0]+'/IMG_DATA/R10m')
    bandnames_part1 = str(bandnames[0].split('_')[0])
    bandnames_part2 = str(bandnames[0].split('_')[1])

    b4 = rasterio.open(R10+'/'+bandnames_part1+'_'+bandnames_part2+'_B04_10m.jp2')
    b3 = rasterio.open(R10+'/'+bandnames_part1+'_'+bandnames_part2+'_B03_10m.jp2')
    b2 = rasterio.open(R10+'/'+bandnames_part1+'_'+bandnames_part2+'_B02_10m.jp2')

    # Create an RGB image
    with rasterio.open(filename[0]+'.tiff','w',driver='Gtiff', width=b4.width, height=b4.height, count=3,crs=b4.crs,transform=b4.transform, dtype=b4.dtypes[0]) as rgb:
        rgb.write(b2.read(1),1)
        rgb.write(b3.read(1),2)
        rgb.write(b4.read(1),3)
        rgb.close()
