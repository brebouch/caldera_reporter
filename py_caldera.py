###################
#
# Python Caldera Client
#
#
#
######################
import json
import os

import dotenv
import requests
from json2html import *

dotenv.load_dotenv()

base_url = 'http://198.18.128.193:8888/api/v2'

waiting_responses = []


STATUS_CODES = {
    0: 'Success',
    1: 'Fail',
    124: 'Timeout'
}


def get_header():
    return {
        'KEY': os.environ.get('API_TOKEN'),
        'Content-Type': 'application/json',
        'Acccept': 'application/json'
    }


def rest_get(endpoint, **kwargs):
    url = f'{base_url}/{endpoint}'
    response = requests.get(url, headers=get_header(), verify=False)
    if response.status_code == 200:
        return response.json()


def rest_delete(endpoint, **kwargs):
    url = f'{base_url}/{endpoint}'
    response = requests.delete(url, headers=get_header(), verify=False)
    if response.status_code == 200:
        return response.json()


def rest_post(endpoint, data, **kwargs):
    url = f'{base_url}/{endpoint}'
    if not isinstance(data, dict):
        data = {}
    response = requests.post(url, json=data, headers=get_header(), verify=False)
    if response.status_code == 200:
        return response.json()


def rest_put(endpoint, data, **kwargs):
    url = f'{base_url}/{endpoint}'
    if not isinstance(data, dict):
        data = {}
    response = requests.put(url, json=data, headers=get_header(), verify=False)
    if response.status_code == 200:
        return response.json()


def run_operation(name, adversary_id, group='', auto_close='true'):
    operation = {
        'name': name,
        'adversary': {
            'adversary_id': adversary_id
        },
        'group': group,
        'auto_close': auto_close
    }
    op = rest_post('operations', operation)
    if op:
        waiting_responses.append(op)


def get_operation_report(operation_id, enable_agent_output=False):
    data = {
        'enable_agent_output': enable_agent_output
    }
    return rest_post(f'operations/{operation_id}/report', data=data)


def get_operation_list():
    return rest_get(f'operations')


def get_steps_key(report_json):
    if 'steps' in report_json.keys():
        if isinstance(report_json['steps'], dict):
            return report_json['steps'].keys()


def normalize_report_json(report_json):
    agents = get_steps_key(report_json)
    result = {}
    success = 0
    failed = 0
    for a in agents:
        for s in report_json['steps'][a]['steps']:
            if a not in result.keys():
                result.update({a: []})
            if s['status'] == 0:
                success += 1
            else:
                failed += 1

            result[a].append({
                'Status': STATUS_CODES[s['status']],
                'Task': s['name'],
                'Description': s['description']
            })
    if failed == 0:
        successful = 100
    else:
        successful = float(success / failed)
    return result, successful


def generate_report_html(report_json, run_type):
    cleaned_steps, successful = normalize_report_json(report_json)
    output = (f'<html><head><link rel="stylesheet" href="index.css"></head>'
              f'<body><h2>Operation Name: {report_json["name"]}</h2>')
    output += f'<h4>Start Time: {report_json["start"]}</h4>'
    output += f'<h4>End Time: {report_json["finish"]}</h4>'
    output += f'<h4>Percent Success: {successful}%</h4>'
    for c in cleaned_steps.values():
        output += json2html.convert(json=c, table_attributes="id=\"test-results\" "
                                                             "colgroup_attributes=style=\"max-width: 50%;\"")
        output += '<br>'
    output += '</body></html>'
    report_path = f'{os.getcwd()}/static/{run_type}.html'
    with open(report_path, 'w') as report_writer:
        report_writer.write(output)


def check_operation_run(operation_id, run_type):
    checkup = rest_get(f'operations/{operation_id}')
    if checkup:
        if checkup['state'] != 'running':
            response_index = 0
            for i in range(len(waiting_responses)):
                if waiting_responses[i]['id'] == operation_id:
                    response_index = i
                    break
            if response_index:
                del waiting_responses[response_index]
            if checkup['state'] == 'finished':
                # Add reference to completed operation but not in error state
                report = get_operation_report(operation_id, True)
                generate_report_html(report, run_type)
    return checkup


if __name__ == '__main__':
    check_operation_run('14860721-76f7-44d9-a86d-5be71f9c6071')
    run_operation('TestOp1', '89d971f4-fab8-4c15-bc8f-d64b26728c81')
