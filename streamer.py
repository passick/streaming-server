from flask import Flask, request, abort
from flask_redis import FlaskRedis

import requests

application = Flask(__name__)
application.config['REDIS_URL'] = "redis://localhost:6379/0"
redis_store = FlaskRedis(application)

dispatch_server_address = "178.62.117.207"

@application.route("/", methods=['GET'])
def index():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    return "This is a streaming server. Nothing interesting here. Your ip: " + ip

@application.route("/check", methods=['POST'])
def check():
    stream_name = request.form.get('name')
    key = request.form.get('key')
    if redis_store.exists(stream_name) and \
          redis_store.get(stream_name).decode('UTF-8') == key:
        r = requests.post('http://' + dispatch_server_address + '/stream_status_changed',
			data={'name': stream_name, 'status': 1})
        return 'ok'
    abort(401)

@application.route("/done", methods=['POST'])
def done():
    stream_name = request.form.get('name')
    r = requests.post('http://' + dispatch_server_address + '/stream_status_changed',
				data={'name': stream_name, 'status': 0})
    print(r.text)
    return 'ok'
    abort(401)

@application.route("/add", methods=['POST'])
def add():
    ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    if ip != dispatch_server_address:
        abort(401)
    stream_name = request.form.get('name')
    key = request.form.get('key')
    if stream_name == None or key == None:
        return str(request.form)
        abort(404)
    redis_store.set(stream_name, key)
    return 'ok'

if __name__ == "__main__":
    application.run(host='0.0.0.0')
