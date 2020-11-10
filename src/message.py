from datetime import datetime
from data import data
from error import InputError, AccessError

MAX_MSG_IN_CH = 10000

def message_send(token, channel_id, message):
    '''
    Sends a message from an authenticated user, to the channel.
    A mesage_id is generated which depends on the channel_id and the number of current messages in the channel.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (int): the token of the authenticated user who is sending the message
        2. channel_id (int): used to identify the channel
        3. message (string): the message being sent (cannot be of NoneType)

    Return:
        The generated message_id (int)

    An AccessError or InputError is raised when there are errors in the function call

    '''

    # check for valid token/channel
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    if not valid_channel(channel_id):
        raise InputError("Channel ID does not exist") 

    if not channel_member(u_id, channel_id):
        raise AccessError("User not in channel")
    
    # message length must be at most 1000 and at least 1 characters
    if len(message) > 1000:
        raise InputError(f"Message is {len(message) - 1000} characters too long")
    elif message == "":
        raise InputError("Message must contain at least 1 character")
    
    # Calculates current timestamp
    timestamp = datetime.timestamp(datetime.now())

    msg_id = generate_message_id(channel_id)
    append_msg_to_channel(channel_id, message, msg_id, u_id, timestamp)

    return {
        'message_id': msg_id
    }

def message_remove(token, message_id):
    '''
    An authenticated user of a channel, removes a message.
    All details corresponding to the message message_id are erased from the channel for everyone.
    To be accessed from a member of the channel corresponding to the message.

    Args:
        1. token (int): the token of the authenticated user who is deleting the message
        3. message_id (int): the message getting removed

    Return:
        A dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    # check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id) or message_not_found(channel_id, message_id):
        raise InputError("Message not found")

    # Only a channel owner or flockr owner can remove a message
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']
    flockr_owner_id = get_flockr_owner_id(u_id)
    if user_is_not_owner(u_id, owners) and u_id != flockr_owner_id:
        raise AccessError("You are not authorised to remove this message")

    # an owner cannot remove another owner's message unless it's your own
    for msg in channel['messages']:
        if msg.get('message_id') == message_id:
            msg_creator = msg['u_id']
    if not user_is_not_owner(msg_creator, owners) or msg_creator == flockr_owner_id:
        # trying to edit a channel/flockr owner's message
        if msg_creator != u_id:
            raise AccessError("You cannot remove another owner's message")

    # Remove the message
    do_remove(channel, message_id)
    return {
        'is_success': True
    }

def message_edit(token, message_id, message):
    '''
    An authenticated user from a channel, edits a message in a channel by modifying the message.
    The edited message corresponds to the message with id message_id, and is replaced.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (int): the token of the authenticated user who is editting the message
        2. message_id (int): used to identify the message to be edited
        3. message (string): the message is replaced with this string
            * an empty string will delete the message (see message_remove)

    Return:
        A dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    # check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id):
        raise InputError("Message not found")

    # Only a channel owner or flockr owner can remove a message
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']
    flockr_owner_id = get_flockr_owner_id(u_id)
    if user_is_not_owner(u_id, owners) and u_id != flockr_owner_id:
        raise AccessError("You are not authorised to edit this message")

    # an owner cannot edit another owner's message unless it's your own
    for msg in channel['messages']:
        if msg.get('message_id') == message_id:
            msg_creator = msg['u_id']
    if not user_is_not_owner(msg_creator, owners) or msg_creator == flockr_owner_id:
        # trying to edit a channel/flockr owner's message
        if msg_creator != u_id:
            raise AccessError("You cannot edit another owner's message")
    
    # delete if empty string else, edit
    if message == "":
        do_remove(channel, message_id)
    else:
        do_edit(channel, message_id, message)

    return {
        'is_success': True
    }

#################################################################################
## HELPER FUNCTIONS ##
#################################################################################

# Returns the user_id corresponding to the active token
def get_uid_from_token(token):
    for user in data['users']:
        if user.get('token') == token:
            return user['u_id']
    return None

# Determines if the channel is valid or not
def valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

# Determines if a user is a member of a channel
def channel_member(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member == u_id:
                    return True
    return False        

# Generate a message_id based on the channel and the messages inside that channel
def generate_message_id(channel_id):
    i = channel_id*MAX_MSG_IN_CH + 1
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') != i:
                    break
                i += 1
    return i

# Returns the channel_id corresponding to the message_id
def get_channel_id(message_id):
    return int(message_id/MAX_MSG_IN_CH)

# Determines if a message exists within the channel
def message_not_found(channel_id, msg_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    return False
    return True

# Adds a message to a channel along with other relevant details
def append_msg_to_channel(channel_id, msg_string, msg_id, u_id, time):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(
                {
                    'message': msg_string,
                    'message_id': msg_id,
                    'u_id': u_id,
                    'time_created': time
                }
            )
            channel['message_count'] += 1

# Returns the channel array corresponding to the message_id and channel_id
def find_channel(msg_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    return channel

# Modify a message string with a new message
def do_edit(channel, msg_id, new_msg):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            msg['message'] = new_msg

# Delete a message
def do_remove(channel, msg_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            channel['messages'].remove(msg)
            channel['message_count'] -= 1

# Identifies if a user is an owner of a channel
def user_is_not_owner(u_id, owners):
    for p in owners:
        if p == u_id:
            return False
    return True

# Returns the user_id corresponding to the owner of FlockR
def get_flockr_owner_id(u_id):
    if u_id == data['users'][0].get('u_id'):
        return True
    return False
