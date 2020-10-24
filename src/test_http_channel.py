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

## CHANNEL ##
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

def details(url_detail, token, channel_id):
    payload = {'token': token, 'channel_id': channel_id}
    response = requests.get(url_detail + "channel/details", params=payload)
    return {
        'status': response.status_code,
        'name': response.json().get('name'),
        'owners': response.json().get('owner_members'),
        'all': response.json().get('all_members')
    }

def messages(url_msg, token, channel_id, start):
    payload = {'token': token, 'channel_id': channel_id, 'start': start}
    response = requests.get(url_msg + "channel/messages", params=payload)
    return {
        'status': response.status_code,
        'msgs': response.json().get('messages'),
        'start': response.json().get('start'),
        'end': response.json().get('end')
    }

## OTHER ##
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

def send(url_send, token, channel_id, msg):
    payload = {"token": token, "channel_id": channel_id, "message": msg,}
    requests.post(url_send + "message/send", json=payload)


######################################################################
## /channel/invite ##

def test_invite_success(url, data):
    '''Owners in either public or private channel can invite anyone who is not a member of the channel'''
    
    assert invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) == 200
    assert invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id']) == 200
    assert invite(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) == 200

def test_invite_existing(url, data):
    '''Can't invite an existing member'''

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])

    # InputErrors:
    assert invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) != 200
    assert invite(url, data['p1']['token'], data['public_id'], data['p1']['u_id']) != 200

def test_not_in_channel_invite(url, data):
    '''User must be a member of a channel to invite someone'''

    # AccessError:
    assert invite(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) != 200

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    assert invite(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) == 200


########################################################################
## /channel/details ##

def test_details_authorisation(url, data):
    '''channel_details requires the person viewing the details to be a member of the channel'''

    assert details(url, data['p1']['token'], data['public_id'])['status'] == 200
    assert details(url, data['p2']['token'], data['private_id'])['status'] == 200

    # AccessErrors: 
    assert details(url, data['p2']['token'], data['public_id'])['status'] != 200
    assert details(url, data['p1']['token'], data['private_id'])['status'] != 200

def test_view_details(url, data):
    '''Checking whether all the necessary channel details are returned'''

    invite(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])
    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    join(url, data['p5']['token'], data['public_id'])
    rem_owner(url, data['p3']['token'], data['private_id'], data['p2']['u_id'])
    leave(url, data['p2']['token'], data['public_id'])

    '''
    Public: Person1 (O), <Person 2 left>, Person5
    Private: Person2, Person3 (O), Person4
    '''

    assert details(url, data['p1']['token'], data['public_id'])['name'] == 'PublicChannel'
    assert details(url, data['p1']['token'], data['public_id'])['owners'][0]['u_id'] == data['p1']['u_id']
    assert details(url, data['p1']['token'], data['public_id'])['owners'][0]['name_first'] == 'Personone'
    assert details(url, data['p1']['token'], data['public_id'])['owners'][0]['name_last'] == 'One'
    assert details(url, data['p1']['token'], data['public_id'])['all'][0]['u_id'] == data['p1']['u_id']
    assert details(url, data['p1']['token'], data['public_id'])['all'][0]['name_first'] == 'Personone'
    assert details(url, data['p1']['token'], data['public_id'])['all'][0]['name_last'] == 'One'
    assert details(url, data['p1']['token'], data['public_id'])['all'][1]['u_id'] == data['p5']['u_id']

    assert details(url, data['p2']['token'], data['private_id'])['name'] == 'PrivateChannel'
    assert details(url, data['p2']['token'], data['private_id'])['owners'][0]['u_id'] == data['p3']['u_id']
    assert details(url, data['p2']['token'], data['private_id'])['owners'][0]['name_first'] == 'Personthree'
    assert details(url, data['p2']['token'], data['private_id'])['owners'][0]['name_last'] == 'Three'
    assert details(url, data['p2']['token'], data['private_id'])['all'][0]['u_id'] == data['p2']['u_id']
    assert details(url, data['p2']['token'], data['private_id'])['all'][0]['name_first'] == 'Persontwo'
    assert details(url, data['p2']['token'], data['private_id'])['all'][0]['name_last'] == 'Two'
    assert details(url, data['p2']['token'], data['private_id'])['all'][1]['u_id'] == data['p3']['u_id']
    assert details(url, data['p2']['token'], data['private_id'])['all'][2]['u_id'] == data['p4']['u_id']
    

