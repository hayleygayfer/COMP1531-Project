from data import data
from user import find_match, find_user
from error import AccessError, InputError
from channel import user_is_owner, validate_user
from channels import channels_list

def clear():
    global data
    data['users'].clear()
    data['channels'].clear()

    return {}

def users_all(token):
    if valid_token(token) is False:
        raise AccessError
    return {
        'users': data['users']
    }

def admin_userpermission_change(token, u_id, permission_id):
    #print(permission_id)

    if valid_token(token) is False:
        raise AccessError

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
    if valid_token(token) is False:
        raise AccessError("Invalid token")

    # Search not specific enough
    if len(query_str) <= 1:
        raise InputError("Enter at least 2 characters")
    
    channels = channels_list(token)['channels']
    messages = []

    for channel in channels:
        for msg in channel['messages']:
            if query_str in msg['message']:
                messages.append(msg['message'])

    return {
        'messages': messages
    }

# validate token
def valid_token(token):
    for users in data['users']:
        if token == users.get('token'):
            return True
    return False