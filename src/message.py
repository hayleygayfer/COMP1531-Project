from datetime import datetime, timedelta
from data import data
from error import InputError, AccessError

import threading
import time

MAX_MSG_IN_CH = 10000
REACT_VALID = 1
FLOCKR_OWNER = 1

def message_send(token, channel_id, message):
    '''
    Sends a message from an authenticated user, to the channel.
    A mesage_id is generated which depends on the channel_id and the number of current messages in the channel.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is sending the message
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
    timestamp = int(datetime.timestamp(datetime.now()))
    print(timestamp)

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
        1. token (str): the token of the authenticated user who is deleting the message
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

    # Only a channel owner or a flockr owner can remove a message
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']

    if user_is_not_owner(u_id, owners) and not is_flockr_owner(u_id):
        raise AccessError("You are not authorised to remove this message")

    # an owner cannot remove another owner's message unless it's your own
    for msg in channel['messages']:
        if msg.get('message_id') == message_id:
            msg_creator = msg['u_id']
    if not user_is_not_owner(msg_creator, owners) or is_flockr_owner(msg_creator):
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
        1. token (str): the token of the authenticated user who is editting the message
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

    # Only a channel owner or a flockr owner can remove a message
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']

    if user_is_not_owner(u_id, owners) and not is_flockr_owner(u_id):
        raise AccessError("You are not authorised to edit this message")

    # an owner cannot edit another owner's message unless it's your own
    for msg in channel['messages']:
        if msg.get('message_id') == message_id:
            msg_creator = msg['u_id']
    if not user_is_not_owner(msg_creator, owners) or is_flockr_owner(msg_creator):
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


## ITERATION 3
def message_sendlater(token, channel_id, message, time_sent):
    '''
    An authenticated user from a channel, can send a message in the future within a channel.
    The edited message corresponds to the message with id message_id, and is replaced.
    To be accessed from a member of the channel with id channel_id.

    Args:
        1. token (str): the token of the authenticated user who is editting the message
        2. channel_id (int): used to identify the channel
        3. message (string): the message being sent (cannot be of NoneType)
        4. time_sent (integer- UNIX timestamp): the time in the future where the message is sent

    Return:
        The generated message_id (int)

    An AccessError or InputError is raised when there are errors in the function call

    '''

    # Check for valid token
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
    timestamp = int(datetime.timestamp(datetime.now()))

    # Time_sent must be in the future
    if timestamp >= time_sent:
        raise InputError(f"Time: is in the past or the current time.")

    msg_id = generate_message_id(channel_id)

    # Run the rest of the program, while waiting the required time delta for appending message to channel.
    time_delta = float(time_sent - timestamp)

    t = threading.Timer(time_delta, append_msg_to_channel, [channel_id, message, msg_id, u_id, time_sent])
    t.daemon = True
    t.start()

    return {
        'message_id': msg_id
    }

def message_react(token, message_id, react_id):
    '''
    Any user in the channel can react to a message in the current channel.
    Reacting to a message displays a certain react.

    Args:
        1. token (str): the token of the authenticated user who is reacting to the message
        2. message_id (int): used to identify the message to be reacted
        3. react_id (int): used to identify the type of react, only valid react is 1 

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''
    # Check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id):
        raise InputError("Message not found")

    if not channel_member(u_id, channel_id):
        raise InputError("You are not a member of this channel")
    
    # Get channel
    channel = find_channel(message_id, channel_id)

    # Check that react is valid - this is specific to front end 
    if react_id != REACT_VALID:
        raise InputError("Invalid react")

    # Check if user has already reacted to message 
    if alreadyReacted(u_id, channel, message_id, react_id):
        raise InputError("You have already reacted to this message")

    doReact(u_id, channel, message_id, react_id)

    return {}