####################################################################
## /channel/messages ##

def test_view_messages_authorisation(url, data):
    '''Must be a member of the channel to view messages'''

    send(url, data['p1']['token'], data['public_id'], "public message")
    send(url, data['p2']['token'], data['private_id'], "private message")

    assert messages(url, data['p1']['token'], data['public_id'], 0)['status'] == 200
    assert messages(url, data['p2']['token'], data['private_id'], 0)['status'] == 200

    # AccessErrors:
    assert messages(url, data['p2']['token'], data['public_id'], 0)['status'] != 200
    assert messages(url, data['p1']['token'], data['private_id'], 0)['status'] != 200

    invite(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])
    assert messages(url, data['p1']['token'], data['private_id'], 0)['status'] == 200

def test_invalid_messages_start(url, data):
    '''Checking for valid start values'''

    for x in range(1, 10 + 1):
        send(url, data['p1']['token'], data['public_id'], f"Message {x}")
    
    # InputErrors:
    assert messages(url, data['p1']['token'], data['public_id'], 11)['status'] != 200
    assert messages(url, data['p1']['token'], data['public_id'], 10)['status'] != 200

    assert messages(url, data['p1']['token'], data['public_id'], 9)['status'] == 200

def test_message_less_than_50(url, data):
    '''checking return values after adding a few messages to a channel'''

    for x in range(1, 4 + 1):
        send(url, data['p1']['token'], data['public_id'], f"Message {x}")
    
    assert messages(url, data['p1']['token'], data['public_id'], 0)['start'] == 0
    assert messages(url, data['p1']['token'], data['public_id'], 0)['end'] == -1
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][0]['message'] == 'Message 4'
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][1]['message'] == 'Message 3'
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][2]['message'] == 'Message 2'
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][3]['message'] == 'Message 1'

def test_message_exactly_50(url, data):
    '''checking return values after adding exactly 50 messages to a channel'''

    for x in range(1, 50 + 1):
        send(url, data['p1']['token'], data['public_id'], f"Message {x}")

    assert messages(url, data['p1']['token'], data['public_id'], 0)['start'] == 0
    assert messages(url, data['p1']['token'], data['public_id'], 0)['end'] == -1
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][0]['message'] == 'Message 50'
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][49]['message'] == 'Message 1'


def test_150_messages(url, data):
    '''Pagination with 150 messages by modifying start values'''

    for x in range(1, 150 + 1):
        send(url, data['p1']['token'], data['public_id'], f"Message {x}")

    # start = 0
    assert messages(url, data['p1']['token'], data['public_id'], 0)['start'] == 0
    assert messages(url, data['p1']['token'], data['public_id'], 0)['end'] == 50
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][0]['message'] == 'Message 150'
    assert messages(url, data['p1']['token'], data['public_id'], 0)['msgs'][49]['message'] == 'Message 101'

    # start = 50
    assert messages(url, data['p1']['token'], data['public_id'], 50)['start'] == 50
    assert messages(url, data['p1']['token'], data['public_id'], 50)['end'] == 100
    assert messages(url, data['p1']['token'], data['public_id'], 50)['msgs'][0]['message'] == 'Message 100'
    assert messages(url, data['p1']['token'], data['public_id'], 50)['msgs'][49]['message'] == 'Message 51'

    # start = 100
    assert messages(url, data['p1']['token'], data['public_id'], 100)['start'] == 100
    assert messages(url, data['p1']['token'], data['public_id'], 100)['end'] == -1
    assert messages(url, data['p1']['token'], data['public_id'], 100)['msgs'][0]['message'] == 'Message 50'
    assert messages(url, data['p1']['token'], data['public_id'], 100)['msgs'][49]['message'] == 'Message 1'

