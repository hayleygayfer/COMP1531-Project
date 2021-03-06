from data import data
from error import InputError, AccessError

FLOCKR_OWNER = 1

def channel_invite(token_inviter, channel_id, u_id_invitee):
    '''
    Invite a user who is not currently in the channel, to the channel.
    The invited user is added to the channel immediately.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token_inviter (str): the token of the authenticated user who is doing the inviting
        2. channel_id (int): used to identify the channel
        3. u_id_invitee (int): the user_id of the non-channel member who is getting the invitation

    Return:
        A dictionary to signify the fact that there were no errors in the function call

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_token(token_inviter) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    if validate_user(u_id_invitee) == False:
        raise InputError(f"The User ID: {u_id_invitee} entered is not a valid user ")
    
    # Matching the inviter and the token
    u_id_inviter = token_to_u_id(token_inviter)['u_id']

    if exists_in_channel(channel_id, u_id_invitee) == True:
        raise InputError(f"The User already exists in this Channel ")
    
    if exists_in_channel(channel_id, u_id_inviter) == False:
        raise AccessError("User is not a part of the Channel ")

    # Append the user to 'all_members' of the channel after all tests are passed
    append_data(channel_id, u_id_invitee)

    return {
        'is_success': True
    }

def channel_details(token, channel_id):
    '''
    Provide some details about a particular channel that the authenticated user is a part of.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is viewing the details
        2. channel_id (int): used to identify the channel

    Return:
        A dictionary containing details about the channel corresponding to the channel_id with keys:
        - 'name' (string): - channel name
        - 'owner_members' (array): - displays the owners in the channel including their user_id's, first name and surname
        - 'all_members' (array): - displays the regular members including their user_id's, first name and surname

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    u_id = token_to_u_id(token)['u_id']

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    # only return the channel name and members
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return {
                'name': channel['name'],
                'all_members': get_user_details(channel['all_members']),
                'owner_members': get_user_details(channel['owner_members'])
            }
            

def channel_messages(token, channel_id, start):
    '''
    Output a list of messages from a particular channel that the authenticated user is a part of.
    Uses pagination to display a maximum of 50 messages from the start value.
    The displayed messages start with the message with the start value index and prints previous messages.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is viewing the messages
        2. channel_id (int): used to identify the channel
        3. start (int): identifies the message to begin displaying other messages from

    Return:
        A dictionary containing details about the channel corresponding to the channel_id with keys:
        - 'messages' (array): an array containing details about some messages incluing the actual message string
        - 'start' (int): the starting index of the returned messages
        - 'end' (int): the ending index of the messages containing one of:
            * (start value + 50) to show that 50 messages have been returned
            * (-1) to show that all the older messages have been returned (less than 50 remaining messages)

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    u_id = token_to_u_id(token)['u_id']

    # Must be a member of the channel to view message ##TEST
    if (exists_in_channel(channel_id, u_id) == False):
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")
    
    if invalid_messages_start(channel_id, start) == True:
        raise InputError("Start is greater than the total messages in the channel")

    # default negative start values to 0
    if (start <= 0):
        start = 0
    
    # get the return 'end' depending on the # of messages left
    return_array = []
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            newest = channel['message_count'] - 1 - start
            if channel['message_count'] <= 50 or start + 50 >= channel['message_count']:
                end = -1
                oldest = -1
            else:
                end = start + 50
                oldest = channel['message_count'] - start - 51
                
            # add messages from newest to oldest
            for x in range(newest, oldest, -1):
                return_array.append(channel['messages'][x])


    # Updated for reacts
    # Set is_this_user_reacted for each message in the display messages depending on whether they have reacted or not
    for msg in return_array:
        if u_id in msg['reacts'][0]['u_ids']:
            msg['reacts'][0]['is_this_user_reacted'] = True
        else:
            msg['reacts'][0]['is_this_user_reacted'] = False

    # returns the relevant data in a dictionary
    return {
        'messages': return_array,
        'start': start,
        'end': end
    }

def channel_leave(token, channel_id):
    '''
    The authenticated user who is a part of a channel, leaves that channel.
    All channel details of that user (including owner status) gets removed.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is leaving
        2. channel_id (int): used to identify the channel

    Return:
        A dictionary to signify the fact that there were no errors in the function call

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    user_details = token_to_u_id(token)
    u_id = user_details['u_id']

    if exists_in_channel(channel_id, u_id) == False:
        raise AccessError(f"You are not a member of the Channel ID: {channel_id} ")

    if size_owners(channel_id) < 2 and is_token_owner(token, channel_id): 
        raise InputError("You are the only admin left in this channel. You cannot leave if you are the only admin")

    # Member leaves the channel and is cleared from all_members
    rem_user_member(channel_id, u_id)

    return {
        'is_success': True
    }

