data = {
    'users': [
        {
            'u_id': 1,
            'email': 'random@email.com',
            'password': 'password',
            'token': '123456'
        }
    ],
    'channels': [
        {
            'id': 1,
            'name': 'channel1'
        }
    ]
}

def clear():
    global data
    data = {
        'users': [],
        'channels': []
    }