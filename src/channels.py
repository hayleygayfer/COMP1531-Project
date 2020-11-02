from data import data
from error import InputError, AccessError
import auth

def channels_list(token):
    '''
    Provide a list of all the channels and all their details.
    An authorised user must be appart of the channel. 
    
    Args:
        1. Token of authorised user (str)
    Return:
        A dictionary of all the channels and their associated details 
        - Each key is a channel 

    An AccessError or InputError is raised when there are errors in the function call.
    '''
    
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
    '''
    Provide a list of all the channels and all their details.
    The authentication does not impact the list.
    
    Args:
        1. Token of user (str)
    Return:
        A dictionary of all the channels and their associated details. 
        The Authentication does not matter
        - Each key is a channel 

    An AccessError or InputError is raised when there are errors in the function call.
    '''

    # Check for authentication
    auth.validate_token(token)

    # List all channels (regardless of authentication)
    return {
        'channels': data['channels']
    }


def channels_create(token, name, is_public):
    '''
    Creates a new channel with that name that is either a public or private channel.
    The name must be more than 20 characters long.
    Member must be authenticated to create channel. 
    
    Args:
        1. Token of user (str)
        2. Name of channel (string): Must be more than 20 characters long
        3. If the channel is public or private (True/False) 
    Return:
        A dictionary of all channel IDs.
        - All keys are channel IDs
        - The data is taken from channel

    An AccessError or InputError is raised when there are errors in the function call.
    '''

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
