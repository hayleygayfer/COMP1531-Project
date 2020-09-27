from data import *
import re

def auth_login(email, password):
    for user in data['users']:
        if user['email'] == email:
            if user['password'] == password:
                print(f"You've logged in as {email}")
                user['token'] = email
                return {
                    'u_id': user['u_id'],
                    'token': user['token'],
                }
            else:
                print("Incorrect password")
                # placeholder return
                return {
                    'is_success': False
                }
    print(f"The user {email} is not registered")
    # placeholder return
    return {
        'is_success': False
    }

def auth_logout(token):
    for user in data['users']:
        if user['token'] == token:
            user['token'] = ''
            print(f"{user['email']}) has been logged out")
            return {
                'is_success': True,
            }
    
    print(f"{user['email']} is already logged out")
    return {
        'is_success': False,
    }

def auth_register(email, password, name_first, name_last):
    if validate_email(email) == False:
        print("Invalid email")
        return False

    if validate_first_name(name_first) == False:
        print("Invalid first name")
        return False

    if validate_last_name(name_last) == False:
        print("Invalid last name")
        return False
    
    if validate_password(password) == False:
        print("Invalid password")
        return False

    for user in data['users']:
        if user['email'] == email:
            print("Email already in use")
            return False

    data['users'].append(
        {
            'u_id': len(data['users']) + 1,
            'token': '',
            'email': email,
            'password': password,
            'name_first': name_first,
            'name_last': name_last,
        }
    )

    return {
        'u_id': len(data['users']),
        'token': email,
    }

def validate_email(email):
    regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    if(re.search(regex,email)):  
        return True    
    else:  
        return False

def validate_first_name(name_first):
    if not 0 < len(name_first) < 50:
        return False

    for character in name_first:
        if not character.isalpha() == True or character == '-':
            return False


def validate_last_name(name_last):
    if not 0 < len(name_last) < 50:
        return False

    for character in name_last:
        if not character.isalpha() == True or character == '-' or character == ' ':
            return False

def validate_password(password):
    if len(password) <= 1:
        return False

    

    



