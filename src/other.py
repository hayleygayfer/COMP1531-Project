from data import data
from user import find_match, find_user
from error import AccessError, InputError
from channel import user_is_owner, validate_user
from channels import channels_list

OWNER = 1
MEMBER = 2

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
    
    if valid_token(token) is False:
        raise AccessError

    user = find_match('u_id', u_id)
    if user == []:
        raise InputError("Not a valid u_id")

    if permission_id != MEMBER and permission_id != OWNER:
        raise InputError("Permission does not exist")

    u_it = find_user(token)
    if data['users'][u_it]['permissions'] != OWNER:
        raise AccessError("You must be an owner to change permissions")

    u_token = user[0]['token']
    u_it = find_user(u_token)

    # Check if proposed permission change is already in effect
    if data['users'][u_it]['permissions'] == permission_id:
        if permission_id == OWNER:
            status = "n owner"
        else:
            status = " member"
        raise InputError(f"User is already a{status}")

    # Trying to remove the last flockr owner (which will be yourself)
    if count_owners() == 1 and permission_id == MEMBER:
        raise InputError("There must be at least one flockr owner")

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
            if query_str.lower() in msg['message'].lower():
                messages.append(msg)

    return {
        'messages': messages
    }

# validate token
def valid_token(token):
    for users in data['users']:
        if token == users.get('token'):
            return True
    return False

# count the number of flockr owners
def count_owners():
    num = 0
    for user in data['users']:
        if user['permissions'] == OWNER:
            num += 1
    return num