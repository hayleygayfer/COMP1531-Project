import data from data

def channels_list(token):

    channels = []
    u_id = 0

    # Check for authentication
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
    
    # Loop through channels, and associated users to find matches -> inefficient
    for channel in data['channels']:
        for member in channel['all_members']:
            if member == u_id:
                channels.append(channel)
    
    return {
        'channels': channels
    }

def channels_listall(token):

    return {
        'channels': data['channels']
    }

def channels_create(token, name, is_public):
    u_id = 0

    # Check for authentication & retrieve owner member id
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']

    channel = {
        'channel_id': len(data['channels']),
        'name': name,
        'is_public': is_public,
        'all_members': [u_id],
        'owner_members': [u_id]
    }

    data['channels'].append(channel)

    return {
        'channel_id': channel['channel_id']
    }
