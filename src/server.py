import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from data import data

from auth import auth_register, auth_login, auth_logout
from channels import channels_list, channels_listall, channels_create

def defaultHandler(err):
    response = err.get_response()
    print('response', err, err.get_response())
    response.data = dumps({
        "code": err.code,
        "name": "System Error",
        "message": err.get_description(),
    })
    response.content_type = 'application/json'
    return response

APP = Flask(__name__)
CORS(APP)

APP.config['TRAP_HTTP_EXCEPTIONS'] = True
APP.register_error_handler(Exception, defaultHandler)

# Example
@APP.route("/echo", methods=['GET'])
def echo():
    data = request.args.get('data')
    if data == 'echo':
        raise InputError(description='Cannot echo "echo"')
    return dumps({
        'data': data
    })

###### AUTH ######

# Clear
@APP.route("/clear", methods=['DELETE'])
def http_clear():
    global data
    data['users'].clear()
    data['channels'].clear()
    return {}


# Auth Register
@APP.route("/auth/register", methods=['POST'])
def http_auth_register():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    name_first = request.get_json()["name_first"]
    name_last = request.get_json()["name_last"]
    response = auth_register(email, password, name_first, name_last)
    return dumps(response)

@APP.route("/auth/login", methods=['POST'])
def http_auth_login():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    response = auth_login(email, password)
    return dumps(response)

@APP.route("/auth/logout", methods=['POST'])
def http_auth_logout():
    token = request.get_json()["token"]
    response = auth_logout(token)
    return dumps(response)

###### CHANNELS ######

# Channels_list
@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    token = request.get_json()["token"]
    response = channels_list(token)
    return dumps(response)

# Channels_listall
@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    token = request.get_json()["token"]
    response = channels_listall(token)
    return dumps(response)

# Channels_create
@APP.route("/channels/create", methods=['POST'])
def http_channels_create():
    token = request.get_json()["token"]
    name = request.get_json()["name"]
    is_public = request.get_json()["is_public"]
    response = channels_create(token, name, is_public)
    return dumps(response)

if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port