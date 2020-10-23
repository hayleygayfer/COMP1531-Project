import requests
import json 
from echo_http_test import url
import pytest

### Fixtures for creating Flockr and setting up users + channels
@pytest.fixture
def data(url):
    requests.delete(url + 'clear')

    # Flockr owner id and token
    response0 = auth(url, "almightygod@unsw.com", "firstuser", "Flockr", "Owner")

    # Person1 - Person5
    response1 = auth(url, "person1@unsw.com", "pass1234", "Personone", "One")
    response2 = auth(url, "person2@unsw.com", "pass1234", "Persontwo", "Two")
    response3 = auth(url, "person3@unsw.com", "pass1234", "Personthree", "Three")
    response4 = auth(url, "person4@unsw.com", "pass1234", "Personfour", "Four")
    response5 = auth(url, "person5@unsw.com", "pass1234", "Personfive", "Five")

    # Creatiion of Channels public and private
    response6 = create(url, response1['token'], "PublicChannel", True)
    response7 = create(url, response2['token'], "PrivateChannel", False)

    return {
        'flockr_owner': response0,
        'p1': response1,
        'p2': response2,
        'p3': response3,
        'p4': response4,
        'p5': response5,
        'public_id': response6['channel_id'],
        'private_id': response7['channel_id']
    }

'''
Users: FlockrOwner (FO), Person1, Person2, Person3, Person4, Person5
Public Channel: Person1 (O)
Private Channel: Person2 (O)
'''

######################################################################
## HELPER FUNCTIONS
######################################################################

def auth(url_str, email, password, n1, n2):
    payload = {"email": email, "password": password, "name_first": n1, "name_last": n2}
    requests.post(url_str + "auth/register", json=payload)
    payload = {"email": email, "password": password}
    response = requests.post(url_str + "auth/login", json=payload)
    return response.json()

def create(url_create, token, name, is_pub):
    payload = {"token": token, "name": name, "is_public": is_pub}
    response = requests.post(url_create + "channels/create", json=payload)
    return response.json()

def invite(url_invite, token, channel_id, u_id):
    payload = {"token": token, "channel_id": channel_id, "u_id": u_id}
    response = requests.post(url_invite + "channel/invite", json=payload)
    return response.status_code

def leave(url_leave, token, channel_id):
    payload = {"token": token, "channel_id": channel_id}
    response = requests.post(url_leave + "channel/leave", json=payload)
    return response.status_code

def join(url_join, token, channel_id):
    payload = {"token": token, "channel_id": channel_id}
    response = requests.post(url_join + "channel/join", json=payload)
    return response.status_code

def add_owner(url_add, token, channel_id, u_id):
    payload = {"token": token, "channel_id": channel_id, "u_id": u_id}
    response = requests.post(url_add + "channel/addowner", json=payload)
    return response.status_code

def rem_owner(url_rem, token, channel_id, u_id):
    payload = {"token": token, "channel_id": channel_id, "u_id": u_id}
    response = requests.post(url_rem + "channel/removeowner", json=payload)
    return response.status_code

######################################################################

## /channel/invite ##

def test_invite_success(url, data):
    # assert channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    assert invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) == 200
    
    # assert channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    assert invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id']) == 200

    # assert ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])
    assert invite(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) == 200

def test_invite_existing(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])

    # InputError: ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    assert invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) != 200
    
    # InputError: ch.channel_invite(data['p1_token'], data['public_id'], data['p1_id'])
    assert invite(url, data['p1']['token'], data['public_id'], data['p1']['u_id']) != 200

def test_not_in_channel_invite(url, data):
    # AccessError: ch.channel_invite(data['p2_token'], data['public_id'], data['p3_id'])
    assert invite(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) != 200

    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])

    # assert ch.channel_invite(data['p2_token'], data['public_id'], data['p3_id'])
    assert invite(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) == 200

## TODO: /channel/details ##

## TODO: /channel/messages ##

## /channel/leave ##

