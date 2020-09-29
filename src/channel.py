# Comments in this file are assumptions
from data import data
from error import InputError, AccessError

def channel_invite(token, channel_id, u_id):
    # If you invite someone (yourself included) to a channel that the user already exists in then raise InputError
    return {
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
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    pass

    return {
    }

def channel_join(token, channel_id):
    # A user CANNOT join a private channel they MUST be invited (raise AccessError)
    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")
    
    if private_channel(channel_id, token) == True:
        raise AccessError(f"The Channel ID: {channel_id} entered is a private channel ")

    if exists_in_channel(channel_id) == True:
        raise AccessError(f"You are already a member of the Channel ID: {channel_id} ")
    
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']
            append_data(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_addowner(token, channel_id, u_id):
    return {
    }

def channel_removeowner(token, channel_id, u_id):
    # You are allowed to remove yourself as an owner
    return {
    }

def validate_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

def private_channel(channel_id, token):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if status == channel['is_public']:
                return False
    return True

# def exists_in_channel(channel_id, token):
   
def append_data(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(
                {
                    'u_id': u_id,
                    'name_first': name_first,
                    'name_last': name_last,
                }
            )

