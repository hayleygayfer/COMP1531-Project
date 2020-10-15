from data import data
from error import InputError, AccessError

def message_send(token, channel_id, message):
    '''Send a message from an authorised user to the channel specified by channel_id'''
    msg_id = generate_message_id(channel_id)

    append_msg_to_channel(channel_id, message, msg_id)

    return data

def message_remove(token, message_id):
    '''Given a message_id for a message, this message is removed from the channel'''
    return {
    }

def message_edit(token, message_id, message):
    '''Given a message_id for a message, update the existing message with the new message.
    
    The message is deleted if the message is an empty string
    '''
    return {
    }

#################################################################################
## HELPER FUNCTIONS ##
#################################################################################

# generate a message id based on the channel and the messages inside that channel
def validate_token(token):
    for user in data['users']:
        if user['token'] == user.get('token'):
            return True
    return False


def generate_message_id(channel_id):
    i = channel_id*10000 + 1
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            for msg in channel['messages']:
                if msg.get('message_id') != i:
                    break
                i += 1
    return i


def append_msg_to_channel(channel_id, msg_string, msg_id):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['messages'].append(
                {
                    'message': msg_string,
                    'message_id': msg_id
                }
            )



if __name__ == "__main__":
    print(message_send(1, 1, "hello"))