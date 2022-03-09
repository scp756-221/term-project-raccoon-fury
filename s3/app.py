"""
SFU CMPT 756
Sample application---playlist service.
"""

# Standard library modules
import logging
import sys
import time

# Installed packages
from flask import Blueprint
from flask import Flask
from flask import request
from flask import Response

from prometheus_flask_exporter import PrometheusMetrics

import requests

import simplejson as json

# The application

app = Flask(__name__)

metrics = PrometheusMetrics(app)
metrics.info('app_info', 'Playlist process')

bp = Blueprint('app', __name__)

db = {
    "name": "http://cmpt756db:30002/api/v1/datastore",
    "endpoint": [
        "read",
        "write",
        "delete",
        "update"
    ]
}


def get_music(headers, music_id):
    payload = {"objtype": "music", "objkey": music_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return response.json()


@bp.route('/', methods=['GET'])
@metrics.do_not_track()
def hello_world():
    return ("If you are reading this in a browser, your service is "
            "operational. Switch to curl/Postman/etc to interact using the "
            "other HTTP verbs.")


@bp.route('/health')
@metrics.do_not_track()
def health():
    return Response("", status=200, mimetype="application/json")


@bp.route('/readiness')
@metrics.do_not_track()
def readiness():
    return Response("", status=200, mimetype="application/json")


@bp.route('/<playlist_id>', methods=['GET'])
def get_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(
            json.dumps({"error": "missing auth"}),
            status=401,
            mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]
    response = requests.get(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/', methods=['POST'])
def create_playlist():
    headers = request.headers
    try:
        content = request.get_json()
        PlaylistName = content['PlaylistName']
        Songs = content['Songs'].strip().split(",")
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    for music_id in Songs:
        response = get_music(headers, music_id)
        if response['Count'] == 0:
            return Response(json.dumps({"error": "get_song failed"}),
                            status=500,
                            mimetype='application/json')

    payload = {"objtype": "playlist", "PlaylistName": PlaylistName, "Songs": Songs}
    url = db['name'] + '/' + db['endpoint'][1]
    response = requests.post(
        url,
        json=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>', methods=['DELETE'])
def delete_playlist(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][2]
    response = requests.delete(
        url,
        params=payload,
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>/add', methods=['POST'])
def add_song(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]

    pl_response_json = get_playlist(playlist_id)
    if pl_response_json['Count'] == 0:
        return Response(json.dumps({"error": "get_playlist failed"}),
                        status=500,
                        mimetype='application/json')

    music_response_json = get_music(headers, music_id)
    if music_response_json['Count'] == 0:
        return Response(json.dumps({"error": "get_song failed"}),
                        status=500,
                        mimetype='application/json')

    current_songs = pl_response_json['Items'][0]['Songs']
    if music_id in current_songs:
        return Response(json.dumps({"error": "music_id exists in playlist"}),
                        status=500,
                        mimetype='application/json')

    current_songs.append(music_id)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"Songs": current_songs},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


@bp.route('/<playlist_id>/delete', methods=['POST'])
def delete_song(playlist_id):
    headers = request.headers
    # check header here
    if 'Authorization' not in headers:
        return Response(json.dumps({"error": "missing auth"}),
                        status=401,
                        mimetype='application/json')
    try:
        content = request.get_json()
        music_id = content['music_id']
    except Exception:
        return json.dumps({"message": "error reading arguments"})

    payload = {"objtype": "playlist", "objkey": playlist_id}
    url = db['name'] + '/' + db['endpoint'][0]

    pl_response_json = get_playlist(playlist_id)
    if pl_response_json['Count'] == 0:
        return Response(json.dumps({"error": "get_playlist failed"}),
                        status=500,
                        mimetype='application/json')

    music_response_json = get_music(headers, music_id)
    if music_response_json['Count'] == 0:
        return Response(json.dumps({"error": "get_song failed"}),
                        status=500,
                        mimetype='application/json')

    current_songs = pl_response_json['Items'][0]['Songs']
    if music_id not in current_songs:
        return Response(json.dumps({"error": "music_id does not exist in playlist"}),
                        status=500,
                        mimetype='application/json')

    current_songs.remove(music_id)
    url = db['name'] + '/' + db['endpoint'][3]
    response = requests.put(
        url,
        params=payload,
        json={"Songs": current_songs},
        headers={'Authorization': headers['Authorization']})
    return (response.json())


# All database calls will have this prefix.  Prometheus metric
# calls will not---they will have route '/metrics'.  This is
# the conventional organization.
app.register_blueprint(bp, url_prefix='/api/v1/playlist/')

if __name__ == '__main__':
    if len(sys.argv) < 2:
        logging.error("Usage: app.py <service-port>")
        sys.exit(-1)

    p = int(sys.argv[1])
    # Do not set debug=True---that will disable the Prometheus metrics
    app.run(host='0.0.0.0', port=p, threaded=True)
