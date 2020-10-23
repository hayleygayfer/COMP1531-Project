import requests
import json 
from echo_http_test import url
import message
import channel
import pytest

@pytest.fixture
def  user_list():
    requests.delete(url + 'clear')
    
    payload = {"email":"person1@email.com", "password": "password", "name_first": "Person", "name_last": "One"}
    regResponse1 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person1@email.com", "password": "password"}
    Logresponse1 = requests.post(url + "auth/login", json=payload)


    payload = {"email":"person2@email.com", "password": "password", "name_first": "Person", "name_last": "Two"}
    regResponse2 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person2@email.com", "password": "password"}
    Logresponse2 = requests.post(url + "auth/login", json=payload)


    payload = {"email":"person3@email.com", "password": "password", "name_first": "Person", "name_last": "Three"}
    regResponse3 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person3@email.com", "password": "password"}
    Logresponse3 = requests.post(url + "auth/login", json=payload)

    return {
        'u1_id': regResponse1.json()['u_id']],
        'u2_id': regResponse2.json()['u_id'],
        'u3_id': regResponse2.json()['u_id'],
        'token1': Logresponse1.json()['token'],
        'token2': Logresponse2.json()['token'],
        'token3': Logresponse3.json()['token'],
    }

@pytest.fixture
def channel_list(user_list):
    # person one creates a channel
    payload = {"token": user_list['user1']['token'], "name": "channel_1", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    c_id_1 = response.json()

    # person two creates a channel
    payload = {"token": user_list['user2']['token'], "name": "channel_2", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    c_id_2 = response.json()

    return {
        'c_id_1': c_id_1['channel_id'],
        'c_id_2': c_id_2['channel_id'],
    }

# test message_send #
"""
message_send(token, channel_id, message)
OUTPUT: { message_id }
"""

#### MESSAGE 0 IS THE MOST RECENT MESSAGE IN THE CHANNEL ####

# VALID CASES #

def test_message_user_owner_http(url, user_list, channel_list):
    payload = {"token1": user_list['token1']['token'], }

def test_message_user_member(data):

def test_message_non_alpha_characters(data):

# INVALID CASES #
def test_message_greater_than_1000(data):

def test_user_not_in_channel(data):

def test_user_logged_out(data):

def test_empty_message(data):

# test message_remove #
"""
message_remove(token, message_id)
OUTPUT: {}
"""

# VALID CASES #
def test_remove_user_owner(data):
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This message will be removed"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message
    payload = {'token1': user_list['token1'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 200

def test_remove_flocker_owner_but_not_owner(data):
    # Join channel
    payload = {'token1': user_list['token1'], 'c2_id': channel_list['c2_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Send message
    payload = {'token1': user_list['token1'], 'c2_id': channel_list['c2_id'], 'message': "This message will be removed"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message
    payload = {'token1': user_list['token1'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 200


def test_remove_request_user_member(data):
     # Send message
    payload = {'token2': user_list['token2'], 'c2_id': channel_list['c2_id'], 'message': "This message will be removed"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message
    payload = {'token2': user_list['token2'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 200

# INVALID CASES #
def test_message_no_longer_exists(data):
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This is a valid message"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message
    payload = {'token1': user_list['token1'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 200
    # Remove message again
    payload = {'token1': user_list['token1'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 404

def test_not_users_message(data):
    # Join channel
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Add owner
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'u2_id': user_list['u2_id']}
    response = requests.post(url + "channel/addowner", json=payload)
    assert response.status_code == 200
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by one of the owners of the channel"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message 
    payload = {'token2': user_list['token2'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 404

def test_user_not_owner(data):
    # Join channel
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Send message
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by one of the members of the channel"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Remove message 
    payload = {'token2': user_list['token2'], 'message_id': message_ID}
    response = response.post(url + "message/remove", json=payload)
    assert response.status_code == 404
    
# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(data):
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by the owner of flocker"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Edit message 
    payload = {'token1': user_list['token1'], 'message_id': message_ID, 'message': "This is the new message we just changed it completely but same same hey"}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 200


def test_edit_user_member(data):
    # Join channel
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Add owner
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'u1_id': user_list['u1_id']}
    response = requests.post(url + "channel/addowner", json=payload)
    assert response.status_code == 200
    # Send message
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by an owner of this channel"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Edit message
    payload = {'token2': user_list['token2'], 'message_id': message_ID, 'message': "This message should be able to be edited"}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 200

# INVALID CASES #
def test_not_valid_user(data):
    # Join channel
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Send message
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by not an owner"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Edit message
    payload = {'token2': user_list['token2'], 'message_id': message_ID, 'message': "This message should not be able to be edited"}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 400

def test_edit_not_by_person_who_sent(data):
    # Join channel
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id']}
    response = requests.post(url + "channel/join", json=payload)
    assert response.status_code == 200
    # Add owner
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'u2_id': user_list['u2_id']}
    response = requests.post(url + "channel/addowner", json=payload)
    assert response.status_code == 200
    # Edit message
    payload = {'token2': user_list['token2'], 'c1_id': channel_list['c1_id'], 'message': "This message was sent by an owner of this channel"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    # Edit message again
    payload = {'token1': user_list['token1'], 'message_id': message_ID, 'message': "This message should not be able to be edited"}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 400

def test_empty_string (data):
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This is the first message sent"}
    response = requests.post(url + "message/send", json=payload)
    message_ID1 = response.json()
    assert response.status_code == 200
    # Send message
    payload = {'token1': user_list['token1'], 'c1_id': channel_list['c1_id'], 'message': "This is the second message sent"}
    response = requests.post(url + "message/send", json=payload)
    message_ID2 = response.json()
    assert response.status_code == 200
    # Edit message
    payload = {'token1': user_list['token1'], 'message_id': message_ID2, 'message': ""}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 200
    # Get message from channel messages
    payload = {'token1': user_list['token1'], 'message_id': message_ID2, 'start': 0}
    response = requests.post(url + "channel/message", json=payload)
    messages = response.json()['messages']
    message_id_at_index_zero = message[0]['message_id']
    assert message_ID1 == message_id_at_index_zero





