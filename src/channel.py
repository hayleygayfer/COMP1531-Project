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
        raise InputError(f"The User ID: {u_id_invitee} entered is not a valid user ")
    
    # Matching the inviter and the token
    for user in data['users']:
        if user['token'] == token_inviter:
            u_id_inviter = user['u_id']

    # Find name and last name of invitee
    for user in data['users']:
        if user['u_id'] == u_id_invitee:
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

    # Matching the user and the token
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

def channel_messages(token, channel_id, start):

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    # Matching the user and the token
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # TODO: InputError (start is greater than the total number of messages in the channel)

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

    # Matching the user and the token
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    if SIZE_OWNERS(channel_id) < 2 and is_token_owner(token, channel_id): 
        raise InputError("You are the only admin left in this channel. You cannot leave if you are the only admin")

    # Member leaves the channel and is cleared from all_members
    clear_user_member(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_join(token, channel_id):    

    if validate_token(token) == False:
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
        if is_token_flockr_owner(token) == True:
            break
        else:
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

    if exists_in_channel(channel_id, u_id) == False:
        raise InputError(f"The User is not a member of the Channel ID: {channel_id} ")

    # Matching the user and the token
    for user in data['users']:
        if user['u_id'] == u_id:
            name_first = user['name_first']
            name_last = user['name_last']

    if (is_token_owner(token, channel_id) == False) or (is_token_flockr_owner(token) == False):
        raise AccessError("User is not an owner or owner of the Flockr")

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

    if exists_in_channel(channel_id, u_id) == False:
        raise InputError(f"The User is not a member of the Channel ID: {channel_id} ")

    # Matching the user and the token
    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if is_token_owner(token, channel_id) == False:
        raise AccessError("User is not an owner of the channel")

    for user in data['users']:
        if user['token'] == token:
            u_id = user['u_id']
            name_first = user['name_first']
            name_last = user['name_last']

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if user_is_owner(channel_id, u_id) == False:
        if is_token_flockr_owner(token) == True:
            break
        else:
            raise InputError(f"User {u_id} is not an owner of the channel ")

    clear_user_owner(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

# TODO: Function prototypes currently working on


# Validation functions
def validate_token(token):
    for users in data['users']:
        if token == users.get('token'):
            return True
    return False

def validate_channel(channel_id):
    for channel in data['channels']:
        if channel.get('channel_id') == channel_id:
            return True
    return False

def validate_user(u_id):
    for users in data['users']:
        if users.get('u_id') == u_id:
            return True
    return False

# Check if channel is private
def private_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if channel.get('is_public') is True:
                return False
    return True

# Check if user exists within the channel
def exists_in_channel(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for user in channel['all_members']:
                if user.get('u_id') == u_id:
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
                if owners.get('u_id') == u_id:
                    return True
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
                if owners.get('u_id') == u_id:
                    owners.clear()

def clear_user_member(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for members in channel['all_members']:
                if members.get('u_id') == u_id:
                    members.clear()

    # IF they are an owner they need to be cleared from owner_members
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for members in channel['owner_members']:
                if members.get('u_id') == u_id:
                    members.clear()

def is_token_owner(token, channel_id):
    owner_member_u_id = 0
    for user in data['users']:
        if token == user.get('token'):
            owner_member_u_id = user['u_id']

    if owner_member_u_id == 0:
        return False
            
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owner_member_u_id == owners.get('u_id'):
                    return True
    return False


def SIZE_OWNERS(channel_id):
    owner_members = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            owner_members = len(channel['owner_members'])
    return owner_members

def is_token_flockr_owner(token):
    for users in data['users']:
        if token == users[0]['token']:
            return True
    return False
