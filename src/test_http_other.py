import requests
import json 
from echo_http_test import url
import pytest

ERROR = 400

@pytest.fixture
def userObject(url):
    requests.delete(url + 'clear')

    response1 = auth(url, "person1@email.com", "password", "Person", "One")
    response2 = auth(url, "person2@email.com", "password", "Person", "Two")

    response3 = channels_create(url, response1['token'], "Channel1", True)
    response4 = channels_create(url, response1['token'], "Channel2", True)

    response5 = message_send(url, response1['token'], response3, "Message One ilovedogs")
    response6 = message_send(url, response1['token'], response4, "Message Two ilovecats")

    return {
        'p1ID': response1['u_id'],
        'p1t': response1['token'],
        'p2ID': response2['u_id'],
        'p2t': response2['token'],
        'c1ID': response3,
        'c2ID': response4,
        'm1ID': response5,
        'm2ID': response6
    }

######################################################
## HELPER FUNCTIONS

def clear(url_clear):
    response = requests.delete(url_clear + 'clear')
    return response.status_code

def users_all(url_all, token):
    payload = {'token': token}
    response = requests.get(url_all + "users/all", params=payload)
    return {
        'status': response.status_code,
        'users': response.json().get('users')
    }

def admin_userpermission_change(url_perm, token, u_id, p_id):
    payload = {'token': token, 'u_id': u_id, 'permission_id': p_id}
    response = requests.post(url_perm + 'admin/userpermission/change', json=payload)
    return response.status_code

def search(url_search, token, qs):
    payload = {'token': token, 'query_str': qs}
    response = requests.get(url_search +'search', params=payload)
    return {
        'status': response.status_code,
        'messages': response.json().get('messages')
    }

def auth(url_auth, email, password, n1, n2):
    payload = {"email": email, "password": password, "name_first": n1, "name_last": n2}
    requests.post(url_auth + "auth/register", json=payload)
    payload = {"email": email, "password": password}
    response = requests.post(url_auth + "auth/login", json=payload)
    return response.json()

def channels_create(url_create, token, name, is_pub):
    payload = {"token": token, "name": name, "is_public": is_pub}
    response = requests.post(url_create + "channels/create", json=payload)
    return response.json()['channel_id']

def message_send(url_send, token, channel_id, msg):
    payload = {"token": token, "channel_id": channel_id, "message": msg}
    response = requests.post(url_send + "message/send", json=payload)
    return response.json()['message_id']

def channel_join(url_join, token, channel_id):
    payload = {"token": token, "channel_id": channel_id}
    response = requests.post(url_join + "channel/join", json=payload)
    return response.status_code

#####################################################

## CLEAR ##


## USERS ALL ##

# Check if all users are displayed
def test_users_all_contents(url, userObject):
    assert len(users_all(url, userObject['p1t'])['users']) == 2
    assert users_all(url, userObject['p1t'])['users'][0]['u_id'] == userObject['p1ID']
    assert users_all(url, userObject['p1t'])['users'][1]['u_id'] == userObject['p2ID']


# Check if the contents for both users are identical
def test_users_all_comparison(url, userObject):
    assert users_all(url, userObject['p1t']) == users_all(url, userObject['p2t'])



## SEARCH ##

## VALID CASES

# Search for a message with that exact query
def test_search_exact(url, userObject):
    query_str = "Message One ilovedogs"
    msg_dict = search(url, userObject['p1t'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m1ID']

    query_str = "Message Two ilovecats"
    msg_dict = search(url, userObject['p1t'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m2ID']

# Non-existant queries
def test_search_query_non_existant(url, userObject):
    assert search(url, userObject['p1t'], 'fish')['messages'] == []
    assert search(url, userObject['p1t'], 'ilovefish')['messages'] == []

# The search item is part of a message
def test_search_partly(url, userObject):
    assert len(search(url, userObject['p1t'], 'Message')['messages']) == 2
    assert len(search(url, userObject['p1t'], 'ilove')['messages']) == 2
    assert len(search(url, userObject['p1t'], 'cats')['messages']) == 1

# Query matches with message regardless of upper/lower/mixed cases
def test_search_ignore_case(url, userObject):
    assert len(search(url, userObject['p1t'], 'MESSAGE')['messages']) == 2
    assert len(search(url, userObject['p1t'], 'mEssAGe')['messages']) == 2

# More search results become available whenyou join multiple channels
def test_search_not_in_channel(url, userObject):
    assert len(search(url, userObject['p2t'], 'Message')['messages']) == 0
    
    # Join a channel
    channel_join(url, userObject['p2t'], userObject['c1ID'])
    assert len(search(url, userObject['p2t'], 'Message')['messages']) == 1

    # Join another
    channel_join(url, userObject['p2t'], userObject['c2ID'])
    assert len(search(url, userObject['p2t'], 'Message')['messages']) == 2


## INVALID CASES

# Valid search queries must have at least 2 characters
def test_search_short(url, userObject):
    assert search(url, userObject['p1t'], 'M')['status'] == ERROR

    assert search(url, userObject['p1t'], ' ')['status'] == ERROR

    assert search(url, userObject['p1t'], '')['status'] == ERROR


## ADMIN USER PERMISSION CHANGE ##

## VALID CASES

# A flockr owner can add someone else as a flockr owner
def test_make_flockr_owner(url, userObject):
    # Add p2 as a flockr owner
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p2ID'], 1) != None

    # Check that they have flockr owner privilges e.g. joining a private channel
    private = channels_create(url, userObject['p1t'], "PRIVATE", False)

    assert channel_join(url, userObject['p2t'], private) == 200


# The original flockr owner can get their rights revoked by another flockr owner
def test_remove_original_flockr_owner(url, userObject):
    # Add p2 as a flockr owner
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p2ID'], 1) != None

    # Remove flockr owner status from p1
    assert admin_userpermission_change(url, userObject['p2t'], userObject['p1ID'], 2) != None

    # Check that p1 has their flockr owner rights revoked by being unable to join a private channel

    private = channels_create(url, userObject['p2t'], 'PRIVATE', False)
    assert channel_join(url, userObject['p1t'], private) == ERROR


## INVALID CASES

# Can't change permissions if you are not a flockr owner
def test_not_owner_permission_change(url, userObject):
    # p2 is a normal member
    admin_userpermission_change(url, userObject['p2t'], userObject['p2ID'], 1) == ERROR


# If you are the only flockr owner left, you cannot remove yourself as an owner
def test_last_flockr_owner(url, userObject):
    # P1 changes P2 to flockr owner
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p2ID'], 1) != None
    # P2 changes P1 to member
    assert admin_userpermission_change(url, userObject['p2t'], userObject['p1ID'], 2) != None
    # p2 is the only flockr owner
    assert admin_userpermission_change(url, userObject['p2t'], userObject['p2ID'], 2) == ERROR


# Permission does not exist
def test_invalid_permission(url, userObject):
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p2ID'], 3) == ERROR


# User_id does not exist
def test_invalid_uid(url, userObject):
    assert admin_userpermission_change(url, userObject['p1t'], 42, 1) == ERROR


# User is already an owner/member
def test_redundant_perm_change(url, userObject):
    # P1 is already an owner
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p1ID'], 1) == ERROR

    # P2 is already a member
    assert admin_userpermission_change(url, userObject['p1t'], userObject['p2ID'], 2) == ERROR


## INVALID TOKEN CASES

# Pass a dummy token of a non-user
def test_other_invalid_tokens(url, userObject):
    users_all(url, 123456) == 400
    search(url, 7891011, 'Message')    == 400
    admin_userpermission_change(url, 22352356, userObject['p2ID'], 2) == 400
