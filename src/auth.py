from data import data
from error import InputError, AccessError
from re import search # regex for email validation
from random import random
import hashlib
import jwt
import smtplib, ssl
from random import random

SECRET = 'adaskljnkjladsncjakldnckjscankj'

def auth_login(email, password):
    '''
    Matches an email and password to a user to log them in.
    After the user logs in, they become authenticated and an active token is generated and added to their user data
        * A new token is generated every time the user is logged in
    The password is immediately hashed so it is not stored in the database
        * The hashed password is compared with the hashed password for the input email
    Can be accessed by anyone but will only be successful if the user has already registered.

    Args:
        1. email (str): the user email used to idenitfy a user
        2. password (str): a password used to verify their identity

    Return:
        A dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_email(email) == False:
        raise InputError("Email entered is not a valid email")

    for user in data['users']:
        if user['email'] == email:
            if user['password'] == hashlib.sha256(password.encode()).hexdigest():
                user['token'] = jwt.encode({'email': user['email']}, SECRET, algorithm='HS256').decode('utf-8')
                return {
                    'u_id': user['u_id'],
                    'token': user['token'],
                }
            else:
                raise InputError("Password is not correct")
    raise InputError("Email entered does not belong to a user")


def auth_logout(token):
    '''
    Takes the active token and logs the user out
    After the user logs out, their token becomes inactive and will never be valid again
    Can be accessed by anyone who is currently logged in

    Args:
        1. token (str): the token of the authenticated user who is attempting to log out

    Return:
        A dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

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
    '''
    Takes some information about a new user to create an account for them
    If a new user manages to register successfully, they automatically become logged in and an active token is generated (see auth_login)

    Args:
        1. email (str): the email of the new user
        2. password (int): used to identify the channel
        3. name_first (string): the first name of the user (cannot contain multiple names)
        4. name_last (string): the surname of the user (can contain multiple names)

    Return:
        A dictionary containing the following keys:
        'u_id' (int): The user_id is a fixed integer used for identification
        'token' (str): A ticket which allows the user to explore the Flockr in their current session

    The password is hashed before it is stored so the original string is not visible on the server
    A handle is generated using the names of the user and is added to their user data

    An AccessError or InputError is raised when there are errors in the function call

    '''

    SECRET = 'adaskljnkjladsncjakldnckjscankj'

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

    # Hashed password
    hash_password = hashlib.sha256(password.encode()).hexdigest()

    # Token
    encoded_token = jwt.encode({'email': email}, SECRET, algorithm='HS256').decode('utf-8')

    data['users'].append(
        {
            'u_id': len(data['users']) + 1,
            'token': (encoded_token),
            'email': email,
            'password': hash_password,
            'name_first': name_first,
            'name_last': name_last,
            'handle_str': handle,
            'permissions': permissions,
        }
    )


    return {
        'u_id': len(data['users']),
        'token': str(encoded_token),
    }

## ITERATION 3

def auth_passwordreset_request(email):
    '''
    Given an email, sends the email a reset code, to reset the password.

    Args:
        1. email (str): the email of the user requesting the password be reset

    Return:
        {}

    The function first checks the email is valid, then sends email with a random code, which is added to memory.
    '''
    for user in data['users']:
        if user['email'] == email:
            reset_code = {
                'reset_code': str(generate_reset_code()),
                'u_id': user['u_id']
            }
            data['reset_codes'].append(reset_code)
            port = 465
            context = ssl.create_default_context()
            message = f"""\
            Flockr Password Reset Request

            Hi {user['name_first']},
            We've recently recieved a password reset request from you for Flockr. If you did not request this, ignore this email.
            Your password reset code is: {reset_code['reset_code']}"""
            with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
                server.login("flockrhelp@gmail.com", "surelypub")
                server.sendmail("flockrhelp@gmail.com", email, message)

    return {}

def auth_passwordreset_reset(reset_code, new_password):
    '''
    Given a reset code, sends the email a reset code, to reset the password.

    Args:
        1. reset code (str): the reset code of the user requesting the password be reset
        2. new_password (str): the new password for the user requesting a password reset

    Return:
        {}

    The function first checks the reset code is valid, then checks the password
     is valid, then changes the password of the user.
    '''
    for combination in data['reset_codes']:
        if combination['reset_code'] == reset_code:
            if not validate_password(new_password):
                raise InputError('Invalid Password')
            for user in data['users']:
                if user['u_id'] == combination['u_id']:
                    user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
                    data['reset_codes'].remove(combination)
                    return {}
    raise InputError('Invalid Reset Code')


#########################################################################

def generate_reset_code():
    reset_code = 0
    unique_code = False
    while unique_code == False:
        unique_code = True
        reset_code = int(random()*100000)
        for combination in data['reset_codes']:
            if combination['reset_code'] == reset_code:
                unique_code = False
    return reset_code

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

###### VALIDATE TOKEN ######

def validate_token(token):
    SECRET = 'adaskljnkjladsncjakldnckjscankj'
    try:
        email = jwt.decode(token, SECRET, algorithms=['HS256'])
    except:
        raise AccessError("Invalid token")
    for user in data['users']:
        if user.get('email') == email['email']:
            return user
    return None


if __name__ == '__main__':
    auth_register("ethoshansen@gmail.com", "password", "Ethan", "Hansen")
    print(data)
    auth_passwordreset_request("ethoshansen@gmail.com")
    print(data)