def test_leave_success(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # assert ch.channel_leave(data['p4_token'], data['private_id'])
    assert leave(url, data['p4']['token'], data['private_id']) == 200

    # assert ch.channel_leave(data['p1_token'], data['public_id'])
    assert leave(url, data['p1']['token'], data['public_id']) == 200

def test_owner_leaving(url, data):

    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # InputError: ch.channel_leave(data['p1_token'], data['public_id'])
    assert leave(url, data['p1']['token'], data['public_id']) != 200

    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id']) 
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # assert ch.channel_leave(data['p1_token'], data['public_id'])
    assert leave(url, data['p1']['token'], data['public_id']) == 200
    
    # InputError ch.channel_leave(data['p3_token'], data['public_id'])
    assert leave(url, data['p3']['token'], data['public_id']) != 200

def test_leaving_diff_channel(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])

    # AccessError ch.channel_leave(data['p3_token'], data['private_id'])
    assert leave(url, data['p3']['token'], data['private_id']) != 200

## /channel/join ##
def test_join_public(url, data):
    # assert ch.channel_join(data['p2_token'], data['public_id'])
    assert join(url, data['p2']['token'], data['public_id']) == 200

    # assert ch.channel_join(data['p3_token'], data['public_id'])
    assert join(url, data['p3']['token'], data['public_id']) == 200

    # assert ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert join(url, data['flockr_owner']['token'], data['public_id']) == 200

def test_join_private(url, data):
    # AccessError ch.channel_join(data['p1_token'], data['private_id'])
    assert join(url, data['p1']['token'], data['private_id']) != 200

    # AccessError ch.channel_join(data['p3_token'], data['private_id'])
    assert join(url, data['p3']['token'], data['private_id']) != 200

def test_join_but_existing(url, data):
    # InputError ch.channel_join(data['p1_token'], data['public_id'])
    assert join(url, data['p1']['token'], data['public_id']) != 200

    # Steps:
    # 1. ch.channel_join(data['p3_token'], data['public_id'])
    # 2. ch.channel_join(data['p4_token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])

    join(url, data['p4']['token'], data['public_id'])

    # InputError ch.channel_join(data['p3_token'], data['public_id'])
    assert join(url, data['p3']['token'], data['public_id']) != 200

    # InputError ch.channel_join(data['p4_token'], data['public_id'])
    assert join(url, data['p4']['token'], data['public_id']) != 200

def test_leave_then_join(url, data):
    # ch.channel_join(data['p2_token'], data['public_id'])
    join(url, data['p2']['token'], data['public_id'])

    # Assert ch.channel_leave(data['p2_token'], data['public_id'])
    assert leave(url, data['p2']['token'], data['public_id']) == 200

    # join
    assert join(url, data['p2']['token'], data['public_id']) == 200 == 200

    # leave
    assert leave(url, data['p2']['token'], data['public_id']) == 200

## /channel/addowner ##
def test_addowner_success(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])

    # ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p2']['u_id'])

    # assert ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    assert add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) == 200

    # assert ch.channel_addowner(data['p2_token'], data['private_id'], data['p1_id'])
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p1']['u_id']) != 200

def test_addowner_but_not_owner(url, data):
    # ch.channel_join(data['p2_token'], data['public_id'])
    join(url, data['p2']['token'], data['public_id'])

    # ch.channel_join(data['p3_token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])
    
    # AccessError ch.channel_addowner(data['p2_token'], data['public_id'], data['p3_id'])
    assert add_owner(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) != 200
    
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    
    # AccessError ch.channel_addowner(data['p2_token'], data['public_id'], data['p3_id'])
    assert add_owner(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) == 200

def test_addowner_when_already_owner(url, data):
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    
    # ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id'])
    add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    
    # InputError ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id']) 
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) != 200
    
    # InputError ch.channel_addowner(data['p3_token'], data['private_id'], data['p2_id']) 
    assert add_owner(url, data['p3']['token'], data['private_id'], data['p2']['u_id']) != 200

