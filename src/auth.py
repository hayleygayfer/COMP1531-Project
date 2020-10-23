from data import data
from error import InputError, AccessError
from re import search # regex for email validation
from random import random

def auth_login(email, password):
    if validate_email(email) == False:
        raise InputError("Email entered is not a valid email")

    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                user['token'] = email
                return {
                    'u_id': user['u_id'],
                    'token': user['token'],
                }
            else:
                raise InputError("Password is not correct")
    raise InputError("Email entered does not belong to a user")

def auth_logout(token):
    for user in data['users']:
        if user['token'] == token:
            user['token'] = ''
            return {
                'is_success': True,
            }
    
    return {
        'is_success': False,
    }

def auth_register(email, password, name_first, name_last):
    if validate_email(email) == False:
        raise InputError(f"Email entered is not a valid email ")

    if validate_first_name(name_first) == False:
        raise InputError(f"{name_first} is not between 1 and 50 characters")

    if validate_last_name(name_last) == False:
        raise InputError(f"{name_last} is not between 1 and 50 characters")
    
    if validate_password(password) == False:
        raise InputError("Password entered is less than 6 characters long")

    for user in data['users']:
        if user['email'] == email:
            raise InputError("Email address is already being used by another user")

    handle = generate_valid_handle(name_first, name_last)
    permissions = 'MEMBER'
    if data['users'] == []:
        permissions = 'OWNER'

    data['users'].append(
        {
            'u_id': len(data['users']) + 1,
            'token': '',
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': handle,
            'permissions': permissions,
        }
    )

    return {
        'u_id': len(data['users']),
        'token': email,
    }

def validate_email(email):
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if search(regex, email):  
        return True    
    else:  
        return False

def validate_first_name(name_first):
    if not 0 < len(name_first) <= 50:
        return False

    for character in name_first:
        if not character.isalpha() == True or character == '-':
            return False


def validate_last_name(name_last):
    if not 0 < len(name_last) <= 50:
        return False

    for character in name_last:
        if not character.isalpha() == True or character == '-' or character == ' ':
            return False

def validate_password(password):
    if len(password) < 6:
        return False

def check_handle_exists(handle):
    for user in data['users']:
        if user['handle_str'] == handle:
            return True
    return False
 
def generate_valid_handle(name_first, name_last):
    handle = "{0}{1}".format(name_first, name_last).lower()
    handle = handle[:20]

    # Default first_last name
    if not check_handle_exists(handle):
        return handle

    # Iterate to find a valid handle
    while check_handle_exists(handle):
        handle = handle[:15]
        handle = handle + str(int(random()*100000))
    return handle
