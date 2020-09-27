# IMPORTANT
# To whoever is implementing the functions for channel.py ,
# if you're not happy with some of the assumptions then pls let me know
# - Rohan

def channel_invite(token, channel_id, u_id):
    # If you invite someone (yourself included) to a channel that the user already exists in then raise InputError
    return {
        'is_success': True
    }

def channel_details(token, channel_id):
    return {
        'name': 'Hayden',
        'owner_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
        'all_members': [
            {
                'u_id': 1,
                'name_first': 'Hayden',
                'name_last': 'Jacobs',
            }
        ],
    }

def channel_messages(token, channel_id, start):
    return {
        'messages': [
            {
                'message_id': 1,
                'u_id': 1,
                'message': 'Hello world',
                'time_created': 1582426789,
            }
        ],
        'start': 0,
        'end': 50,
    }

def channel_leave(token, channel_id):
    # You cannot leave a channel if you are the only owner (raise InputError)
    return {
        'is_success': True
    }

def channel_join(token, channel_id):
    # A user CANNOT join a private channel they MUST be invited (raise AccessError)
    return {
        'is_success': True
    }

def channel_addowner(token, channel_id, u_id):
    
    return {
        'is_success': True
    }

def channel_removeowner(token, channel_id, u_id):
    
    return {
        'is_success': True
    }