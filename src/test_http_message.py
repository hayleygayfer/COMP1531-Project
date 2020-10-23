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
        'u1_id': regResponse1.json(),
        'u2_id': regResponse2.json(),
        'u3_id': regResponse2.json(),
        'token1': Logresponse1.json(),
        'token2': Logresponse2.json(),
        'token3': Logresponse3.json(),
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
        'c_id_1': c_id_1,
        'c_id_2': c_id_2,
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

def test_remove_flocker_owner_but_not_owner(data):

def test_remove_request_user_member(data):

# INVALID CASES #
def test_message_no_longer_exists(data):

def test_not_users_message(data):

def test_user_not_owner(data):

# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(data):
    payload = {'token1': user_list['token1']['token'], 'c1_id': channel_list['c1_id']['channel_id'], 'message': "This message was sent by the owner of flocker"}
    response = requests.post(url + "message/send", json=payload)
    message_ID = response.json()
    assert response.status_code == 200
    
    payload = {'token1': user_list['token1']['token'], 'message_id': message_ID, 'message': "This is the new message we just changed it completely but same same hey"}
    response = requests.post(url + "message/edit", json=payload)
    assert response.status_code == 200


def test_edit_user_member(data):

# INVALID CASES #
def test_not_valid_user(data):

def test_edit_not_by_person_who_sent(data):

def test_empty_string (data):



