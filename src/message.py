from data import data
from error import InputError, AccessError

MAX_MSG_IN_CH = 10000
EDIT = 1
REMOVE = 2

def message_send(token, channel_id, message):
    '''Send a message from an authorised user to the channel specified by channel_id'''
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
    
    # TODO: Calculate current timestamp
    timestamp = 1582426789

    msg_id = generate_message_id(channel_id)
    append_msg_to_channel(channel_id, message, msg_id, u_id, timestamp)

    return msg_id

def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''
    # check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id) or message_not_found(channel_id, message_id):
        raise InputError("Message not found")

    # Only the user or flockr owner can remove a message
    msg_sender_id = find(message_id, channel_id, None, 0)
    flockr_owner_id = get_flockr_owner_id(u_id)
    if msg_sender_id != u_id and msg_sender_id != flockr_owner_id:
        raise AccessError("You cannot remove this message")


    # Remove the message
    find(message_id, channel_id, None, REMOVE)
    return {
        'is_success': True
    }

def message_edit(token, message_id, message):
    '''Given a message_id for a message, update the existing message with the new message.
    
    The message is deleted if the message is an empty string
    '''
    # check for valid token
    u_id = get_uid_from_token(token)
    if u_id == None:
        raise AccessError("Invalid token")

    # Find message
    channel_id = get_channel_id(message_id)
    if not valid_channel(channel_id):
        raise InputError("Message not found")

    # Only the user or flockr owner can remove a message
    msg_sender_id = find(message_id, channel_id, None, 0)
    flockr_owner_id = get_flockr_owner_id(u_id)
    if msg_sender_id != u_id and msg_sender_id != flockr_owner_id:
        raise AccessError("You cannot edit this message")

    # Edit the message
    find(message_id, channel_id, message, EDIT)
    return {
        'is_success': True
    }

#################################################################################
## HELPER FUNCTIONS ##
#################################################################################

def get_uid_from_token(token):
    for user in data['users']:
        if user.get('token') == token:
            return user['u_id']
    return None

def valid_channel(channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            return True
    return False

def channel_member(u_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for member in channel['all_members']:
                if member['u_id'] == u_id:
                    return True
    return False        

# generate a message id based on the channel and the messages inside that channel
def generate_message_id(channel_id):
    i = channel_id*MAX_MSG_IN_CH + 1
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') != i:
                    break
                i += 1
    return i

def get_channel_id(message_id):
    return int(message_id/MAX_MSG_IN_CH)

def message_not_found(channel_id, msg_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    return False
    return True

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

def find(msg_id, channel_id, new_msg, mode):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    # get mode to determine what to do
                    if mode == EDIT:
                        msg['message'] == new_msg
                    elif mode == REMOVE:
                        channel['messages'].remove(msg)
                    else:
                        return msg['u_id']

def get_flockr_owner_id(u_id):
    if u_id == data['users'][0].get('u_id'):
        return True
    return False