def message_unreact(token, message_id, react_id):
    '''
    A member of a channel can unreacts a particular message in the channel.
    Unreacting a message removes the react on the message on the frontend.

    Args:
        1. token (str): the token of the authenticated user who is reacting to the message
        2. message_id (int): used to identify the message to be reacted
        3. react_id (int): used to identify the type of react, only valid react is 1 

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''
    # Check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id):
        raise InputError("Message not found")

    if not channel_member(u_id, channel_id):
        raise InputError("You are not a member of this channel")
    
    # Get channel
    channel = find_channel(message_id, channel_id)

    # Check that react is valid - this is specific to front end 
    if react_id != REACT_VALID:
        raise InputError("Invalid react")

    if noReact(u_id, channel, message_id, react_id):
        raise InputError("You have not reacted to this message so cannot remove react")

    doUnreact(u_id, channel, message_id, react_id)

    return {}
    

def message_pin(token, message_id):
    '''
    A channel owner (or a flockr owner), pins a particular message in the channel.
    Marking a message as pinned gives the message display priority on the frontend.

    Args:
        1. token (str): the token of the authenticated user who is pinning the message
        2. message_id (int): used to identify the message to be pinned

    Return:
        An empty dictionary to indicate that the function call was successful

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

    if not channel_member(u_id, channel_id):
        raise AccessError("You are not a member of this channel")

    # User must be a channel/flockr owner
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']

    if user_is_not_owner(u_id, owners) and not is_flockr_owner(u_id):
        raise AccessError("You must be an owner to pin this message")
    

    # Pin the message
    doPin(channel, message_id)
    return {}


def message_unpin(token, message_id):
    '''
    A channel owner (or a flockr owner), unpins a particular message in the channel.
    Unpinning a pinned message removes the pinned status of the message on the frontend.

    Args:
        1. token (str): the token of the authenticated user who is unpinning the message
        2. message_id (int): used to identify the message to be unpinned

    Return:
        An empty dictionary to indicate that the function call was successful

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

    if not channel_member(u_id, channel_id):
        raise AccessError("You are not a member of this channel")

    # User must be a channel/flockr owner
    channel = find_channel(message_id, channel_id)
    owners = channel['owner_members']

    if user_is_not_owner(u_id, owners) and not is_flockr_owner(u_id):
        raise AccessError("You must be an owner to pin this message")
    

    # Unpin the message
    doUnpin(channel, message_id)
    return {}


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
    return any(channel['channel_id'] == channel_id for channel in data['channels'])

# Determines if a user is a member of a channel
def channel_member(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return any(member == u_id for member in channel['all_members'])       

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
            return not any(msg.get('message_id') == msg_id for msg in channel['messages'])

# Adds a message to a channel along with other relevant details
def append_msg_to_channel(channel_id, msg_string, msg_id, u_id, time):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(
                {
                    'message': msg_string,
                    'message_id': msg_id,
                    'u_id': u_id,
                    'time_created': time,
                    'reacts': [{
                        'react_id': 1,
                        'u_ids': [],
                        'is_this_user_reacted': False
                    }],
                    'is_pinned': False
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
    return not any(person == u_id for person in owners)

def is_flockr_owner(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return user['permissions'] == FLOCKR_OWNER

# Pin the message to channel 
def doPin(channel, msg_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            if msg['is_pinned']:
                raise InputError(f'This message is already pinned')

            msg['is_pinned'] = True

# Unpin the message to the channel
def doUnpin(channel, msg_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            if not msg['is_pinned']:
                raise InputError(f'This message is not pinned')

            msg['is_pinned'] = False

# Checks if the user has already reacted to the message
def alreadyReacted(u_id, channel, msg_id, react_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            return any(user == u_id for user in msg['reacts'][0]['u_ids'])

# react to a message in the channel
def doReact (u_id, channel, msg_id, react_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            if alreadyReacted(u_id, channel, msg_id, react_id) == True:
                raise InputError(f'This message is already reacted by this user')
            msg['reacts'][0]['u_ids'].append(u_id)

# Returns True if the message corresponding to msg_id does not have any reacts (empty list)
def noReact(u_id, channel, msg_id, react_id):
    return any(msg.get('message_id') == msg_id and msg['reacts'][0]['u_ids'] == [] for msg in channel['messages'])

# removes react from message in channel
def doUnreact(u_id, channel, msg_id, react_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id: 
            for user in msg['reacts'][0]['u_ids']:
                if user == u_id:
                    msg['reacts'][0]['u_ids'].remove(u_id)
            
            if msg['reacts'][0]['is_this_user_reacted'] == True:
                msg['reacts'][0]['is_this_user_reacted'] == False
