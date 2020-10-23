import requests
import json 
from echo_http_test import url
import channel as ch
import pytest

### Fixtures for ccreating Flockr and setting up users + channels
@pytest.fixture
def data(url):
    requests.delete(url + 'clear')
    # Flockr owner id and token
    payload = {"email":"almightygod@unsw.com", "password": "firstuser", "name_first": "Flockr", "name_last": "Owner"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"almightygod@unsw.com", "password": "firstuser"}
    response0 = requests.post(url + "auth/login", json=payload)

    # Person1 owner id and token
    payload = {"email":"person1@unsw.com", "password": "pass1234", "name_first": "Personone", "name_last": "One"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"person1@unsw.com", "password": "pass1234"}
    response1 = requests.post(url + "auth/login", json=payload)

    # Person2 owner id and token
    payload = {"email":"person2@unsw.com", "password": "pass1234", "name_first": "Persontwo", "name_last": "Two"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"person2@unsw.com", "password": "pass1234"}
    response2 = requests.post(url + "auth/login", json=payload)

    # Person3 owner id and token
    payload = {"email":"person3@unsw.com", "password": "pass1234", "name_first": "Personthree", "name_last": "Three"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"person3@unsw.com", "password": "pass1234"}
    response3 = requests.post(url + "auth/login", json=payload)

    # Person4 owner id and token
    payload = {"email":"person4@unsw.com", "password": "pass1234", "name_first": "Personfour", "name_last": "Four"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"person4@unsw.com", "password": "pass1234"}
    response4 = requests.post(url + "auth/login", json=payload)

    # Person5 owner id and token
    payload = {"email":"person5@unsw.com", "password": "pass1234", "name_first": "Personfive", "name_last": "Five"}
    requests.post(url + "auth/register", json=payload)
    payload = {"email":"person5@unsw.com", "password": "pass1234"}
    response5 = requests.post(url + "auth/login", json=payload)

    # Creatiion of Channels public and private
    payload = {"token": response1.json()['token'], "name": "PublicChannel", "is_public": True}
    response6 = requests.post(url + "channels/create", json=payload)

    # channels.channels_create(p1_token, "PublicChannel", True)['channel_id'],
    payload = {"token": response2.json()['token'], "name": "PrivateChannel", "is_public": False}
    response7 = requests.post(url + "channels/create", json=payload)

    return {
        'flockr_owner': response0.json(),
        'p1': response1.json(),
        'p2': response2.json(),
        'p3': response3.json(),
        'p4': response4.json(),
        'p5': response5.json(),
        'public_id': response6.json()['channel_id'],
        'private_id': response7.json()['channel_id']
    }

'''
Users: FlockrOwner (FO), Person1, Person2, Person3, Person4, Person5
Public Channel: Person1 (O)
Private Channel: Person2 (O)
'''

# channel/invite

def test_invite_success(url, data):
    # assert channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p2']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)

    assert response.status_code == 200
    
    # assert channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

    # assert ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])
    payload = {"token": data['p2']['token'], "channel_id": data['private_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code == 200

def test_invite_existing(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p2']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)

    # InputError: ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p2']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code != 200
    
    # InputError: ch.channel_invite(data['p1_token'], data['public_id'], data['p1_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p1']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)
    assert response.status_code != 200


#channel/leave

def test_leave_success(url, data):
    # Steps:
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)

    payload = {"token": data['p2']['token'], "channel_id": data['private_id'], "u_id": data['p4']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)

    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/addowner", json=payload)

    # assert ch.channel_leave(data['p4_token'], data['private_id'])
    payload = {"token": data['p4']['token'], "channel_id": data['private_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code == 200

    # assert ch.channel_leave(data['p4_token'], data['private_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code == 200

def test_owner_leaving(url, data):

    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/invite", json=payload)

    # InputError: ch.channel_leave(data['p1_token'], data['public_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code != 200

    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id']) 
    payload = {"token": data['p1']['token'], "channel_id": data['public_id'], "u_id": data['p3']['u_id']}
    response = requests.post(url + "channel/addowner", json=payload)

    # assert ch.channel_leave(data['p1_token'], data['public_id'])
    payload = {"token": data['p1']['token'], "channel_id": data['public_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code == 200
    
    # InputError ch.channel_leave(data['p3_token'], data['public_id'])
    payload = {"token": data['p3']['token'], "channel_id": data['public_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code != 200

def test_leaving_diff_channel(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    payload = {"token": data['p3']['token'], "channel_id": data['public_id']}
    response = requests.post(url + "channel/join", json=payload)

    # AccessError ch.channel_leave(data['p3_token'], data['private_id'])
    payload = {"token": data['p3']['token'], "channel_id": data['private_id']}
    response = requests.post(url + "channel/leave", json=payload)
    assert response.status_code != 200