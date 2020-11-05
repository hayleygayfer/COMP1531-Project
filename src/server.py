import sys
from json import dumps
from flask import Flask, request
from flask_cors import CORS
from error import InputError
from data import data

import auth
from other import search, users_all, admin_userpermission_change
import channel as ch
from channels import channels_list, channels_listall, channels_create
import message as msg
import user
from standup import standup_start, standup_active, standup_send


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

# Auth/Register
@APP.route("/auth/register", methods=['POST'])
def http_auth_register():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    name_first = request.get_json()["name_first"]
    name_last = request.get_json()["name_last"]
    response = auth.auth_register(email, password, name_first, name_last)
    return dumps(response)

# Auth/Login
@APP.route("/auth/login", methods=['POST'])
def http_auth_login():
    email = request.get_json()["email"]
    password = request.get_json()["password"]
    response = auth.auth_login(email, password)
    return dumps(response)

# Auth/Logout
@APP.route("/auth/logout", methods=['POST'])
def http_auth_logout():
    token = request.get_json()["token"]
    response = auth.auth_logout(token)
    return dumps(response)

# Auth/PasswordReset/Request
@APP.route("/auth/passwordreset/request", methods=['POST'])
def http_auth_passwordreset_request():
    email = request.get_json()['token']
    response = auth.auth_passwordreset_request(email)
    return dumps(response)

# Auth/PasswordReset/Reset
@APP.route("/auth/passwordreset/reset", methods=['POST'])
def http_auth_passwordreset_reset():
    reset_code = request.get_json()['reset_code']
    new_password = request.get_json()['new_password']
    response = auth.auth_passwordreset_reset(reset_code, new_password)
    return dumps(response)


###### CHANNEL ########

# Channel/Invite
@APP.route("/channel/invite", methods=['POST'])
def http_channel_invite():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    u_id = int(request.get_json()["u_id"])
    response = ch.channel_invite(token, channel_id, u_id)
    return dumps(response)

# Channel/Details
@APP.route("/channel/details", methods=['GET'])
def http_channel_details():
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    response = ch.channel_details(token, channel_id)
    return dumps(response)

# Channel/Messages
@APP.route("/channel/messages", methods=['GET'])
def http_channel_msgs():
    token = request.args.get("token")
    channel_id = int(request.args.get("channel_id"))
    start = int(request.args.get("start"))
    response = ch.channel_messages(token, channel_id, start)
    return dumps(response)

# Channel/Leave
@APP.route("/channel/leave", methods=['POST'])
def http_channel_leave():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    response = ch.channel_leave(token, channel_id)
    return dumps(response)

# Channel/Join
@APP.route("/channel/join", methods=['POST'])
def http_channel_join():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    response = ch.channel_join(token, channel_id)
    return dumps(response)

# Channel/AddOwner
@APP.route("/channel/addowner", methods=['POST'])
def http_channel_add():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    u_id = int(request.get_json()["u_id"])
    response = ch.channel_addowner(token, channel_id, u_id)
    return dumps(response)

# Channel/RemoveOwner
@APP.route("/channel/removeowner", methods=['POST'])
def http_channel_rem():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    u_id = int(request.get_json()["u_id"])
    response = ch.channel_removeowner(token, channel_id, u_id)
    return dumps(response)


###### USER ######

# User/Profile
@APP.route("/user/profile", methods=['GET'])
def http_user_profile():
    token = request.args.get('token')
    u_id = int(request.args.get('u_id'))
    response = user.user_profile(token, u_id)
    return dumps(response)

# User/Profile/Setname
@APP.route("/user/profile/setname", methods=['PUT'])
def http_user_profile_setname():
    token = request.get_json()['token']
    name_first = request.get_json()['name_first']
    name_last = request.get_json()['name_last']
    response = user.user_profile_setname(token, name_first, name_last)
    return dumps(response)

# User/Profile/Setemail
@APP.route("/user/profile/setemail", methods=['PUT'])
def http_user_profile_setemail():
    token = request.get_json()['token']
    email = request.get_json()['email']
    response = user.user_profile_setemail(token, email)
    return dumps(response)

# User/Profile/Sethandle
@APP.route("/user/profile/sethandle", methods=['PUT'])
def http_user_profile_sethandle():
    token = request.get_json()['token']
    handle = request.get_json()['handle_str']
    response = user.user_profile_sethandle(token, handle)
    return dumps(response)

