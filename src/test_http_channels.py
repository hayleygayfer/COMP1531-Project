import json 
import requests
from echo_http_test import url
import pytest

#### login and channel creation fixtures ####
@pytest.fixture
def user_list(url):
    requests.delete(url + 'clear')
    
    payload = {"email":"person1@email.com", "password": "password", "name_first": "Person", "name_last": "One"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email": "person1@email.com", "password": "password"}
    response1 = requests.post(url + "auth/login", json=payload)

    payload = {"email":"person2@email.com", "password": "password", "name_first": "Person", "name_last": "Two"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email": "person2@email.com", "password": "password"}
    response2 = requests.post(url + "auth/login", json=payload)

    payload = {"email":"person3@email.com", "password": "password", "name_first": "Person", "name_last": "Three"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email": "person3@email.com", "password": "password"}
    response3 = requests.post(url + "auth/login", json=payload)

    return {
        'user1': response1.json(),
        'user2': response2.json(),
        'user3': response3.json(),
    }

@pytest.fixture
def channel_list(url, user_list):
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

### channels_list ###

# VALID CASES #
def test_no_channels_http(url, user_list):
    # get channels list according to person one when none have been created
    payload = {"token": user_list['user1']['token']}
    response = requests.get(url + "channels/list", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == []

def test_user_in_no_channels_http(url, user_list):
    # get channels list according to person two when person one has created a channel and has invited person three
    payload = {"token": user_list['user1']['token'], "name": "channel_1", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 200
    c_id = response.json()
 
    # person one invites person 3
    payload = {"token": user_list['user1']['token'], "channel_id": c_id['channel_id'], "u_id": user_list['user3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person two accesses their channels list
    payload = {"token": user_list['user2']['token']}
    response = requests.get(url + "channels/list", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == []

def test_user_is_in_all_channels_http(url, user_list, channel_list):
    # person one invites person three to channel one
    payload = {"token": user_list['user1']['token'], "channel_id": channel_list['c_id_1'], "u_id": user_list['user3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person two invites person three to channel two
    payload = {"token": user_list['user2']['token'], "channel_id": channel_list['c_id_2'], "u_id": user_list['user3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person one invites person two to channel one
    payload = {"token": user_list['user1']['token'], "channel_id": channel_list['c_id_1'], "u_id": user_list['user2']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person three accesses their channels list
    payload = {"token": user_list['user3']['token']}
    response = requests.get(url + "channels/list", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == [
        {
            'channel_id': channel_list['c_id_1'], 
            'name': "channel_1", 
            'all_members': [user_list['user1']['u_id'], user_list['user3']['u_id'], user_list['user2']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
        {
            'channel_id': channel_list['c_id_2'], 
            'name': "channel_2", 
            'all_members': [user_list['user2']['u_id'], user_list['user3']['u_id']],
            'owner_members': [user_list['user2']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
    ]

def test_user_is_in_some_channels_http(url, user_list, channel_list):
    # person one invites person two to channel one
    payload = {"token": user_list['user1']['token'], "channel_id": channel_list['c_id_1'], "u_id": user_list['user2']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person one invites person three to channel one
    payload = {"token": user_list['user1']['token'], "channel_id": channel_list['c_id_1'], "u_id": user_list['user3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # person three accesses their channel list
    payload = {"token": user_list['user3']['token']}
    response = requests.get(url + "channels/list", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == [
        {
            'channel_id': channel_list['c_id_1'], 
            'name': "channel_1", 
            'all_members': [user_list['user1']['u_id'], user_list['user2']['u_id'], user_list['user3']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
    ]

    # user2 and user3 will not see the same list
    payload = {"token": user_list['user2']['token']}
    response2 = requests.get(url + "channels/list", params=payload)
    assert response2.status_code == 200
    assert response.json() != response2.json()
    # user1 and user3 will see the same list
    payload = {"token": user_list['user1']['token']}
    response2 = requests.get(url + "channels/list", params=payload)
    assert response2.status_code == 200
    assert response.json() == response2.json()

### channels_listall ###

# VALID CASES #
def test_no_total_channels_http(url, user_list):
    # person one accesses all channels list when none have been created
    payload = {"token": user_list['user1']['token']}
    response = requests.get(url + "channels/listall", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == []


def test_total_channels_http(url, user_list, channel_list):
    # person one accesses all channels list when two have been created
    payload = {"token": user_list['user1']['token']}
    response = requests.get(url + "channels/listall", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == [
        {
            'channel_id': channel_list['c_id_1'], 
            'name': "channel_1", 
            'all_members': [user_list['user1']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
        {
            'channel_id': channel_list['c_id_2'], 
            'name': "channel_2", 
            'all_members': [user_list['user2']['u_id']],
            'owner_members': [user_list['user2']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
    ]


def test_total_channels_not_created_by_user_http(url, user_list, channel_list):
    # person three accessed all channels list when none are created by them
    payload = {"token": user_list['user3']['token']}
    response = requests.get(url + "channels/listall", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == [
        {
            'channel_id': channel_list['c_id_1'], 
            'name': "channel_1", 
            'all_members': [user_list['user1']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
        {
            'channel_id': channel_list['c_id_2'], 
            'name': "channel_2", 
            'all_members': [user_list['user2']['u_id']],
            'owner_members': [user_list['user2']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
    ]


### channels_create ###

# EXCEPTIONS #
def test_name_over_20_characters_http(url, user_list):
    # person one creates a channel with a name over 20 character
    payload = {"token": user_list['user1']['token'], "name": "channels____________1", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 400


# VALID CASES #

def test_name_1_or_20_characters_http(url, user_list):
    # person one creates a channel with a name 20 characters long
    payload = {"token": user_list['user1']['token'], "name": "channels___________1", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 200

    # person one creates a channel with a name 1 character long
    payload = {"token": user_list['user1']['token'], "name": "2", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 200

def test_public_private_http(url, user_list):
    # person one creates a private channel
    payload = {"token": user_list['user1']['token'], "name": "channel_private", "is_public": False}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 200
    c_id_private = response.json()

    # person one creates a public channel
    payload = {"token": user_list['user1']['token'], "name": "channel_public", "is_public": True}
    response = requests.post(url + "channels/create", json=payload)
    assert response.status_code == 200
    c_id_public = response.json()

    # person one tries to acccess all channels list
    payload = {"token": user_list['user1']['token']}
    response = requests.get(url + "channels/listall", params=payload)
    assert response.status_code == 200
    assert response.json()['channels'] == [
        {
            'channel_id': c_id_private['channel_id'], 
            'name': "channel_private", 
            'all_members': [user_list['user1']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': False,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
        {
            'channel_id': c_id_public['channel_id'], 
            'name': "channel_public", 
            'all_members': [user_list['user1']['u_id']],
            'owner_members': [user_list['user1']['u_id']],
            'is_public': True,
            'messages': [],
            'message_count': 0,
            'standup_finish': None,
            'standup_message': ''
        },
    ]


