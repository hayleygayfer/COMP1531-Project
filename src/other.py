import data
from user import find_match, find_user
from error import AccessError, InputError

def clear():
    global data
    data['users'].clear()
    data['channels'].clear()

def users_all(token):
    return {
        data['users']
    }

def admin_userpermission_change(token, u_id, permission_id):
    if find_match('u_id', u_id) == []:
        raise InputError("Not a valid u_id")

    if find_match('permission_id', permission_id) == []:
        raise AccessError("user does not have the correct permissions")

    

    return {}


def search(token, query_str):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
    }