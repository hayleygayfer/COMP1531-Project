# Comments in this file are assumptions
from data import data
from error import InputError, AccessError

def channel_invite(token_inviter, channel_id, u_id_invitee):
    # If you invite someone (yourself included) to a channel that the user already exists in then raise InputError
    
    if validate_token(token_inviter) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if validate_user(u_id_invitee) == False:
        raise InputError(f"The User ID: {u_id} entered is not a valid user ")
    
    # Matching the inviter and the token
    for user in data['users']:
        if user['token'] == token_inviter:
            u_id_inviter = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if exists_in_channel(channel_id, u_id_invitee) == True:
        raise InputError(f"The User already exists in this Channel ")
    
    if exists_in_channel(channel_id, u_id_inviter) == False:
        raise AccessError("User is not a part of the Channel ")

    # Append the user to 'all_members' of the channel after all tests are passed
    append_data(channel_id, u_id_invitee, name_first, name_last)

    return {
        'is_success': True
    }

def channel_details(token, channel_id):

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
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

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # InputError (start is greater than the total number of messages in the channel)

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

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

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    pass

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    return {
        'is_success': True
    }

def channel_join(token, channel_id):

    if validate_token(token_inviter) == False:
        raise AccessError(f"Not a valid token ")

    # Matching the user and the token
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    # Raising input and access errors
    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")
    
    if private_channel(channel_id) == True:
        raise AccessError(f"The Channel ID: {channel_id} entered is a private channel ")

    if exists_in_channel(channel_id, u_id) == True:
        raise InputError(f"You are already a member of the Channel ID: {channel_id} ")
    
    # After all tests are passed, append the data for all channel members
    append_data(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_addowner(token, channel_id, u_id):

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if user_is_owner(channel_id, u_id) == True:
        raise InputError(f"User {u_id} is already an owner of the channel ")
    
    append_user_owner(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_removeowner(token, channel_id, u_id):
    # You are allowed to remove yourself as an owner

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if user_is_owner(channel_id, u_id) == False:
        raise InputError(f"User {u_id} is not an owner of the channel ")

    clear_user_owner(channel_id, u_id, name_first, name_last)

    return {
    }

# Validation functions
def validate_token(token):
    for users in data['users']:
        if token == users['token']:
            return True
    return False

def validate_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

def validate_user(u_id):
    for users in data['users']:
        if users['u_id'] == u_id:
            return True
    return False

# Check if channel is private
def private_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if status == channel['is_public']:
                return False
    return True

# Check if user exists within the channel
def exists_in_channel(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['all_members']:
                if user['u_id'] == u_id:
                    return True
    return False

# Append data of user to channel where all members can see
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

def user_is_owner(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners['u_id'] == u_id:
                    return True:
    return False

def append_user_owner(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['owner_members'].append(
                {
                    'u_id': u_id,
                    'name_first': name_first,
                    'name_last': name_last,
                }
            )

def clear_user_owner(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners['u_id'] == u_id:
                    owners.clear()
                    
