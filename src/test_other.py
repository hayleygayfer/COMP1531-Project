import auth
import channel as ch
from channels import channels_create
import message as msg
from other import clear, users_all, admin_userpermission_change, search

import pytest
import data as d
from error import InputError, AccessError

# Create fixture
@pytest.fixture
def userObject():
    clear()
    flockr_owner_id = auth.auth_register("almightygod@unsw.com", "firstuser", "Flockr", "Owner")['u_id']
    flockr_owner_token = auth.auth_login("almightygod@unsw.com", "firstuser")['token']
    person2_id = auth.auth_register("person2@unsw.com", "pass1234", "Persontwo", "Two")['u_id']
    p2_token = auth.auth_login("person2@unsw.com", "pass1234")['token']

    channel1_id = channels_create(flockr_owner_token, "Channel1", True)['channel_id']
    channel2_id = channels_create(flockr_owner_token, "Channel2", True)['channel_id']

    msg1_id = msg.message_send(flockr_owner_token, channel1_id, "Message One ilovedogs")['message_id']
    msg2_id = msg.message_send(flockr_owner_token, channel2_id, "Message Two ilovecats")['message_id']

    return {
        'fID': flockr_owner_id,
        'ft': flockr_owner_token,
        'p2ID': person2_id,
        'p2t': p2_token,
        'c1ID': channel1_id,
        'c2ID': channel2_id,
        'm1ID': msg1_id,
        'm2ID': msg2_id
    }

## CLEAR ##

# Clear removes all user and channel data from the data structure
def test_clear(userObject):
    assert len(d.data['users']) == 2
    assert clear() != None
    assert len(d.data['users']) == 0


## USERS ALL ##

# Check if all users are displayed
def test_users_all_contents(userObject):
    assert len(users_all(userObject['ft'])['users']) == 2
    assert users_all(userObject['ft'])['users'][0]['u_id'] == userObject['fID']
    assert users_all(userObject['ft'])['users'][1]['u_id'] == userObject['p2ID']


# Check if the contents for both users are identical
def test_users_all_comparison(userObject):
    assert users_all(userObject['ft']) == users_all(userObject['p2t'])



## SEARCH ##

## VALID CASES

# Search for a message with that exact query
def test_search_exact(userObject):
    query_str = "Message One ilovedogs"
    msg_dict = search(userObject['ft'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m1ID']

    query_str = "Message Two ilovecats"
    msg_dict = search(userObject['ft'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m2ID']

# Non-existant queries
def test_search_query_non_existant(userObject):
    assert search(userObject['ft'], 'fish')['messages'] == []
    assert search(userObject['ft'], 'ilovefish')['messages'] == []

# The search item is part of a message
def test_search_partly(userObject):
    assert len(search(userObject['ft'], 'Message')['messages']) == 2
    assert len(search(userObject['ft'], 'ilove')['messages']) == 2
    assert len(search(userObject['ft'], 'cats')['messages']) == 1

# Query matches with message regardless of upper/lower/mixed cases
def test_search_ignore_case(userObject):
    assert len(search(userObject['ft'], 'MESSAGE')['messages']) == 2
    assert len(search(userObject['ft'], 'mEssAGe')['messages']) == 2

# More search results become available whenyou join multiple channels
def test_search_not_in_channel(userObject):
    assert len(search(userObject['p2t'], 'Message')['messages']) == 0
    
    # Join a channel
    ch.channel_join(userObject['p2t'], userObject['c1ID'])
    assert len(search(userObject['p2t'], 'Message')['messages']) == 1

    # Join another
    ch.channel_join(userObject['p2t'], userObject['c2ID'])
    assert len(search(userObject['p2t'], 'Message')['messages']) == 2


## INVALID CASES

# Not enough characters for a valid search
def test_search_short(userObject):
    with pytest.raises(InputError):
        search(userObject['ft'], 'M')

    with pytest.raises(InputError):
        search(userObject['ft'], ' ')

    with pytest.raises(InputError):
        search(userObject['ft'], '')



## INVALID TOKEN CASES

# Pass a dummy token of a non-user
def test_other_invalid_tokens():
    with pytest.raises(AccessError):
        users_all(123456)
    with pytest.raises(AccessError):
        search(7891011, 'Message')