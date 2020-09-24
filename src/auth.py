state = {
    users = [
        {
            'u_id': 1
            'token': 123456
            'email': "email@email.com"
            'password': "password"
            'name_first': "firstname"
            'name_last': "lastname"
        }
    ]
}

def auth_login(email, password):
    return {
        'u_id': 1,
        'token': '12345',
    }

def auth_logout(token):
    return {
        'is_success': True,
    }

def auth_register(email, password, name_first, name_last):
    state[users].append(
        {
            'u_id': len(state[users]) + 1
            'token': ''
            'email': email
            'password': password 
            'name_first': name_first
            'name_last': name_last  
        }
    )

    return {
        'u_id': 1,
        'token': '12345',
    }
