from data import data
from error import InputError, AccessError
import auth

def channels_list(token):
    
    channels = []

    # Check for authentication
    user = auth.validate_token(token)
    
    # Loop through channels, and associated users to find matches -> inefficient?
    for channel in data['channels']:
        for member in channel['all_members']:
            if member == user['u_id']:
                channels.append(channel)
    
    return {
        'channels': channels
    }

def channels_listall(token):

    # Check for authentication
    user = auth.validate_token(token)

    # List all channels (regardless of authentication)
    return {
        'channels': data['channels']
    }

def channels_create(token, name, is_public):

    # Test whether channel name is more than 20 characters.
    if len(name) > 20:
        raise InputError('Invalid channel name: Must be less than 20 characters')

    # Check for authentication & retrieve owner member id
    channel_creator = auth.validate_token(token)
    
    channel = {
        'channel_id': len(data['channels']),
        'name': name,
        'all_members': [ channel_creator['u_id'] ],
        'owner_members': [ channel_creator['u_id'] ],
        'is_public': is_public,
        'messages': [],
        'message_count': 0
    }

    data['channels'].append(channel)

    return {
        'channel_id': channel['channel_id']
    }
