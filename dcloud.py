import os
import requests
from flask import jsonify, session


def get_oauth2_token():
    response = requests.post(os.environ.get("DCLOUD_TOKEN_URL"), data={
        "grant_type": os.environ.get("DCLOUD_GRANT_TYPE"),
        "client_id": os.environ.get("DCLOUD_CLIENT_ID"),
        "client_secret": os.environ.get("DCLOUD_CLIENT_SECRET")
    })
    response_data = response.json()
    return response_data.get("access_token")


def get_user_id(email, token):
    search_url = f"https://dcloud2-rtp.cisco.com/api/users/search?name={email}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        search_data = response.json()
        if search_data.get("success") and search_data.get("users"):
            return search_data["users"][0]["userId"]
    return None


def get_user_preference(user_id, token):
    user_url = f"https://dcloud2-rtp.cisco.com/api/users/{user_id}"
    headers = {
        'Authorization': f'Bearer {token}',
        'Accept': 'application/json'
    }
    response = requests.get(user_url, headers=headers)
    if response.status_code == 200:
        user_data = response.json()
        return user_data.get("preferences", {}).get("demoTheatre", "rtp")
    return "rtp"


def fetch_preferred_data_center(user_email, token):
    user_id = get_user_id(user_email, token)
    if not user_id:
        return None, {"error": "Unable to find user ID"}, 404

    preferred_data_center = get_user_preference(user_id, token)
    return preferred_data_center, None, 200


def prepare_dcloud_request(request, subpath):
    token = request.cookies.get('access_token') or get_oauth2_token()
    if not token:
        return None, {"error": "Unable to obtain OAuth2 token"}, 500

    user_email = request.cookies.get('user_email')
    if not user_email:
        return None, {"error": "Email is missing in the request"}, 400

    preferred_data_center = request.cookies.get('preferred_data_center')
    if not preferred_data_center:
        if 'preferred_data_center' in session:
            preferred_data_center = session['preferred_data_center']
        else:
            if not preferred_data_center:
                preferred_data_center, error_response, status_code = fetch_preferred_data_center(user_email, token)
                if error_response:
                    return None, error_response, status_code
            session['preferred_data_center'] = preferred_data_center

    data_center_url = {
        'sjc': 'https://dcloud2-sjc.cisco.com',
        'syd': 'https://dcloud2-syd.cisco.com',
        'lon': 'https://dcloud2-lon.cisco.com',
        'sng': 'https://dcloud2-sng.cisco.com',
        'rtp': 'https://dcloud2-rtp.cisco.com'
    }.get(preferred_data_center, 'https://dcloud2-rtp.cisco.com')

    dcloud_api_url = f"{data_center_url}/api/{subpath}"

    headers = {
        'Accept': 'application/json',
        'Authorization': f'Bearer {token}'
    }

    response = requests.request(
        method=request.method,
        url=dcloud_api_url,
        headers=headers,
        data=request.data,
        params=request.args
    )

    return response
