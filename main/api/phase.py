import numpy as np
import pyproj
from obspy.geodetics import degrees2kilometers
from geojson import Polygon
import json

class Phase(object):

    def __init__(self, phases_data, lat, lon, depth, time, phases, azimuth_interval):
        self.phases_data = phases_data
        self.lat = float(lat)
        self.lon = float(lon)
        self.depth = float(depth)
        self.time = int(time)
        self.phases = phases
        self.azimuth_interval = float(azimuth_interval)

    def __keys_to_nparray(self, **kwargs):
        keys = kwargs.get('keys', None)

        depths = list(keys)
        depths = [float(x) for x in depths]
        depths = np.array(depths)

        return depths

    def __find_nearest2(self, array, values):
        indices = np.abs(np.subtract.outer(array, values)).argmin(0)
        return indices

    def __point_to_Circle(self, **kwargs):
        """
        From Point on Geoide (lat, lon), distance from point and
        set of azimuths, returns new point. Distance in meters
        """

        delta = kwargs.get('radius_deg', None)
        #depth = kwargs.get('depth', None)

        geod = pyproj.Geod(ellps='WGS84')

        points = list(np.arange(0, 360, self.azimuth_interval))

        matrix = [[0] * 2 for i in range(len(points) + 1)]

        radius = degrees2kilometers(delta) * 1000  # [radius in m]

        for i in range(len(points)):
            endLon, endLat, backAzimuth = geod.fwd(self.lon, self.lat, points[i], radius, radians=False)
            matrix[i][0] = endLon
            matrix[i][1] = endLat
            # print("%7.2f %7.2f" % (endLat, endLon))

        matrix[len(points)][0] = matrix[0][0]
        matrix[len(points)][1] = matrix[0][1]

        matrix.reverse()

        return matrix

    def __make_geojson(self, **kwargs):

        polygon = kwargs.get('polygon', None)

        a = Polygon(([polygon]))

        geometries = {
            "type": "Feature",
            "geometry": a,
            "properties": {
                "phase_name": self.phases,
                "file_name": f"ttimes_{self.phases}.json"
            }
        }

        # p = Polygon(([polygon]))
        # s = Polygon(([polygon]))
        # f1 = {
        #     "type": "Feature",
        #     "geometry": p,
        #      "properties": {
        #          "phase_name": 'P',
        #          "file_name": f"ttimes_{self.phases}.json"
        #      }
        #  }
        #
        # f2 = {
        #     "type": "Feature",
        #     "geometry": s,
        #      "properties": {
        #          "phase_name": 'S',
        #          "file_name": f"ttimes_{self.phases}.json"
        #      }
        #  }
        #
        #
        # geometries = {
        #     "type": "FeatureCollection",
        #      "features": [f1, f2]
        #  }

        return geometries

    # DEPRECATED
    def get_geojson_DEPRECATED(self):
        depths = self.__keys_to_nparray(keys=self.phases_data[self.phases]['data']['times'].keys())
        degree = np.array(self.phases_data[self.phases]['distances_degree'])

        # Cerco la profondita che piu si avvicina a me
        depth_idx = self.__find_nearest2(depths, float(self.depth))
        depth_val = str(int(depths[depth_idx]))

        # Seleziono i tempi della profondita e cerco l'indice di quello piu vicino a me
        times_vals = self.phases_data[self.phases]['data']['times'][depth_val]
        time_idx = self.__find_nearest2(times_vals, float(self.time))

        # Check of -1 values in times:
        phase_exists = True
        if (times_vals[time_idx - 1] == -1 or times_vals[time_idx + 1]):
            if (abs(float(self.time) - times_vals[time_idx]) >= 0.5):
                return None,  f"No phase {self.phases}"

        # Uso quell'indice per pescare la distanza dal vettore distanze
        distance_deg = degree[time_idx]
        # print(distance_deg)

        # Build circle
        circle = self.__point_to_Circle(radius_deg=distance_deg)

        # Build geojson
        geojson = self.__make_geojson(polygon=circle)


        return geojson, None


    '''
        ROBA NUOVA
    '''
    def __get_circle(self, phase):
        #errore se phase PKP(vedere se dipende da software originale o da modifiche)
        depths = self.__keys_to_nparray(keys=self.phases_data[phase]['data']['times'].keys())
        degree = np.array(self.phases_data[phase]['distances_degree'])

        # Cerco la profondita che piu si avvicina a me
        depth_idx = self.__find_nearest2(depths, float(self.depth))
        depth_val = str(int(depths[depth_idx]))

        # Seleziono i tempi della profondita e cerco l'indice di quello piu vicino a me
        times_vals = self.phases_data[phase]['data']['times'][depth_val]
        time_idx = self.__find_nearest2(times_vals, float(self.time))

        # Check of -1 values in times:
        phase_exists = True
        if (times_vals[time_idx - 1] == -1 or times_vals[time_idx + 1]):
            if (abs(float(self.time) - times_vals[time_idx]) >= 0.5):
                return None,  f"No phase {phase}"

        # Uso quell'indice per pescare la distanza dal vettore distanze
        distance_deg = degree[time_idx]
        # print(distance_deg)

        # Build circle
        circle = self.__point_to_Circle(radius_deg=distance_deg)

        return circle, None

    def get_geojson(self):
        errors = []
        # if self.phases:
        #     phases = [self.phases]
        # else:
        #     phases = ['P', 'S']

        geometries = {
            "type": "FeatureCollection",
             "features": []
        }

        for phase in self.phases:
            circle, errorMessage = self.__get_circle(phase)

            if errorMessage:
                errors.append(errorMessage)
                continue

            #self.phases = phases
            #polygon = circle.get('polygon', None)

            a = Polygon(([circle]))
            feature = {
                "type": "Feature",
                "geometry": a,
                 "properties": {
                     "phase_name": phase,
                     "file_name": f"ttimes_{phase}.json"
                 }
            }

            geometries['features'].append(feature)

        return geometries, '; '.join(errors)


