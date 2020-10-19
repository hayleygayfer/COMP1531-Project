from data import data
from error import InputError, AccessError

MAX_MSG_IN_CH = 10000

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
    if not valid_channel(channel_id):
        raise InputError("Message not found")

    # Remove the message
    find_and_remove(message_id, channel_id)


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

    # Edit the message
    find_and_edit(message_id, channel_id, message)

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

def find_and_remove(msg_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    channel['messages'].remove(msg)

def find_and_edit(msg_id, channel_id, new_msg):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    msg['message'] == new_msg

def is_flockr_owner(token):
    if token == data['users'][0].get('token'):
        return True
    return False