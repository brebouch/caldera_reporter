import logging
import os
from flask import Flask, jsonify, request, send_from_directory, abort
from flask_cors import CORS
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
from typing import Optional

import py_caldera

load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

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


@app.route('/api/operation/<operation_id>', methods=['GET'])
def caldera_operation(operation_id: str):
    run_type = request.args.get('run_type')
    response = py_caldera.check_operation_run(operation_id, run_type)
    return jsonify(response), 200


@app.route('/api/operation', methods=['POST', 'GET'])
def operation():
    if request.method == 'POST':
        try:
            operation_data = request.json
            op = OperationRequest(**operation_data)
        except ValidationError as e:
            return jsonify(e.errors()), 400

        name = op.name
        adversary_id = op.adversary.adversary_id
        response = py_caldera.run_operation(name, adversary_id)
        return jsonify(response), 200
    if request.method == 'GET':
        response = py_caldera.get_operation_list()
        return jsonify(response), 200


@app.route('/api/reset', methods=['GET'])
def reset_app():
    try:
        cwd = os.getcwd()
        files = os.listdir(f'{cwd}/static/')
        if 'initial_test.html' in files:
            os.remove(f'{cwd}/static/initial_test.html')
        if 'final_test.html' in files:
            os.remove(f'{cwd}/static/final_test.html')
        return jsonify({
            'action': 'rest',
            'status': 'success'
        }), 200
    except ValidationError as e:
        return jsonify({
            'action': 'rest',
            'status': 'fail',
            'error': str(e)
        }), 400


@app.route('/', methods=['GET'])
def serve_static_files():
    try:
        return send_from_directory(app.static_folder, 'index.html')
    except FileNotFoundError:
        abort(404)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=debug)