def test_addowner_but_not_in_channel(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])

    # InputError ch.channel_addowner(data['p1_token'], data['public_id'], data['p4_id']) # Person4 is not in public
    assert add_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200
    
    # InputError ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id']) # Person3 is not in private
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) != 200

    

## /channel/removeowner ##

def test_removeowner_success(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    # ch.channel_addowner(data['p2_token'], data['private_id'], data['p1_id'])

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    add_owner(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])

    # assert ch.channel_removeowner(data['p2_token'], data['public_id'], data['p1_id'])
    assert rem_owner(url, data['p2']['token'], data['public_id'], data['p1']['u_id']) == 200
    
    # assert ch.channel_removeowner(data['p1_token'], data['private_id'], data['p2_id'])
    assert rem_owner(url, data['p1']['token'], data['private_id'], data['p2']['u_id']) == 200

def test_removeowner_but_not_owner(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    # ch.channel_join(data['p4_token'], data['public_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    join(url, data['p3']['token'], data['public_id'])
    join(url, data['p4']['token'], data['public_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # AccessError: ch.channel_removeowner(data['p4_token'], data['public_id'], data['p3_id'])
    assert rem_owner(url, data['p4']['token'], data['public_id'], data['p3']['u_id']) != 200

def test_removeowner_for_ordinary_member(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    # ch.channel_join(data['p4_token'], data['public_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    join(url, data['p3']['token'], data['public_id'])
    join(url, data['p4']['token'], data['public_id'])        
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # AccessError: ch.channel_removeowner(data['p1_token'], data['public_id'], data['p4_id'])
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200

def test_removeowner_but_not_in_channel(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    # ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    # ch.channel_addowner(data['p2_token'], data['private_id'], data['p4_id'])

    join(url, data['p3']['token'], data['public_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    add_owner(url, data['p2']['token'], data['public_id'], data['p4']['u_id'])

    # InputError: ch.channel_removeowner(data['p1_token'], data['public_id'], data['p4_id'])
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200

def test_self_removeowner(url, data):
    # ch.channel_join(data['p3_token'], data['public_id'])
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    join(url, data['p3']['token'], data['public_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # InputError: ch.channel_removeowner(data['p1_token'], data['public_id'], data['p1_id'])
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p1']['u_id']) != 200
    
    # InputError: ch.channel_removeowner(data['p3_token'], data['public_id'], data['p3_id'])
    assert rem_owner(url, data['p3']['token'], data['public_id'], data['p3']['u_id']) != 200


## Invalid Cases ##
def test_invalid_channels(url, data):
    # InputError ch.channel_invite(data['p1_token'], 4645, data['p3_id'])
    assert invite(url, data['p1']['token'], 4645, data['p3']['u_id']) != 200

    # InputError ch.channel_join(data['p3_token'], 24324)
    assert join(url, data['p3']['token'], 24342) != 200
    
    # TODO: InputError ch.channel_messages(data['p1_token'], 3235325, 0)

    # ch.channel_join(data['p3_token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])

    # InputError ch.channel_leave(data['p3_token'], 523545)
    assert leave(url, data['p3']['token'], 523545) != 200

    # InputError ch.channel_addowner(data['p1_token'], 3453453, data['p3_id'])
    assert add_owner(url, data['p1']['token'], 3453452, data['p3']['u_id'])
    
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError ch.channel_removeowner(data['p1_token'], 436356, data['p3_id'])
    assert rem_owner(url, data['p1']['token'], 4362674, data['p3']['u_id']) != 200

# Invalid U_ID raises InputErrors
def test_invalid_u_id(url, data):
    # InputError ch.channel_invite(data['p1_token'], data['public_id'], 3454356)
    assert invite(url, data['p1']['token'], data['public_id'], 324215423) != 200
    
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError ch.channel_addowner(data['p1_token'], data['public_id'], 4365346)
    assert add_owner(url, data['p1']['token'], data['public_id'], 325252535) != 200
    
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError ch.channel_removeowner(data['p1_token'], data['public_id'], 2354542)
    assert rem_owner(url, data['p1']['token'], data['public_id'], 2345662352345) != 200

# invalid tokens raise AccessErrors
def test_invalid_tokens(url, data):
    # ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    
    # AccessError ch.channel_invite(2736273, data['public_id'], data['p3_id'])
    assert invite(url, 435614532, data['public_id'], data['p3']['u_id']) != 200
    
    # AccessError ch.channel_join(56453, data['public_id'])
    assert join(url, 4353245, data['public_id']) != 200
    
    # TODO: AccessError ch.channel_details(23532, data['public_id'])
    
    
    # AccessError ch.channel_leave(563464, data['public_id'])
    assert leave(url, 3462623, data['public_id']) != 200
    
    # AccessError ch.channel_addowner(23141, data['public_id'], data['p2_id'])
    assert add_owner(url, 53245523253, data['public_id'], data['p2']['u_id']) != 200
    
    # ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    
    # AccessError ch.channel_removeowner(23141, data['public_id'], data['p2_id'])
    assert rem_owner(url, 534252, data['public_id'], data['p2']['u_id']) != 200
    
    # TODO: AccessError ch.channel_messages(232414, data['public_id'], 0)


'''## Flockr owner tests ##
def test_flockr_addowner_success(url, data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    ch.channel_join(data['p3_token'], data['public_id'])
    assert ch.channel_addowner(data['flockr_owner_token'], data['public_id'], data['p3_id'])


# FlockR owner must to be a member of the channel to remove an owner
# They don't necessarily have to be a channel owner 
def test_flockr_removeowner_success(url, data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    
    ch.channel_invite(data['p2_token'], data['private_id'], data['flockr_owner_id'])
    assert ch.channel_removeowner(data['flockr_owner_token'], data['private_id'], data['p2_id'])


# If the flockR owner is not part of the channel, they don't get any piviledges
def test_flockr_addowner_but_not_member(url, data):
    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    with pytest.raises(AccessError):
        ch.channel_addowner(data['flockr_owner_token'], data['public_id'], data['p3_id'])
    with pytest.raises(AccessError):
        ch.channel_addowner(data['flockr_owner_token'], data['private_id'], data['p4_id'])


# If the flockR owner is not part of the channel, they don't get any piviledges
def test_flockr_removeowner_but_not_member(url, data):
    with pytest.raises(AccessError):
        ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    with pytest.raises(AccessError):
        ch.channel_removeowner(data['flockr_owner_token'], data['private_id'], data['p2_id'])


# FlockR members are allowed to join private channels
def test_flockr_join_private(url, data):
    assert ch.channel_join(data['flockr_owner_token'], data['private_id'])
    assert ch.channel_leave(data['flockr_owner_token'], data['private_id'])
    assert ch.channel_join(data['flockr_owner_token'], data['private_id'])


# FlockR owners are allowed to invite anyone who is not currently in the private channel
# even when they are not an owner of the channel
def test_flockr_invite_private(url, data):
    ch.channel_invite(data['p2_token'], data['private_id'], data['flockr_owner_id'])
    assert ch.channel_invite(data['flockr_owner_token'], data['private_id'], data['p3_id'])


# Adding the FlockR owner as a channel owner doesn't change much
def test_add_flockr_as_owner(url, data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_addowner(data['p1_token'], data['public_id'], data['flockr_owner_id'])
    with pytest.raises(InputError):
        ch.channel_addowner(data['p1_token'], data['public_id'], data['flockr_owner_id'])

    assert ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    with pytest.raises(InputError):
        ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])


# Flockr members can leave channels but the channels must have an owner
def test_flockr_leaving_channel(url, data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_leave(data['flockr_owner_token'], data['public_id'])

    # Leaving a channel with no owners
    ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    
    with pytest.raises(InputError):
        # If FlockR owner leaves then Person3 is the only member left and there are no owners
        ch.channel_leave(data['flockr_owner_token'], data['public_id'])
'''