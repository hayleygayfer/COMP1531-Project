data = {
    'users': [],
    'channels': [],
}

'''
'users': [
    {
        'u_id': 1,
        'email': 'random@email.com',
        'password': 'password',
        'token': '123456',
        'name_first': 'John',
        'name_last': 'Doe',
        'handle_str': 'handle',
        'profile_img_url': 'https://google.com/sample_img'
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
                'time_created': 123456789,
                'reacts': [
                    {
                        'react_id': 0,
                        'u_ids': [0, 1, 2],
                        'is_this_user_racted': False
                    }
                    # ONLY ONE REACT ATM
                ],
                'is_pinned': True
            },
            {
                # Another message
            }
        ],
        'message_count': 2
    }
]
'''