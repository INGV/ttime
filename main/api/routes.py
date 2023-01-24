import flask_api.status
from main.api import util
from flask import Blueprint, jsonify, render_template
from flask import (
    request,
    Response,
    make_response
)
from flask_api import status as http_status_code
from main import logger
from main.api.queries import Queries
route = Blueprint('webserver', __name__)
from flask_cors import CORS
from datetime import datetime

cors = CORS(route, resources={r"/*": {"origins": "*"}})

queries = Queries()

errors = Blueprint('webservsr_errors', __name__)
@errors.app_errorhandler(Exception)

def handle_unexpected_error(error):
    status_code = 500
    return f"{type(error)}, {str(error)}", status_code

@route.before_request
def before_request_callback():
    path = request.path
    method = request.method
    logger.info(path + " [" + method + "]")

@route.route('/api/test', methods=["GET"])
def test():
    return 'test OK!!'

@route.route('/api/get_phase_circle', methods=["GET"])
def get_phase_circle():
    json_data, status = queries.get_phase_circle(request)
    if status != http_status_code.HTTP_200_OK:
        json_data = util.completeErrorStruct(request, json_data)
    result = (Response(json_data, content_type='application/json'), status)
    return result
