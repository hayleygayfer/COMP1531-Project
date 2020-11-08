import requests
import json 
from echo_http_test import url
import pytest
from time import sleep

## Fixtures
@pytest.fixture
def state(url):
    requests.delete(url + 'clear')

    # user 1
    payload = {"email":"person1@email.com", "password": "password", "name_first": "Person", "name_last": "One"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email": "person1@email.com", "password": "password"}
    response1 = requests.post(url + "auth/login", json=payload)
    u_id1 = response1.json()['u_id']
    token1 = response1.json()['token']

    # user 2
    payload = {"email":"person2@email.com", "password": "password", "name_first": "Person", "name_last": "Two"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email": "person2@email.com", "password": "password"}
    response2 = requests.post(url + "auth/login", json=payload)
    u_id2 = response2.json()['u_id']
    token2 = response2.json()['token']

    # user 1 creates channel 1
    payload = {"token": token1, "name": "channel_1", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    c_id_1 = response.json()['channel_id']

    # user 2 creates channel 2
    payload = {"token": token2, "name": "channel_2", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    c_id_2 = response.json()['channel_id']

    return {
        'u_id1': u_id1,
        'token1': token1,
        'u_id2': u_id2,
        'token2': token2,
        'c_id_1': c_id_1,
        'c_id_2': c_id_2
    }

######### standup_start #########

# INVALID CASES #
def test_channel_id_not_valid_start_http(url, state):
    invalid_ch_id = 123
    payload = {'token': state['token1'], 'channel_id': invalid_ch_id, 'length': 5}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 400

def test_standup_already_active_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 20}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 400

def test_token_not_valid_start_http(url, state):
    invalid_token = 123
    payload = {'token': invalid_token, 'channel_id': state['c_id_1'], 'length': 5}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 400

def test_length_equal_0_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 0}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 400

def test_length_less_than_0_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': -1}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 400

# VALID CASES #
def test_standup_in_channel_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 20}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == True

def test_length_1_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 1}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200
    sleep(1)
    
    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == False

def test_length_long_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 60}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200
    
    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == True

######### standup_active #########

# INVALID CASES #
def test_channel_id_invalid_active_http(url, state):
    invalid_ch_id = 123
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 20}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': invalid_ch_id}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 400

def test_invalid_token_active_http(url, state):
    invalid_token = 123
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 20}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': invalid_token, 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 400

# VALID CASES #
def test_standup_active_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 20}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == True

def test_standup_inactive_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == False

def test_standup_time_finish_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token2'], 'channel_id': state['c_id_2'], 'length': 150}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == True

    payload = {'token': state['token2'], 'channel_id': state['c_id_2']}
    response = requests.get(url + "standup/active", json=payload)
    assert response.status_code == 200
    assert response.json()['is_active'] == True

######### standup_send #########

# INVALID CASES #
def test_invalid_channel_id_send_http(url, state):
    invalid_ch_id = 123
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': invalid_ch_id, 'message': 'hello'}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 400

def test_invalid_token_send_http(url, state):
    invalid_token = 123
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': invalid_token, 'channel_id': state['c_id_1'], 'message': 'hello'}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 400

def test_message_over_1000_char_http(url, state):
    message = 1001*'a'
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'message': message}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 400

def test_standup_not_active_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'message': 'hello'}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 400

def test_user_not_in_channel_http(url, state):
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token2'], 'channel_id': state['c_id_1'], 'message': 'hello'}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 400

# VALID CASES #
def test_message_empty_http(url, state):
    message = ''
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'message': message}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 200

def test_message_1000_char_http(url, state):
    message = 1000*'a'
    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'message': message}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 200

def test_standup_active_send_two_people_http(url, state):
    message = 'hello'

    payload = {"token": state['token1'], "channel_id": state['c_id_1'], "u_id": state['u_id2']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'length': 30}
    response = requests.post(url + "standup/start", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token1'], 'channel_id': state['c_id_1'], 'message': message}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 200

    payload = {'token': state['token2'], 'channel_id': state['c_id_1'], 'message': message}
    response = requests.post(url + "standup/send", json=payload)
    assert response.status_code == 200






