import requests
import json 
from echo_http_test import url
import channel
import pytest

### Fixtures for ccreating Flockr and setting up users + channels
@pytest.fixture
def data():
    requests.delete(url + 'clear')

    # Flockr owner id and token
    payload = {"email":"almightygod@unsw.com", "password": "firstuser", "name_first": "Flockr", "name_last": "Owner"}
    response1 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"almightygod@unsw.com", "password": "firstuser"}
    response2 = requests.post(url + "auth/login", json=payload)

    # Person1 owner id and token
    payload = {"email":"person1@unsw.com", "password": "pass1234", "name_first": "Personone", "name_last": "One"}
    response3 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person1@unsw.com", "password": "pass1234"}
    response4 = requests.post(url + "auth/login", json=payload)

    # Person2 owner id and token
    payload = {"email":"person2@unsw.com", "password": "pass1234", "name_first": "Persontwo", "name_last": "Two"}
    response5 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person2@unsw.com", "password": "pass1234"}
    response6 = requests.post(url + "auth/login", json=payload)

    # Creatiion of Channels public and private
    payload = {"token": response3.json(), "name": "PublicChannel", "is_public": True}
    response7 = requests.post(url + "channels/create", json=payload)

    payload = {"token": response5.json(), "name": "PrivateChannel", "is_public": False}
    response8 = requests.post(url + "channels/create", json=payload)

    return {
        'flockr_owner_id': response1.json(),
        'flockr_owner_token': response2.json(),
        'p1_id': response3.json(),
        'p1_token': response4.json(),
        'p2_id': response5.json(),
        'p2_token': response6.json(),
        'public_id': response7.json(),
        'private_id': response8.json()
    }

'''
Users: FlockrOwner (FO), Person1, Person2, Person3, Person4, Person5
Public Channel: Person1 (O)
Private Channel: Person2 (O)
'''

#VALID CASES

### Owners in either public or private channel can invite anyone who is not in that channel
def test_invite_success_http(data):
    payload = {"token": data['p1_token']['token'], "channel_id":[], "u_id": data['p1_id']['u_id']}
    response = requests.get(url + "channel/invite", json=payload)
    assert response.status_code == 200
    assert response.json == []



