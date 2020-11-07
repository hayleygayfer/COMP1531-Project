from data import data
from error import InputError, AccessError
from channel import validate_token, validate_channel, exists_in_channel, token_to_u_id
from message import message_send
import threading
from datetime import datetime, timezone, timedelta

def activate_standup(channel_id, time_finish):
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup_finish'] = time_finish

def deactivate_standup(token, channel_id, message):
    message = ''
    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            channel['standup_finish'] = None
            message = channel['standup_message']

    message_send(token, channel_id, message)

def standup_start(token, channel_id, length):
    time_finish = (datetime.now() + timedelta(0, length)).timestamp()

    if validate_token(token) == False:
        raise InputError("invalid token")

    if validate_channel(channel_id) == False:
        raise InputError("invalid channel")

    if standup_active(token, channel_id)['is_active'] == True:
        raise InputError("standup already active")

    activate_standup(channel_id, time_finish)
    threading.Timer(length, deactivate_standup, [token, channel_id]).start()

    return {
        'time_finish': time_finish
    }

def standup_active(token, channel_id):
    if validate_token(token) == False:
        raise InputError("invalid token")

    if validate_channel(channel_id) == False:
        raise InputError("invalid channel")

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            if channel['standup_finish'] == None:
                is_active = False
                time_finish = None
            else:
                is_active = True
                time_finish = channel['standup_finish']

    return {
        'is_active': is_active,
        'time_finish': time_finish
    }

def standup_send(token, channel_id, message):
    if validate_token(token) == False:
        raise InputError("invalid token")

    if validate_channel(channel_id) == False:
        raise InputError("invalid channel")

    if standup_active(token, channel_id)['is_active'] == False:
        raise InputError("no active standup")

    if len(message) > 1000:
        raise InputError("message over 1000 characters")

    u_id = token_to_u_id(token)
    if exists_in_channel(channel_id, u_id) == False:
        raise InputError("user not in channel")

    for channel in data['channels']:
        if channel['channel_id'] == channel_id:
            handle = token_to_handle(token)
            channel['standup_message'] = f"{channel['standup_message']}\n{handle}: {message}"

    return {}

def token_to_handle(token):
    for user in data['users']:
        if user['token'] == token:
            return user['handle_str']
    return None