# User/Profile/Uploadphoto
@APP.route("/user/profile/uploadphoto", methods=['POST'])
def http_user_profile_uploadphoto():
    token = request.get_json()['token']
    img_url = request.get_json()['img_url']
    x_start = int(request.get_json()['x_start'])
    y_start = int(request.get_json()['y_start'])
    x_end = int(request.get_json()['x_end'])
    y_end = int(request.get_json()['y_end'])
    response = user.user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end)
    return dumps(response)


###### CHANNELS ######

# Channels/list
@APP.route("/channels/list", methods=['GET'])
def http_channels_list():
    token = request.args.get("token")
    response = channels_list(token)
    return dumps(response)

# Channels/listall
@APP.route("/channels/listall", methods=['GET'])
def http_channels_listall():
    token = request.args.get("token")
    response = channels_listall(token)
    return dumps(response)

# Channels/create
@APP.route("/channels/create", methods=['POST'])
def http_channels_create():
    token = request.get_json()["token"]
    name = request.get_json()["name"]
    is_public = request.get_json()["is_public"]
    response = channels_create(token, name, is_public)
    return dumps(response)


###### OTHER ######

# users/all
@APP.route("/users/all", methods=['GET'])
def http_users_all():
    token = request.args.get("token")
    response = users_all(token)
    return dumps(response)

# admin/userpermission/change
@APP.route("/admin/userpermission/change", methods=['POST'])
def http_admin_userpermission_change():
    token = request.get_json()["token"]
    u_id = int(request.get_json()["u_id"])
    permission_id = int(request.get_json()["permission_id"])
    response = admin_userpermission_change(token, u_id, permission_id)
    return dumps(response)

# search
@APP.route("/search", methods=['GET'])
def http_search():
    token = request.args.get("token")
    query_str = request.get_json()["query_str"]
    response = search(token, query_str)
    return dumps(response)


### MESSAGES ###

# Message send
@APP.route("/message/send", methods=['POST'])
def http_message_send():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    message = request.get_json()["message"]
    response = msg.message_send(token, channel_id, message)
    return dumps(response)

# Message remove
@APP.route("/message/remove", methods=['DELETE'])
def http_message_remove():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["message_id"])
    response = msg.message_remove(token, channel_id)
    return dumps(response)

# Message edit
@APP.route("/message/edit", methods=['PUT'])
def http_message_edit():
    token = request.get_json()["token"]
    message_id = int(request.get_json()["message_id"])
    message = request.get_json()["message"]
    response = msg.message_edit(token, message_id, message)
    return dumps(response)

# Message sendlater
@APP.route("/message/sendlater", methods=['POST'])
def http_message_sendlater():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["message_id"])
    message = request.get_json()["message"]
    time_sent = int(request.get_json()["time_sent"])
    response = msg.message_sendlater(token, channel_id, message, time_sent)
    return dumps(response)

# Message react
@APP.route("/message/react", methods=['POST'])
def http_message_react():
    token = request.get_json()["token"]
    message_id = int(request.get_json()["message_id"])
    react_id = int(request.get_json()['react_id'])
    response = msg.message_react(token, message_id, react_id)
    return dumps(response)

# Message unreact
@APP.route("/message/unreact", methods=['POST'])
def http_message_unreact():
    token = request.get_json()["token"]
    message_id = int(request.get_json()["message_id"])
    react_id = int(request.get_json()["react_id"])
    response = msg.message_unreact(token, message_id, react_id)
    return dumps(response)

# Message pin
@APP.route("/message/pin", methods=['POST'])
def http_message_pin():
    token = request.get_json()["token"]
    message_id = int(request.get_json()["message_id"])
    response = msg.message_pin(token, message_id)
    return dumps(response)

# Message unpin
@APP.route("/message/unpin", methods=['POST'])
def http_message_unpin():
    token = request.get_json()["token"]
    message_id = int(request.get_json()["message_id"])
    response = msg.message_unpin(token, message_id)
    return dumps(response)


##### STANDUP #####

# Standup/start
@APP.route("/standup/start", methods=['POST'])
def http_standup_start():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    length = int(request.get_json()['length'])
    response = standup_start(token, channel_id, length)
    return dumps(response)

# Standup/active
@APP.route("/standup/active", methods=['GET'])
def http_standup_active():
    token = request.args.get("token")
    channel_id = int(request.get_json()["query_str"])
    response = standup_active(token, channel_id)
    return dumps(response)

# Standup/send
@APP.route("/standup/send", methods=['POST'])
def http_standup_send():
    token = request.get_json()["token"]
    channel_id = int(request.get_json()["channel_id"])
    message = request.get_json()['message']
    response = standup_send(token, channel_id, message)
    return dumps(response)


if __name__ == "__main__":
    APP.run(port=0) # Do not edit this port