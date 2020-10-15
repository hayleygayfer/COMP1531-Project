data = {
    'users': [
        {
            'u_id': 1,
            'email': 'random@email.com',
            'password': 'password',
            'token': '123456',
            'name_first': 'John',
            'name_last': 'Doe'
        }
    ],
    'channels': [
        {
            'channel_id': 1,
            'name': 'channel1',
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'John',
                    'name_last': 'Doe'
                }
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'John',
                    'name_last': 'Doe'
                }
            ],
            'is_public': True,
            'messages': [
                {
                    'u_id': 1,
                    'message_id': 10001,
                    'message': "Hi, this is a simple test msg"
                },
                {
                    'u_id': 2,
                    'message_id': 10002,
                    'message': "I got it!"
                }
            ],
            'message_count': 2
        }
    ]
}