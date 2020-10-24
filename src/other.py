from data import data
from user import find_match, find_user
from error import AccessError, InputError
from channel import user_is_owner, validate_user
from channels import channels_list

def clear():
    global data
    data['users'].clear()
    data['channels'].clear()

def users_all(token):
    return {
        data['users']
    }

def admin_userpermission_change(token, u_id, permission_id):
    user = find_match('u_id', u_id)
    if user == []:
        raise InputError("Not a valid u_id")

    if permission_id != 'MEMBER' or 'OWNER':
        raise InputError("Permission does not exist")

    u_it = find_user(token)
    if data['users'][u_it]['permissions'] != 'OWNER':
        raise AccessError("User is not an owner")

    u_token = user[0]['token']
    u_it = find_user(u_token)
    data['users'][u_it]['permissions'] = permission_id
    
    return {}


def search(token, query_str):
    channels = channels_list(token)
    messages = []

    for channel in channels:
        messages.append(list(filter(lambda message: query_str in message['message'], channel['messages'])))

    return {
        messages
    }