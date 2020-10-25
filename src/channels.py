from data import data
from error import InputError, AccessError
import auth

'''
    Provide a list of all the channels and all their details.
    An authorised user must be appart of the channel. 
    
    Args:
        1. Token of authorised user (int)
    Return:
        A dictionary of all the channels and their associated details 
        - Each key is a channel 

    An AccessError or InputError is raised when there are errors in the function call.
'''

def channels_list(token):
    
    channels = []
    u_id = 0
    validated = False

    # Check for authentication
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            validated = True
    
    if not validated:
        raise AccessError('Invalid Token')
    
    # Loop through channels, and associated users to find matches -> inefficient?
    for channel in data['channels']:
        for member in channel['all_members']:
            if member == u_id:
                channels.append(channel)
    
    return channels

'''
    Provide a list of all the channels and all their details.
    The authentication does not impact the list.
    
    Args:
        1. Token of user (int)
    Return:
        A dictionary of all the channels and their associated details. 
        The Authentication does not matter
        - Each key is a channel 

    An AccessError or InputError is raised when there are errors in the function call.
'''

def channels_listall(token):

    # Check for authentication
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            validated = True
    
    if not validated:
        raise AccessError('Invalid Token')

    # List all channels (regardless of authentication)
    return data['channels']

def channels_create(token, name, is_public):

    # Test whether channel name is more than 20 characters.
    if len(name) > 20:
        raise InputError('Invalid channel name: Must be less than 20 characters')

    global data
    channel_creator = {}
    validated = False

    # Check for authentication & retrieve owner member id
    for user in data['users']:
        if user['token'] == token:
            channel_creator['u_id'] = user['u_id']
            channel_creator['name_first'] = user['name_first']
            channel_creator['name_last'] = user['name_last']
            validated = True
    
    if not validated:
        raise AccessError('Invalid Token')

    channel = {
        'channel_id': len(data['channels']),
        'name': name,
        'all_members': [ channel_creator['u_id'] ],
        'owner_members': [ channel_creator['u_id'] ],
        'is_public': is_public,
    }

    data['channels'].append(channel)

    return {
        'channel_id': channel['channel_id']
    }
