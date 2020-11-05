from data import data
from error import InputError, AccessError

def standup_start(token, channel_id, length):

    return {
        'time_finish': 12345
    }

def standup_active(token, channel_id):

    return {
        'is_active': True/False,
        'time_finish': 12345
    }

def standup_send(token, channel_id, message):

    return {}
