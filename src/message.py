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

    # Edit the message
    do_edit(channel, message_id, message)
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

def find_channel(msg_id, channel_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') == msg_id:
                    return channel

def do_edit(channel, msg_id, new_msg):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            msg['message'] = new_msg

def do_remove(channel, msg_id):
    for msg in channel['messages']:
        if msg.get('message_id') == msg_id:
            channel['messages'].remove(msg)


def user_is_not_owner(u_id, owners):
    for p in owners:
        if p.get('u_id') == u_id:
            return False
    return True

def get_flockr_owner_id(u_id):
    if u_id == data['users'][0].get('u_id'):
        return True
    return False