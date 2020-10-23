import requests
import json 
from echo_http_test import url
import message
import pytest

@pytest.fixture
def  user_list():
    requests.delete(url + 'clear')
    
    payload = {"email":"person1@email.com", "password": "password", "name_first": "Person", "name_last": "One"}
    response1 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person2@email.com", "password": "password", "name_first": "Person", "name_last": "Two"}
    response2 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person3@email.com", "password": "password", "name_first": "Person", "name_last": "Three"}
    response3 = requests.post(url + "auth/register", json=payload)

    return {
        'user1': response1.json(),
        'user2': response2.json(),
        'user3': response3.json(),
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
