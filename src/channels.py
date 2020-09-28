from data import data
from error import InputError

def channels_list(token):
    
    channels = []
    u_id = 0

    # Check for authentication
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    
    # Loop through channels, and associated users to find matches -> inefficient?
    for channel in data['channels']:
        for member in channel['all_members']:
            if member['u_id'] == u_id:
                channels.append(channel)
    
    return {
        'channels': channels
    }

def channels_listall(token):
    # List all channels (regardless of authentication)
    return {
        'channels': data['channels']
    }

def channels_create(token, name, is_public):

    # Test whether channel name is more than 20 characters.
    if len(name) > 20:
        raise InputError('Invalid channel name: Must be less than 20 characters')

    global data
    channel_creator = {}

    # Check for authentication & retrieve owner member id
    for user in data['users']:
        if user['token'] == token:
            channel_creator['u_id'] = user['u_id']
            channel_creator['name_first'] = user['name_first']
            channel_creator['name_last'] = user['name_last']

    channel = {
        'channel_id': len(data['channels']),
        'name': name,
        'is_public': is_public,
        'all_members': [ channel_creator ],
        'owner_members': [ channel_creator ]
    }

    data['channels'].append(channel)

    return {
        'channel_id': channel['channel_id']
    }
