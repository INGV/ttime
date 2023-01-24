#!/usr/bin/env python

import os
import sys
import json
import pyproj  # pip install pyproj
import argparse
import configparser
import numpy as np
from geojson import Polygon
#from django.contrib.gis.geos import Polygon, Point, MultiPoint, GeometryCollection

from obspy.geodetics import degrees2kilometers

#import shapely.geometry as sgeom


def parseMyLine():

    Example = "./get_phase_circle.py --lat 35 --lon 10 --azimuth_interval 90 --depth 33 --time 200"

    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,description=Example)

    parser.add_argument('--lat',              default = None, help = 'Latitude. Default: None')
    parser.add_argument('--lon',              default = None, help = 'Longitude. Default: None')
    parser.add_argument('--cfg',              default = None, help = 'Configuration file. Default: None')
    parser.add_argument('--depth',            default = None, help = 'Depth [km]. Default: None')
    parser.add_argument('--time',             default = None, help = 'Time interval in seconds. Default: None')
    parser.add_argument('--phases',            default = None, help = 'Phane name [P, S]. Default: None')
    parser.add_argument('--azimuth_interval', default = None, help = 'Azimuth interval to compute new poit along the circle. Default: None')

    args=parser.parse_args()

    return args

def point_to_Circle(**kwargs):
    """
    From Point on Geoide (lat, lon), distance from point and
    set of azimuths, returns new point. Distance in meters
    """

    lat      = kwargs.get('lat', None)
    lon      = kwargs.get('lon', None)
    delta    = kwargs.get('radius_deg', None)
    depth    = kwargs.get('depth', None)
    inc_deg  = kwargs.get('increment_deg', None)

    geod   = pyproj.Geod(ellps='WGS84')

    points = list(np.arange(0, 360, float(inc_deg)))

    matrix = [[0]*2 for i in range(len(points)+1)]

    radius = degrees2kilometers(delta)*1000  #[radius in m]

    for i in range(len(points)):
        endLon,endLat,backAzimuth = geod.fwd(lon, lat, points[i], radius, radians=False)
        matrix[i][0] = endLon
        matrix[i][1] = endLat
        #print("%7.2f %7.2f" % (endLat, endLon))

    matrix[i+1][0] = matrix[0][0]
    matrix[i+1][1] = matrix[0][1]

    matrix.reverse()

    return matrix

def load_data(**kwargs):

    file = kwargs.get('json_file', None)
    f = open(file)
    data = json.load(f)

    return data

def keys_to_nparray(**kwargs):

    keys = kwargs.get('keys', None)

    depths = list(keys)
    depths = [float(x) for x in depths]
    depths = np.array(depths)

    return depths

def find_nearest2(array, values):
    indices = np.abs(np.subtract.outer(array, values)).argmin(0)
    return indices

def make_geojson(**kwargs):

    polygon    = kwargs.get('polygon', None)
    phase_file = kwargs.get('phase_file', None)

    a = Polygon(([polygon]))

    phase = phase_file.split('_')[-1].split('.')[0]

    geometries = {
      "type": "Feature",
      "geometry": a,
      "properties": {
        "phase_name": phase,
        "file_name": phase_file
      }}

    return json.dumps(geometries)

def get_phase_file(**kwargs):

    cfg  = kwargs.get('cfg', None)
    args = kwargs.get('args', None)

    if(args.phase == 'P'):
        file_name = cfg['PATHS']['jsn'] + os.sep + cfg['FILES']['P']

    if(args.phase == 'S'):
        file_name = cfg['PATHS']['jsn'] + os.sep + cfg['FILES']['S']

    return file_name

#######################################################################
# Begin
#######################################################################


args=parseMyLine()
nrArguments = sys.argv[1:]
if not nrArguments:
       print ("Use -h or --help option for Help")
       sys.exit(0)

# ---- Load and Read Configuration File and keys ---------------------- #
ConfigFile = args.cfg
Config=configparser.RawConfigParser()
Config.read(ConfigFile)

if(args.azimuth_interval == None):
    args.azimuth_interval = Config['PARAMETERS']['azimuth_interval']


phase_file = get_phase_file(cfg=Config, args=args) #'ttimes_P.json')

# Leggo json con phasi e diestanze
data   = load_data(json_file=phase_file)
depths = keys_to_nparray(keys=data['data']['times'].keys())
degree = np.array(data['distances_degree'])

# Cerco la profondita che piu si avvicina a me
depth_idx  = find_nearest2(depths, float(args.depth))
depth_val  = str(int(depths[depth_idx]))

# Seleziono i tempi della profondita e cerco l'indice di quello piu vicino a me
times_vals = data['data']['times'][depth_val]
time_idx   = find_nearest2(times_vals, float(args.time))

# Check of -1 values in times:
phase_exists = True
if(times_vals[time_idx-1] == -1 or times_vals[time_idx+1]):
    if( abs(float(args.time) - times_vals[time_idx]) >= 0.5):
        print("No phases" + args.phase)
        sys.exit()

# Uso quell'indice per pescare la distanza dal vettore distanze
distance_deg = degree[time_idx]
#print(distance_deg)

# Build circle
circle = point_to_Circle(lat=args.lat, lon=args.lon, radius_deg=distance_deg, increment_deg=args.azimuth_interval)

# Build geojson
geojson= make_geojson(polygon=circle, phase_file=phase_file)
print(geojson)
