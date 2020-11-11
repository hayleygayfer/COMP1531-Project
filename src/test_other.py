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
    person1_id = auth.auth_register("person1@unsw.com", "pass1234", "Personone", "One")['u_id']
    p1_token = auth.auth_login("person1@unsw.com", "pass1234")['token']
    person2_id = auth.auth_register("person2@unsw.com", "pass1234", "Persontwo", "Two")['u_id']
    p2_token = auth.auth_login("person2@unsw.com", "pass1234")['token']

    channel1_id = channels_create(p1_token, "Channel1", True)['channel_id']
    channel2_id = channels_create(p1_token, "Channel2", True)['channel_id']

    msg1_id = msg.message_send(p1_token, channel1_id, "Message One ilovedogs")['message_id']
    msg2_id = msg.message_send(p1_token, channel2_id, "Message Two ilovecats")['message_id']

    return {
        'p1ID': person1_id,
        'p1t': p1_token,
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
    # Count the number of users
    assert len(d.data['users']) == 2

    assert clear() != None

    # Count users again
    assert len(d.data['users']) == 0


## USERS ALL ##

# Check if all users are displayed
def test_users_all_contents(userObject):
    assert len(users_all(userObject['p1t'])['users']) == 2
    assert users_all(userObject['p1t'])['users'][0]['u_id'] == userObject['p1ID']
    assert users_all(userObject['p1t'])['users'][1]['u_id'] == userObject['p2ID']


# Check if the contents for both users are identical
def test_users_all_comparison(userObject):
    assert users_all(userObject['p1t']) == users_all(userObject['p2t'])



## SEARCH ##

## VALID CASES

# Search for a message with that exact query
def test_search_exact(userObject):
    query_str = "Message One ilovedogs"
    msg_dict = search(userObject['p1t'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m1ID']

    query_str = "Message Two ilovecats"
    msg_dict = search(userObject['p1t'], query_str)['messages']
    assert msg_dict[0]['message_id'] == userObject['m2ID']

# Non-existant queries
def test_search_query_non_existant(userObject):
    assert search(userObject['p1t'], 'fish')['messages'] == []
    assert search(userObject['p1t'], 'ilovefish')['messages'] == []

# The search item is part of a message
def test_search_partly(userObject):
    assert len(search(userObject['p1t'], 'Message')['messages']) == 2
    assert len(search(userObject['p1t'], 'ilove')['messages']) == 2
    assert len(search(userObject['p1t'], 'cats')['messages']) == 1

# Query matches with message regardless of upper/lower/mixed cases
def test_search_ignore_case(userObject):
    assert len(search(userObject['p1t'], 'MESSAGE')['messages']) == 2
    assert len(search(userObject['p1t'], 'mEssAGe')['messages']) == 2

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

# Valid search queries must have at least 2 characters
def test_search_short(userObject):
    with pytest.raises(InputError):
        search(userObject['p1t'], 'M')

    with pytest.raises(InputError):
        search(userObject['p1t'], ' ')

    with pytest.raises(InputError):
        search(userObject['p1t'], '')


## ADMIN USER PERMISSION CHANGE ##

## VALID CASES

# A flockr owner can add someone else as a flockr owner
def test_make_flockr_owner(userObject):
    # Add p2 as a flockr owner
    assert admin_userpermission_change(userObject['p1t'], userObject['p2ID'], 1) != None

    # Check that they have flockr owner privilges e.g. joining a private channel
    private = channels_create(userObject['p1t'], "PRIVATE", False)['channel_id']

    assert ch.channel_join(userObject['p2t'], private)


# The original flockr owner can get their rights revoked by another flockr owner
def test_remove_original_flockr_owner(userObject):
    # Add p2 as a flockr owner
    assert admin_userpermission_change(userObject['p1t'], userObject['p2ID'], 1) != None

    # Remove flockr owner status from p1
    assert admin_userpermission_change(userObject['p2t'], userObject['p1ID'], 2) != None

    # Check that p1 has their flockr owner rights revoked by being unable to join a private channel

    private = channels_create(userObject['p2t'], 'PRIVATE', False)['channel_id']
    with pytest.raises(AccessError):
        ch.channel_join(userObject['p1t'], private)


## INVALID CASES

# Can't change permissions if you are not a flockr owner
def test_not_owner_permission_change(userObject):
    # p2 is a normal member
    with pytest.raises(AccessError):
        admin_userpermission_change(userObject['p2t'], userObject['p2ID'], 1)


# If you are the only flockr owner left, you cannot remove yourself as an owner
def test_last_flockr_owner(userObject):
    # P1 changes P2 to flockr owner
    assert admin_userpermission_change(userObject['p1t'], userObject['p2ID'], 1) != None
    # P2 changes P1 to member
    assert admin_userpermission_change(userObject['p2t'], userObject['p1ID'], 2) != None
    # p2 is the only flockr owner
    with pytest.raises(InputError):
        admin_userpermission_change(userObject['p2t'], userObject['p2ID'], 2)


# Permission does not exist
def test_invalid_permission(userObject):
    with pytest.raises(InputError):
        admin_userpermission_change(userObject['p1t'], userObject['p2ID'], 3)


# User_id does not exist
def test_invalid_uid(userObject):
    with pytest.raises(InputError):
        admin_userpermission_change(userObject['p1t'], 42, 1)


# User is already an owner/member
def test_redundant_perm_change(userObject):
    # P1 is already an owner
    with pytest.raises(InputError):
        admin_userpermission_change(userObject['p1t'], userObject['p1ID'], 1)

    # P2 is already a member
    with pytest.raises(InputError):
        admin_userpermission_change(userObject['p1t'], userObject['p2ID'], 2)


## INVALID TOKEN CASES

# Pass a dummy token of a non-user
def test_other_invalid_tokens(userObject):
    with pytest.raises(AccessError):
        users_all(123456)
    with pytest.raises(AccessError):
        search(7891011, 'Message')   
    with pytest.raises(AccessError):
        admin_userpermission_change(22352356, userObject['p2ID'], 2)