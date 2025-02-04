import json
import logging
import os
from flask import Flask, jsonify, request, send_from_directory, abort, make_response
from flask_cors import CORS
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional

import py_caldera
import dcloud

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')

# Allow all origins and credentials
CORS(app, supports_credentials=True)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

debug = os.environ.get('DEBUG')


class Adversary(BaseModel):
    adversary_id: str


class OperationRequest(BaseModel):
    name: str
    adversary: Adversary
    group: Optional[str] = ''
    auto_close: Optional[str] = 'true'


@app.route('/api/courses/', methods=['GET', 'HEAD', 'POST'])
def caldera_courses():
    if request.method == 'GET':
        with open('./resources/caldera_courses.json') as course_reader:
            course_string = course_reader.read()
            courses = json.loads(course_string)
        return jsonify(courses), 200


@app.route('/api/caldera/<operation>/', methods=['GET', 'HEAD', 'POST'])
def caldera_api(operation: str):
    if request.method == 'GET':
        response = py_caldera.rest_get(operation, **request.args.to_dict())
        return jsonify(response.json()), response.status_code
    if request.method == 'HEAD':
        response = py_caldera.rest_head(operation, **request.args.to_dict())
        return jsonify(response.json()), response.status_code
    if request.method == 'POST':
        response = py_caldera.rest_post(operation, request.get_json(), **request.args.to_dict())
        return jsonify(response.json()), response.status_code


@app.route('/api/caldera/<operation>/<operation_id>/', methods=['GET', 'PATCH', 'PUT', 'DELETE'])
def caldera_api_id(operation: str, operation_id: str):
    if request.method == 'GET':
        response = py_caldera.rest_get(f'{operation}/{operation_id}', **request.args.to_dict())
        return jsonify(response.json()), response.status_code
    if request.method == 'PUT':
        response = py_caldera.rest_post(f'{operation}/{operation_id}', request.get_json(), **request.args.to_dict())
        return jsonify(response.json()), response.status_code
    if request.method == 'DELETE':
        response = py_caldera.rest_get(f'{operation}/{operation_id}', **request.args.to_dict())
        return jsonify({'response': response.text}), response.status_code


@app.route('/api/caldera/operations/<operation_id>/report/', methods=['GET'])
def caldera_operation_report(operation_id: str):
    response = py_caldera.get_operation_report(operation_id)
    return jsonify(response.json()), 200


@app.route('/api/dcloud/generate-token/', methods=['GET'])
def generate_token():
    user_email = request.args.get('email')
    if not user_email:
        return jsonify({"error": "Email parameter is required"}), 400

    token = request.args.get('token') or dcloud.get_oauth2_token()
    if not token:
        return jsonify({"error": "Unable to obtain OAuth2 token"}), 500

    preferred_data_center = request.cookies.get('preferred_data_center')
    if not preferred_data_center:
        preferred_data_center, error_response, status_code = dcloud.fetch_preferred_data_center(user_email, token)
        if error_response:
            return jsonify(error_response), status_code

    response = make_response(jsonify({"access_token": token, "preferred_data_center": preferred_data_center}))
    response.set_cookie('access_token', token)
    response.set_cookie('user_email', user_email)
    response.set_cookie('preferred_data_center', preferred_data_center)
    return response


@app.route('/api/dcloud/session/', methods=['GET', 'HEAD', 'POST'])
def dcloud_caldera_sessions():
    if request.method == 'GET':
        with open('./resources/dcloud_sessions.json') as session_reader:
            session_string = session_reader.read()
            session = json.loads(session_string)
        return jsonify(session), 200


@app.route('/api/dcloud/<path:subpath>/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def dcloud_view(subpath):
    response = dcloud.prepare_dcloud_request(request, subpath)
    return jsonify(response.json()), response.status_code


@app.route('/', methods=['GET'])
def serve_static_files():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=debug)