from data import *

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
                return "Unsuccessful"
    print(f"The user {email} is not registered")
    # placeholder return
    return "Unsuccessful"

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