def channel_join(token, channel_id):
    '''
    The authenticated user who is not a part of a channel, joins that channel.
    Their details get added to that channel under 'all_members'.
    To be accessed from a user who is not a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is joining
        2. channel_id (int): used to identify the channel

    Return:
        A dictionary to signify the fact that there were no errors in the function call

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_token(token) == False:
        raise AccessError(f"Not a valid token ")

    if validate_channel(channel_id) == False:
        raise InputError(f"The Channel ID: {channel_id} entered is not valid ")

    # Matching the user and the token
    user_details = token_to_u_id(token)
    u_id = user_details['u_id']
    
    # Only Flockr owners can join private channels
    if private_channel(channel_id) == True:
        if is_token_flockr_owner(token) == False:
            raise AccessError(f"The Channel ID: {channel_id} entered is a private channel ")

    if exists_in_channel(channel_id, u_id) == True:
        raise InputError(f"You are already a member of the Channel ID: {channel_id} ")
    
    # After all tests are passed, append the data for all channel members
    append_data(channel_id, u_id)

    return {
        'is_success': True
    }

def channel_addowner(token, channel_id, u_id):
    '''
    The authenticated user who is a part of a channel, adds another user as an owner of the channel.
    The user to-be-added immediately becomes an owner with their details getting added to 'owner_members'.
    The user to-be-added cannot be an onwer of the channel with id channel_id.
    To be accessed from an owner of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is adding another owner
        2. channel_id (int): used to identify the channel
        3. u_id (int): the user_id of the user who is getting promoted to an owner

    Return:
        A dictionary to signify the fact that there were no errors in the function call

    An AccessError or InputError is raised when there are errors in the function call

    '''

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
    append_user_owner(channel_id, u_id)

    return {
        'is_success': True
    }

def channel_removeowner(token, channel_id, u_id):
    '''
    The authenticated user who is a part of a channel, removes another user as an owner of the channel.
    The user to-be-removed immediately gets their owner status revoked and their details gets deleted from 'owner_members'.
    The user to-be-removed must be an onwer of the channel with id channel_id.
    To be accessed from an owner of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is adding another owner
        2. channel_id (int): used to identify the channel
        3. u_id (int): the user_id of the user who is getting promoted to an owner

    Return:
        A dictionary to signify the fact that there were no errors in the function call

    An AccessError or InputError is raised when there are errors in the function call

    '''

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

    # If the flockr owner removes the only owner, he/she becomes the new owner
    flockr_owner_u_id = data['users'][0].get('u_id')

    ####
    if is_token_flockr_owner(token) == True and is_token_owner(token, channel_id) == False:
        if user_is_owner(channel_id, u_id) == True:
            if size_owners(channel_id) == 1:
                append_user_owner(channel_id, flockr_owner_u_id)
    ####

    rem_user_owner(channel_id, u_id)

    return {
        'is_success': True
    }


#################################################################################
# Validation functions

# Validates the active token
def validate_token(token):
    return any(user.get('token') == token for user in data['users'])

# Validates the channel
def validate_channel(channel_id):
    return any(channel.get('channel_id') == channel_id for channel in data['channels'])

# Validates the user
def validate_user(u_id):
    return any(user.get('u_id') == u_id for user in data['users'])

# Returns the corresponding u_id from the active token
def token_to_u_id(token):
    for user in data['users']:
        if user['token'] == token:
            return {
                'u_id': user['u_id'],
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }

# Returns True if channel with channel_id is a private channel
def private_channel(channel_id):
    return any(channel['channel_id'] == channel_id and channel.get('is_public') is False for channel in data['channels'])

# Check if user exists within the channel
def exists_in_channel(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return any(user == u_id for user in channel['all_members'])

# Add data of user to channel for new users to a channel
def append_data(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['all_members'].append(u_id)

# Identifies if the user is an owner of a channel
def user_is_owner(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return any(user == u_id for user in channel['owner_members'])

# Add user data for new owner members of a channel
def append_user_owner(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['owner_members'].append(u_id)

# Remove the user data from owner members
def rem_user_owner(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for owners in channel['owner_members']:
                if owners == u_id:
                    channel['owner_members'].remove(owners)

# Remove user data from channel
def rem_user_member(channel_id, u_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for members in channel['all_members']:
                if members == u_id:
                    channel['all_members'].remove(members)

    # IF they are an owner they need to be cleared from owner_members
    rem_user_owner(channel_id, u_id)

# Identifies if the user corresponding to the active token is an owner of the channel
def is_token_owner(token, channel_id):      
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return any(token_to_u_id(token)['u_id'] == owner for owner in channel['owner_members'])

# Determine the number of owners in a channel
def size_owners(channel_id):
    owner_members = 0
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            owner_members = len(channel['owner_members'])
    return owner_members

# Determine if the authenticated user is the flockr owner
def is_token_flockr_owner(token):
    for user in data['users']:
        if user['token'] == token:
            return user['permissions'] == FLOCKR_OWNER

# Gets user object from u_id
def get_user_names(u_id):
    for user in data['users']:
        if user['u_id'] == u_id:
            return {
                'u_id': u_id,
                'name_first': user['name_first'],
                'name_last': user['name_last']
            }

# Returns a list of user objects
def get_user_details(u_ids):
    users = []
    for u_id in u_ids:
        users.append(get_user_names(u_id))
    return users
        
# Identifies if the start value is greater than the number of messages in a channel
def invalid_messages_start(channel_id, start):
    for channel in data['channels']:
        if channel_id == channel['channel_id']:
            if channel['message_count'] == start and start == 0:
                return False
            if channel['message_count'] <= start:
                return True
    return False
    
