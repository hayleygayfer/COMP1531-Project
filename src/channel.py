# Comments in this file are assumptions
from data import data
from error import InputError, AccessError

def channel_invite(token_inviter, channel_id, u_id_invitee):
    '''A token belonging to a user in a channel is used to invite another user who is not part of that channel.'''

    if validate_token(token_inviter) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if validate_user(u_id_invitee) == False:
        raise InputError(f"The User ID: {u_id_invitee} entered is not a valid user ")
    
    # Matching the inviter and the token
    u_id_inviter = token_to_u_id(token_inviter)['u_id']

    # Find name and last name of invitee
    name_first, name_last = u_id_to_name(u_id_invitee)

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
    '''A token is used to view the details of a channel the corresponding user in.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    u_id = token_to_u_id(token)['u_id']

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return channel

def channel_messages(token, channel_id, start):
    '''A token is used to access messages in a channel that the corresponding user is in.
    
    The system will return back up to 50 messages after the start value in a similar way that many websites use pagination to display small chunks of data at a time.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    u_id = token_to_u_id(token)['u_id']

    # Must be a member of the channel to view message ##TEST
    if (exists_in_channel(channel_id, u_id) == False):
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    # TODO: finish off this function
    
    if invalid_messages_start(channel_id, start) == True:
        raise InputError("Start is greater than the total messages in the channel")
        
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
    '''A token is used to leave a channel that the corresponding user are in.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    user_details = token_to_u_id(token)
    u_id = user_details['u_id']
    name_first = user_details['name_first']
    name_last = user_details['name_last']

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    if size_owners(channel_id) < 2 and is_token_owner(token, channel_id): 
        raise InputError("You are the only admin left in this channel. You cannot leave if you are the only admin")

    # Member leaves the channel and is cleared from all_members
    rem_user_member(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_join(token, channel_id):
    '''A token from a user is used to join a channel they are not currently in.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    user_details = token_to_u_id(token)
    u_id = user_details['u_id']
    name_first = user_details['name_first']
    name_last = user_details['name_last']
    
    # Only Flockr owners can join private channels
    if private_channel(channel_id) == True:
        if is_token_flockr_owner(token) == False:
            raise AccessError(f"The Channel ID: {channel_id} entered is a private channel ")

    if exists_in_channel(channel_id, u_id) == True:
        raise InputError(f"You are already a member of the Channel ID: {channel_id} ")
    
    # After all tests are passed, append the data for all channel members
    append_data(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_addowner(token, channel_id, u_id):
    '''A token from a channel owner is used to add another member as an owner of that channel.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if exists_in_channel(channel_id, u_id) == False:
        raise InputError(f"The User is not a member of the Channel ID: {channel_id} ")

    # Matching the user and the token
    token_uid = token_to_u_id(token)['u_id']

    # Flockr owner needs to be in the channel to add owners
    if exists_in_channel(channel_id, token_uid) == False and (is_token_flockr_owner(token) == True):
        raise AccessError(f"You as the Flockr owner, must be in the channel: {channel_id} to add an owner")
    
    # You must be an owner to add
    if (is_token_owner(token, channel_id) == False) and (is_token_flockr_owner(token) == False):
        raise AccessError("User is not an owner or owner of the Flockr")

    if user_is_owner(channel_id, u_id) == True:
        raise InputError(f"User {u_id} is already an owner of the channel ")

    # Matching the u_id to their name
    name_first, name_last = u_id_to_name(u_id)
    append_user_owner(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

def channel_removeowner(token, channel_id, u_id):
    '''A token from a channel owner is used to remove owner status from another member in that channel.'''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if exists_in_channel(channel_id, u_id) == False:
        raise InputError(f"The User is not a member of the Channel ID: {channel_id} ")

    if user_is_owner(channel_id, u_id) == False:
        raise InputError(f"User {u_id} is not an owner of the channel ")

    # Matching the user and the token
    token_uid = token_to_u_id(token)['u_id']
    
    # You cannot remove yourself as an owner
    if u_id == token_uid:
        raise InputError("You cannot remove yourself as owner")

    # Test to check that the Flockr owner must be in the channel to remove owners
    if exists_in_channel(channel_id, token_uid) == False and (is_token_flockr_owner(token) == True):
        raise AccessError(f"You as the Flockr owner, must be in the channel: {channel_id} to remove an owner")

    # You can only remove owners
    if (is_token_owner(token, channel_id) == False) and (is_token_flockr_owner(token) == False):
        raise AccessError(f"User {u_id} is not an owner of the channel")

    # Match the users u_id to their name
    name_first, name_last = u_id_to_name(u_id)

    # If the flockr owner removes the only owner, he/she becomes the new owner
    flockr_owner_u_id = data['users'][0].get('u_id')
    flockr_owner_name_first = data['users'][0].get('name_first')
    flockr_owner_name_last = data['users'][0].get('name_last')
    ####
    if is_token_flockr_owner(token) == True and is_token_owner(token, channel_id) == False:
        if user_is_owner(channel_id, u_id) == True:
            if size_owners(channel_id) == 1:
                append_user_owner(channel_id, flockr_owner_u_id, flockr_owner_name_first, flockr_owner_name_last)
    ####

    rem_user_owner(channel_id, u_id, name_first, name_last)

    return {
        'is_success': True
    }

#################################################################################
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

# Converts a token to the users id
def token_to_u_id(token):
    for user in data['users']:
        if user['token'] == token:
            return {
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }

# Obtains the users name from their id
def u_id_to_name(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return user['name_first'], user['name_last']

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

# Is the current u_id stored in the owners section of the channel
def user_is_owner(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners.get('u_id') == u_id:
                    return True
    return False

# Append user data to the owner members section of the channel
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

# Remove the user data from owner members
def rem_user_owner(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners.get('u_id') == u_id:
                    channel['owner_members'].remove(owners)

# Remove user data from channel
def rem_user_member(channel_id, u_id, name_first, name_last):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for members in channel['all_members']:
                if members.get('u_id') == u_id:
                    channel['all_members'].remove(members)

    # IF they are an owner they need to be cleared from owner_members
    rem_user_owner(channel_id, u_id, name_first, name_last)

# Is the authenticated user an owner of the channel
def is_token_owner(token, channel_id):      
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                # match the u_id of the authenticated user to the ids of all owners
                if token_to_u_id(token)['u_id'] == owners.get('u_id'):
                    return True
    return False

# Determine the number of owners in a channel
def size_owners(channel_id):
    owner_members = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            owner_members = len(channel['owner_members'])
    return owner_members

# Determine if the authenticated user is the flockr owner
def is_token_flockr_owner(token):
    if token == data['users'][0].get('token'):
        return True
    return False

#### TODO: Message functions currently working on

def invalid_messages_start(channel_id, start):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if channel['message_count'] <= start:
                return True
    return False
    