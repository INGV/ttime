from contextlib import closing
import json
import simplejson
from datetime import date, time, datetime, timedelta
from flask_api import status as http_status_code
from main.api.phase import Phase


class Queries(object):
    @staticmethod
    def dateConverter(o):
        if isinstance(o, (date, datetime)):
            return o.__str__()
        elif isinstance(o, (date, time)):
            return o.__str__()

    #def __init__(self, db, logger=None):
    def __init__(self):
        self.phases_data = {}
        self.all_phases = ['P', 'PKP', 'PKiKP', 'Pdiff', 'S', 'SKS', 'Sdiff']
        for type in self.all_phases:
            with open (f"assets/json/ttimes_{type}.json", 'r') as f:
                self.phases_data[type] = json.load(f)

    def get_phase_circle(self, request):
        args = request.args
        # for key, value in args.items():
        #     print(f'{key}={value}')

        ret_data = {
            "error": None,
            "detail": None,
            "data": None
        }

        try:
            for param in ['lat', 'lon', 'depth', 'time']:
                if not param in args:
                    ret_data['error'] = "MISSING_PARAMETER"
                    ret_data['detail'] = f"Missing parameter [{param}]"
                    return json.dumps(ret_data), http_status_code.HTTP_200_OK

            if not 'phases' in args:
                phases = self.all_phases
            else:
                phases2 = args['phases'].replace(" ","")
                phases = phases2 .split(',')
                #confronto tra due liste
                if not all(elem in self.all_phases for elem in phases):
                    ret_data['error'] = "PARAMETER_VALUE_NOT_VALID"
                    ret_data['detail'] = f"Value of parameter phases must be 'P' or 'S'. Received [{args['phases']}]"
                    return json.dumps(ret_data), http_status_code.HTTP_200_OK
                phases = list(set(phases))
            azimuth_interval = 1
            if 'azimuth_interval' in args:
                azimuth_interval = args['azimuth_interval']

            phase = Phase(
                phases_data = self.phases_data,
                lat = args['lat'],
                lon = args['lon'],
                depth = args['depth'],
                time = args['time'],
                phases = phases,
                azimuth_interval = azimuth_interval
            )

            #data, error = phases.get_geojson()
            data, error = phase.get_geojson()

            if error:
                ret_data['error'] = "GENERIC_ERROR"
                ret_data['detail'] = error

            ret_data['data'] = data
            return simplejson.dumps(ret_data, ignore_nan=True), http_status_code.HTTP_200_OK
            #return json.dumps(ret_data, default=Queries.dateConverter), http_status_code.HTTP_200_OK

        except Exception as e:
            ret_data['error'] = "UNEXPECTED_ERROR"
            ret_data['detail'] = str(e)
            return json.dumps(ret_data), http_status_code.HTTP_200_OK