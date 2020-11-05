from data import data
from error import InputError, AccessError
from auth import validate_first_name, validate_last_name, validate_email

def user_profile(token, u_id):

    user_id = find_match('u_id', u_id)

    if user_id == []:
        raise InputError("Not a valid user")

    if user_id[0]['token'] != token:
        raise AccessError("Not a valid token")

    return {
        'user': user_id[0]
    }

def user_profile_setname(token, name_first, name_last):

    if validate_first_name(name_first) == False:
        raise InputError("Not a valid first name")

    if validate_last_name(name_last) == False:
        raise InputError("Not a valid last name")

    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")

    data['users'][u_it]['name_first'] = name_first
    data['users'][u_it]['name_last'] = name_last

    return { 
    }

def user_profile_setemail(token, email):
    if validate_email(email) == False:
        raise InputError("Not a valid email")

    if find_match('email', email) != []:
        raise InputError("Email already in use")
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")
 
    data['users'][u_it]['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    if validate_handle_str(handle_str) == False:
        raise InputError("Not a valid handle")

    if find_match('handle_str', handle_str) != []:
        raise InputError("handle already in use")
        
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")

    data['users'][u_it]['handle_str'] = handle_str

    return {
    }

## ITERATION 3

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):

    return {}



def validate_handle_str(handle_str):
    return 3 < len(handle_str) < 20
        
def find_match(parameter, match):
    return list(filter(lambda user: user[parameter] == match, data['users']))

def find_user(token):
    return next(i for i, user in enumerate(data['users']) if user['token'] == token)
