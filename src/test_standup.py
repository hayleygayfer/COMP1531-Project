import pytest
from standup import standup_start, standup_active, standup_send
from auth import auth_register, auth_login
from channels import channels_create
from channel import channel_invite
from datetime import datetime, timedelta
from time import sleep
import threading

from error import InputError, AccessError
from other import clear, search
from data import data

## Fixtures
@pytest.fixture
def state():
    clear()

    auth_register("person1@unsw.com", "pass1234", "Personone", "One")
    user1 = auth_login("person1@unsw.com", "pass1234")
    auth_register("person2@unsw.com", "pass1234", "Persontwo", "Two")
    user2 = auth_login("person2@unsw.com", "pass1234")

    channel1_id = channels_create(user1['token'], "ch_1", True)['channel_id']
    channel2_id = channels_create(user2['token'], "ch_2", True)['channel_id']

    return {
        'token1': user1['token'],
        'u_id1': user1['u_id'],
        'token2': user2['token'],
        'u_id2': user2['u_id'],
        'channel_id_1': channel1_id,
        'channel_id_2': channel2_id,
    }

## standup_active thread ##
def is_inactive(token, ch_id):
    assert standup_active(token, ch_id)['is_active'] == False


#### standup_start ####

# INVALID CASES #
def test_channel_id_not_valid_start(state):
    invalid_ch_id = 123

    with pytest.raises(InputError):
        standup_start(state['token1'], invalid_ch_id, 5)

def test_standup_already_active(state):
    standup_start(state['token1'], state['channel_id_1'], 20)

    with pytest.raises(InputError):
        standup_start(state['token1'], state['channel_id_1'], 20)

def test_length_equal_0(state):
    with pytest.raises(InputError):
        standup_start(state['token1'], state['channel_id_1'], 0)

def test_length_less_than_0(state):
    with pytest.raises(InputError):
        standup_start(state['token1'], state['channel_id_1'], -5)

# VALID CASES #
def test_standup_in_channel(state):
    standup_start(state['token1'], state['channel_id_1'], 20)['time_finish']
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == True
    #threading.Timer(20, is_inactive, [state['token1'], state['channel_id_1']]).start()

def test_length_1(state):
    standup_start(state['token1'], state['channel_id_1'], 1)['time_finish']
    #threading.Timer(1, is_inactive, [state['token1'], state['channel_id_1']]).start()

def test_length_long(state):
    standup_start(state['token1'], state['channel_id_1'], 60)['time_finish']
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == True
    #threading.Timer(60, is_inactive, [state['token1'], state['channel_id_1']]).start()

#### standup_active ####

# INVALID CASES #
def test_channel_id_invalid_active(state):
    invalid_ch_id = 123

    with pytest.raises(InputError):
        standup_active(state['token1'], invalid_ch_id)

# VALID CASES #
def test_standup_active(state):
    standup_start(state['token1'], state['channel_id_1'], 30)
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == True
    #threading.Timer(30, is_inactive, [state['token1'], state['channel_id_1']]).start()

def test_standup_inactive(state):
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == False

def test_standup_time_finish(state):
    standup_start(state['token1'], state['channel_id_1'], 30)
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == True
    standup_start(state['token2'], state['channel_id_2'], 150)
    assert standup_active(state['token2'], state['channel_id_2'])['is_active'] == True
    #threading.Timer(30, is_inactive, [state['token1'], state['channel_id_1']]).start()
    #threading.Timer(150, is_inactive, [state['token2'], state['channel_id_2']]).start()

#### standup_send ####

# INVALID CASES #
def test_invalid_channel_id_send(state):
    invalid_ch_id = 123
    message = "message"

    standup_start(state['token1'], state['channel_id_1'], 60)

    with pytest.raises(InputError):
        standup_send(state['token1'], invalid_ch_id, message)

def test_message_over_1000_char(state):
    invalid_message = 1001*'a'

    standup_start(state['token1'], state['channel_id_1'], 60)

    with pytest.raises(InputError):
        standup_send(state['token1'], state['channel_id_1'], invalid_message)

def test_standup_not_active(state):
    message = "message"

    with pytest.raises(InputError):
        standup_send(state['token1'], state['channel_id_1'], message)

def test_user_not_in_channel(state):
    message = "message"

    standup_start(state['token1'], state['channel_id_1'], 60)

    with pytest.raises(InputError):
        standup_send(state['token2'], state['channel_id_1'], message)

# VALID CASES #
def test_message_empty(state):
    message = ''
    standup_start(state['token1'], state['channel_id_1'], 2)
    standup_send(state['token1'], state['channel_id_1'], message)
    sleep(1)
    messages = search(state['token1'], 'persononeone:')
    assert messages != []

def test_message_1000_char(state):
    message = 1000*'a'

    standup_start(state['token1'], state['channel_id_1'], 2)
    standup_send(state['token1'], state['channel_id_1'], message)
    sleep(1)
    messages = search(state['token1'], 'persononeone:')
    assert messages != []

def test_standup_active_send_two_people(state):
    message = 'hello'
    channel_invite(state['token1'], state['channel_id_1'], state['u_id2'])

    standup_start(state['token1'], state['channel_id_1'], 2)
    standup_send(state['token1'], state['channel_id_1'], message)
    standup_send(state['token2'], state['channel_id_1'], message)
    sleep(1)
    messages1 = search(state['token1'], 'persononeone:')['messages']
    messages2 = search(state['token1'], 'persontwotwo:')['messages']

    assert messages1 != []
    assert messages2 != []
    assert data['channels'][0]['messages'][0]['message'] == "persononeone: hello\npersontwotwo: hello"