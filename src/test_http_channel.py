import requests
import json 
from echo_http_test import url
import channel
import pytest

### Fixtures for ccreating Flockr and setting up users + channels
@pytest.fixtures
def data():
    requests.delete(url + 'clear')

    payload = {"email":"almightygod@unsw.com", "password": "firstuser", "name_first": "Flockr", "name_last": "Owner"}
    response1 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person1@unsw.com", "password": "pass1234", "name_first": "Personone", "name_last": "One"}
    response2 = requests.post(url + "auth/register", json=payload)

    payload = {"email":"person2@unsw.com", "password": "pass1234", "name_first": "Persontwo", "name_last": "Two"}
    response3 = requests.post(url + "auth/register", json=payload)

    return {
        'Flockr_owner': response1.json(),
        'Person_One': response2.json(),
        'Person_Two': response3.json()
    }

'''
Users: FlockrOwner (FO), Person1, Person2, Person3, Person4, Person5
Public Channel: Person1 (O)
Private Channel: Person2 (O)
'''

#VALID CASES

### Owners in either public or private channel can invite anyone who is not in that channel
def test_invite_success_http(data):
