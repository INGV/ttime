#!/usr/bin/env python

import sys
import json
import pprint
import numpy as np
from obspy.taup import TauPyModel

# P,  ok
# S,  ok
# PKP: PKP ok
# PKiKP: PKPdif ok
# Pdiff: Pdif ok
# Sdiff: Sdif ok
# SKSac:
# SKS: SKS ok


def point_to_circle_Circle(**kwargs):
    """
    From Point on Geoide (lat, lon), distance from point and
    set of azimuths, returns new point. Distance in meters

    param lat: (degree)
    param lon: (degree)
    param radius_m: (meters)
    param az_min_deg: (degree)
    param az_max_deg: (degree)
    param inc_deg: (degree)
    type lat: float
    type lon: float
    type radius_m: float
    type az_min_deg: integer
    type az_max_deg: integer
    type inc_deg: integer
    """

    lat              = float(kwargs.get('latitude', None))
    lon              = float(kwargs.get('longitude', None))
    radius           = float(kwargs.get('radius', None))
    az_min_deg       = int(kwargs.get('azimuth_min', None))
    az_max_deg       = int(kwargs.get('azimuth_max', None))
    inc_deg          = int(kwargs.get('increment_deg', None))

    # check on min max
    if(az_min_deg<0):
       az_min_deg=0
    if(az_max_deg > 360):
       az_max_deg=360

    geod             = pyproj.Geod(ellps='WGS84')

    points           = list(range(az_min_deg, az_max_deg, inc_deg))

    matrix           = [[0]*2 for i in range(len(points))]

    for i in range(len(points)):
        endLon,endLat,backAzimuth = geod.fwd(lon, lat, points[i], radius*1000, radians=False)
        matrix[i][0] = endLon
        matrix[i][1] = endLat

    return matrix


def get_times(**kwargs):

    phase  = kwargs.get('phases', None)
    depth  = kwargs.get('depth', None)
    degre  = kwargs.get('degre', None)
    model  = kwargs.get('model', None)

    times  = []

    for i in range(len(degre)):
        arrivals = model.get_travel_times(source_depth_in_km=depth, distance_in_degree=degre[i], phase_list=phase)
        if(len(arrivals) > 0):
            times.append(np.around((arrivals[0].time),1))
        else:
            times.append(-1)

    tdict = dict()
    tdict[depth] = times

    return times

taup_dict = dict()
temp_dist = dict()

model     = TauPyModel(model="iasp91")
phases    = ['P', 'S']
degree    = np.around(np.arange(1, 180.1, 0.1),1).tolist()
depths    = np.arange(1, 30, 2).tolist() +  np.arange(30, 50, 5).tolist() + np.arange(50, 200, 10).tolist() + \
            np.arange(200, 400, 20).tolist() + np.arange(400, 700, 50).tolist()

taup_dict['distances_degree']        = degree
taup_dict['data']                    = dict()
taup_dict['data']['phase_name']      = 'SKSac'


for i in range(len(depths)):
    print(i, depths[i])
    times = get_times(phase=["SKSac"], depth=depths[i], degre=degree, model=model)
    temp_dist[depths[i]] = times
    #if i == 1:
    #    break
taup_dict['data']['depth_times']       = temp_dist
json_object = json.dumps(taup_dict)

with open("ttimes_SKSac.json", "w") as outfile:
    outfile.write(json_object)
#print(json.dumps(taup_dict, indent=4))