def test_negative_start(url, data):
    '''Negative start values revert to 0'''

    send(url, data['p1']['token'], data['public_id'], "test")
    assert messages(url, data['p1']['token'], data['public_id'], -1) == messages(url, data['p1']['token'], data['public_id'], 0)


#######################################################################
## /channel/leave ##

def test_leave_success(url, data):
    '''successfully leaving a channel'''

    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    assert leave(url, data['p4']['token'], data['private_id']) == 200
    assert leave(url, data['p1']['token'], data['public_id']) == 200

def test_owner_leaving(url, data):
    '''a channel owner cannot leave if they are the last remaining owner'''

    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # InputError:
    assert leave(url, data['p1']['token'], data['public_id']) != 200

    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    assert leave(url, data['p1']['token'], data['public_id']) == 200
    
    # InputError:
    assert leave(url, data['p3']['token'], data['public_id']) != 200

def test_leaving_diff_channel(url, data):
    '''a member can't leave a channel that they are not in'''

    join(url, data['p3']['token'], data['public_id'])

    # AccessError:
    assert leave(url, data['p3']['token'], data['private_id']) != 200


#########################################################################
## /channel/join ##

def test_join_public(url, data):
    '''anyone who is not already in the channel can join a public channel'''

    assert join(url, data['p2']['token'], data['public_id']) == 200
    assert join(url, data['p3']['token'], data['public_id']) == 200
    assert join(url, data['flockr_owner']['token'], data['public_id']) == 200

def test_join_private(url, data):
    '''No one can join a private channel'''

    # AccessError:
    assert join(url, data['p1']['token'], data['private_id']) != 200
    assert join(url, data['p3']['token'], data['private_id']) != 200

def test_join_but_existing(url, data):
    '''An existing member can't join again'''

    # InputError:
    assert join(url, data['p1']['token'], data['public_id']) != 200

    join(url, data['p3']['token'], data['public_id'])
    join(url, data['p4']['token'], data['public_id'])

    # InputErrors:
    assert join(url, data['p3']['token'], data['public_id']) != 200
    assert join(url, data['p4']['token'], data['public_id']) != 200

def test_leave_then_join(url, data):
    '''Users are allowed to leave then join again'''

    assert join(url, data['p2']['token'], data['public_id']) == 200
    assert leave(url, data['p2']['token'], data['public_id']) == 200
    assert join(url, data['p2']['token'], data['public_id']) == 200
    assert leave(url, data['p2']['token'], data['public_id']) == 200


##########################################################################
## /channel/addowner ##

def test_addowner_success(url, data):
    '''A pre-existing owner must add a normal member in that channel to be successful'''

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])
    assert add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id']) == 200
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p1']['u_id']) == 200

def test_addowner_but_not_owner(url, data):
    '''you must be an owner to add someone as an owner'''

    join(url, data['p2']['token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])
    
    # AccessError:
    assert add_owner(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) != 200
    
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    assert add_owner(url, data['p2']['token'], data['public_id'], data['p3']['u_id']) == 200

def test_addowner_when_already_owner(url, data):
    '''You can't make an owner an owner'''

    invite(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id'])
    
    # InputErrors:
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) != 200
    assert add_owner(url, data['p3']['token'], data['private_id'], data['p2']['u_id']) != 200

def test_addowner_but_not_in_channel(url, data):
    '''Both users must be in the same channel'''

    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])   
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])

    # InputErrors
    assert add_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200
    assert add_owner(url, data['p2']['token'], data['private_id'], data['p3']['u_id']) != 200


