import pytest
from standup import standup_start, standup_active, standup_send
from auth import auth_register, auth_login
from channels import channels_create
from datetime import datetime, timedelta

from error import InputError, AccessError
from other import clear
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

def test_token_not_valid_start(state):
    invalid_token = 123

    with pytest.raises(InputError):
        standup_start(invalid_token, state['channel_id_1'], 20)

def test_length_equal_0(state):
    with pytest.raises(InputError):
        standup_start(state['token1'], state['channel_id_1'], 0)

def test_length_less_than_0(state):
    with pytest.raises(InputError):
        standup_start(state['token1'], state['channel_id_1'], -5)

# VALID CASES #
def test_standup_in_channel(state):
    time_finish = standup_start(state['token1'], state['channel_id_1'], 20)['time_finish']
    assert time_finish == (datetime.now() + timedelta(0, 20)).timestamp()
    # TODO: test that standup is active then inactive after 20s

def test_length_1(state):
    time_finish = standup_start(state['token1'], state['channel_id_1'], 1)['time_finish']
    assert time_finish == (datetime.now() + timedelta(0, 1)).timestamp()
    # TODO: sleep 1 second then test standup is not active

def test_length_long(state):
    time_finish = standup_start(state['token1'], state['channel_id_1'], 60)['time_finish']
    assert time_finish == (datetime.now() + timedelta(0, 60)).timestamp()
    # TODO: test that standup is active, then inactive after a minute

#### standup_active ####

# INVALID CASES #
def test_channel_id_invalid_active(state):
    invalid_ch_id = 123

    with pytest.raises(InputError):
        standup_active(state['token1'], invalid_ch_id)

def test_invalid_token_active(state):
    invalid_token = 123

    with pytest.raises(InputError):
        standup_active(invalid_token, state['channel_id_1'])

# VALID CASES #
def test_standup_active(state):
    standup_start(state['token1'], state['channel_id_1'], 30)
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == True

def test_standup_inactive(state):
    assert standup_active(state['token1'], state['channel_id_1'])['is_active'] == False

def test_standup_time_finish(state):
    standup_start(state['token1'], state['channel_id_1'], 30)
    assert standup_active(state['token1'], state['channel_id_1'])['time_finish'] == (datetime.now() + timedelta(0, 30)).timestamp()
    standup_start(state['token2'], state['channel_id_2'], 150)
    assert standup_active(state['token2'], state['channel_id_2'])['time_finish'] == (datetime.now() + timedelta(0, 150)).timestamp()


#### standup_send ####

# INVALID CASES #
def test_invalid_channel_id_send(state):
    invalid_ch_id = 123
    message = "message"

    standup_start(state['token1'], state['channel_id_1'], 60)

    with pytest.raises(InputError):
        standup_send(state['token1'], invalid_ch_id, message)

def test_invalid_token_send(state):
    invalid_token = 123
    message = "message"

    standup_start(state['token1'], state['channel_id_1'], 60)

    with pytest.raises(InputError):
        standup_send(invalid_token, state['channel_id_1'], message)

def test_message_over_1000_char(state):
    invalid_message = 1000*'a'

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
    #TODO: write test
    pass

def test_message_1000_char(state):
    #TODO: write test
    pass

def test_standup_active_send(state):
    #TODO: write test
    pass