########################################################################
## /channel/removeowner ##

def test_removeowner_success(url, data):
    '''When there are multiple owners, then the newest member has the right to remove the creator as a member'''

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    add_owner(url, data['p2']['token'], data['private_id'], data['p1']['u_id'])

    assert rem_owner(url, data['p2']['token'], data['public_id'], data['p1']['u_id']) == 200
    assert rem_owner(url, data['p1']['token'], data['private_id'], data['p2']['u_id']) == 200

def test_removeowner_but_not_owner(url, data):
    '''You must be an owner to reomve someone as an owner'''

    join(url, data['p3']['token'], data['public_id'])
    join(url, data['p4']['token'], data['public_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # AccessError:
    assert rem_owner(url, data['p4']['token'], data['public_id'], data['p3']['u_id']) != 200

def test_removeowner_for_ordinary_member(url, data):
    '''You must remove an owner and not an ordinary member'''

    join(url, data['p3']['token'], data['public_id'])
    join(url, data['p4']['token'], data['public_id'])        
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # AccessError:
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200

def test_removeowner_but_not_in_channel(url, data):
    '''Both users must be in the same channel'''

    join(url, data['p3']['token'], data['public_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    add_owner(url, data['p2']['token'], data['public_id'], data['p4']['u_id'])

    # InputError:
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p4']['u_id']) != 200

def test_self_removeowner(url, data):
    '''Can't remove yourself'''

    join(url, data['p3']['token'], data['public_id'])
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])

    # InputErrors:
    assert rem_owner(url, data['p1']['token'], data['public_id'], data['p1']['u_id']) != 200
    assert rem_owner(url, data['p3']['token'], data['public_id'], data['p3']['u_id']) != 200


######################################################################
## Invalid Cases ##

def test_invalid_channels(url, data):
    '''invalid channels raise InputErrors'''

    # InputErrors:
    assert invite(url, data['p1']['token'], 4645, data['p3']['u_id']) != 200
    assert join(url, data['p3']['token'], 24342) != 200
    assert details(url, data['p1']['token'], 326532) != 200
    assert messages(url, data['p1']['token'], 23762323, 0) != 200

    join(url, data['p3']['token'], data['public_id'])

    # InputErrors:
    assert leave(url, data['p3']['token'], 523545) != 200
    assert add_owner(url, data['p1']['token'], 3453452, data['p3']['u_id']) != 200
    
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError:
    assert rem_owner(url, data['p1']['token'], 4362674, data['p3']['u_id']) != 200

def test_invalid_u_id(url, data):
    '''Invalid U_ID raises InputErrors'''

    # InputError:
    assert invite(url, data['p1']['token'], data['public_id'], 324215423) != 200
    
    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError:
    assert add_owner(url, data['p1']['token'], data['public_id'], 325252535) != 200
    
    add_owner(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    
    # InputError:
    assert rem_owner(url, data['p1']['token'], data['public_id'], 2345662352345) != 200

def test_invalid_tokens(url, data):
    '''Invalid tokens raise AccessErrors'''

    invite(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    
    # AccessErrors:
    assert invite(url, 435614532, data['public_id'], data['p3']['u_id']) != 200
    assert join(url, 4353245, data['public_id']) != 200
    assert details(url, 2745624, data['public_id']) != 200
    assert leave(url, 3462623, data['public_id']) != 200
    assert add_owner(url, 53245523253, data['public_id'], data['p2']['u_id']) != 200
    
    add_owner(url, data['p1']['token'], data['public_id'], data['p2']['u_id'])
    
    # AccessErrors:
    assert rem_owner(url, 534252, data['public_id'], data['p2']['u_id']) != 200
    assert messages(url, 264323, data['public_id'], 0)


######################################################################
## Flockr owner tests ##

def test_flockr_addowner_success(url, data):
    '''
    The FlockR owner is allowed to add standard users as owners 
    even if they are not an owner of the channel.
    '''

    join(url, data['flockr_owner']['token'], data['public_id'])
    join(url, data['p3']['token'], data['public_id'])
    assert add_owner(url, data['flockr_owner']['token'], data['public_id'], data['p3']['u_id']) == 200

def test_flockr_removeowner_success(url, data):
    '''
    FlockR owner must to be a member of the channel to remove an owner.
    They don't necessarily have to be a channel owner.
    '''

    join(url, data['flockr_owner']['token'], data['public_id'])
    assert rem_owner(url, data['flockr_owner']['token'], data['public_id'], data['p1']['u_id']) == 200
    invite(url, data['p2']['token'], data['private_id'], data['flockr_owner']['u_id'])
    assert rem_owner(url, data['flockr_owner']['token'], data['private_id'], data['p2']['u_id']) == 200

def test_flockr_addowner_but_not_member(url, data):
    '''
    If the flockR owner is not part of the channel, they don't get any piviledges.
    '''

    join(url, data['p3']['token'], data['public_id'])
    invite(url, data['p2']['token'], data['private_id'], data['p4']['u_id'])

    # AccessError:
    assert add_owner(url, data['flockr_owner']['token'], data['public_id'], data['p3']['u_id']) != 200
    assert add_owner(url, data['flockr_owner']['token'], data['private_id'], data['p4']['u_id']) != 200


def test_flockr_removeowner_but_not_member(url, data):
    '''
    If the flockR owner is not part of the channel, they don't get any piviledges.
    '''

    # AccessErrors:
    assert rem_owner(url, data['flockr_owner']['token'], data['public_id'], data['p1']['u_id']) != 200
    assert rem_owner(url, data['flockr_owner']['token'], data['private_id'], data['p2']['u_id']) != 200


def test_flockr_join_private(url, data):
    '''
    FlockR members are allowed to join private channels
    '''

    assert join(url, data['flockr_owner']['token'], data['private_id']) == 200
    assert leave(url, data['flockr_owner']['token'], data['private_id']) == 200
    assert join(url, data['flockr_owner']['token'], data['private_id']) == 200


def test_flockr_invite_private(url, data):
    '''
    FlockR owners are allowed to invite anyone who is not currently in the
    private channel even when they are not an owner of the channel.
    '''

    invite(url, data['p2']['token'], data['private_id'], data['flockr_owner']['u_id'])
    assert invite(url, data['flockr_owner']['token'], data['private_id'], data['p3']['u_id']) == 200


def test_add_flockr_as_owner(url, data):
    '''
    Adding the FlockR owner as a channel owner doesn't change much.
    '''

    join(url, data['flockr_owner']['token'], data['public_id'])
    assert add_owner(url, data['p1']['token'], data['public_id'], data['flockr_owner']['u_id']) == 200

    # InputError:
    assert add_owner(url, data['p1']['token'], data['public_id'], data['flockr_owner']['u_id']) != 200

    assert rem_owner(url, data['flockr_owner']['token'], data['public_id'], data['p1']['u_id']) == 200

    # InputError:
    assert rem_owner(url, data['flockr_owner']['token'], data['public_id'], data['p1']['u_id']) != 200


def test_flockr_leaving_channel(url, data):
    '''
    Flockr members can leave channels but the channels must have an owner.
    '''

    join(url, data['flockr_owner']['token'], data['public_id'])
    assert leave(url, data['flockr_owner']['token'], data['public_id'])

    invite(url, data['p1']['token'], data['public_id'], data['p3']['u_id'])
    join(url, data['flockr_owner']['token'], data['public_id'])
    rem_owner(url, data['flockr_owner']['token'], data['public_id'], data['p1']['u_id'])

    # AccessError:
    assert leave(url, data['flockr_owner']['token'], data['public_id']) != 200
