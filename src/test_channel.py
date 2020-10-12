import auth
import channel as ch
import channels
import pytest

from error import InputError, AccessError
from other import clear

# Create fixture for setting up users and channels
@pytest.fixture
def data():
    clear()
    flockr_owner_id = auth.auth_register("almightygod@unsw.com", "firstuser", "Flockr", "Owner")['u_id']
    flockr_owner_token = auth.auth_login("almightygod@unsw.com", "firstuser")['token']
    person1_id = auth.auth_register("person1@unsw.com", "pass1234", "Personone", "One")['u_id']
    p1_token = auth.auth_login("person1@unsw.com", "pass1234")['token']
    person2_id = auth.auth_register("person2@unsw.com", "pass1234", "Persontwo", "Two")['u_id']
    p2_token = auth.auth_login("person2@unsw.com", "pass1234")['token']
    
    return {
        'flockr_owner_id': flockr_owner_id,
        'flockr_owner_token': flockr_owner_token,
        'p1_id': person1_id,
        'p1_token': p1_token,
        'p2_id': person2_id,
        'p2_token': p2_token,
        'p3_id': auth.auth_register("person3@unsw.com", "pass1234", "Personthree", "Three")['u_id'],
        'p3_token': auth.auth_login("person3@unsw.com", "pass1234")['token'],
        'p4_id': auth.auth_register("person4@unsw.com", "pass1234", "Personfour", "Four")['u_id'],
        'p4_token': auth.auth_login("person4@unsw.com", "pass1234")['token'],
        'p5_id': auth.auth_register("person5@unsw.com", "pass1234", "Personfive", "Five")['u_id'],
        'p5_token': auth.auth_login("person5@unsw.com", "pass1234")['token'],
        'public_id': channels.channels_create(p1_token, "PublicChannel", True)['channel_id'],
        'private_id': channels.channels_create(p2_token, "PrivateChannel", False)['channel_id']
    }

'''
Users: FlockrOwner (FO), Person1, Person2, Person3, Person4, Person5
Public Channel: Person1 (O)
Private Channel: Person2 (O)
'''


# Owners in either public or private channel can invite anyone who is not in that channel
def test_invite_success(data):
    assert ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    assert ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    assert ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])


# can't invite an existing member
def test_invite_existing(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])

    with pytest.raises(InputError):
        ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id']) # already in channel
        ch.channel_invite(data['p1_token'], data['public_id'], data['p1_id']) # inviter inviting themselves


# user must be a member of a channel to invite someone
def test_not_in_channel_invite(data):
    data['public_id'] = data['public_id']

    with pytest.raises(AccessError):
        ch.channel_invite(data['p2_token'], data['public_id'], data['p3_id'])
        # Person2 is not a member of the channel (Person1 created it)
    
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    assert ch.channel_invite(data['p2_token'], data['public_id'], data['p3_id']) # Now person2 can invite person3


# channel_details requires the person viewing the details to be a member of the channel
def test_details_authorisation(data):
    assert ch.channel_details(data['p1_token'], data['public_id'])
    assert ch.channel_details(data['p2_token'], data['private_id'])

    with pytest.raises(AccessError):
        ch.channel_details(data['p2_token'], data['public_id']) # p2 not in public channel
        ch.channel_details(data['p1_token'], data['private_id']) # p1 not in private channel
    
    ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    assert ch.channel_details(data['p1_token'], data['private_id']) # now person1 can view the details


# Checking whether all the necessary channel details are returned
def test_view_details(data):
    # Add more people to channels to fill in data
    ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])
    ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    ch.channel_join(data['p5_token'], data['public_id'])

    '''
    Public: Person1 (O), Person2, Person5
    Private: Person2 (O), Person3 (O), Person4
    '''
    ch.channel_leave(data['p2_token'], data['public_id'])

    # View details of public channel
    assert ch.channel_details(data['p1_token'], data['public_id'])['name'] == 'PublicChannel'
    assert ch.channel_details(data['p1_token'], data['public_id'])['owner_members'][0]['u_id'] == data['p1_id']
    assert ch.channel_details(data['p1_token'], data['public_id'])['owner_members'][0]['name_first'] == 'Personone'
    assert ch.channel_details(data['p1_token'], data['public_id'])['owner_members'][0]['name_last'] == 'One'

    assert ch.channel_details(data['p1_token'], data['public_id'])['all_members'][0]['u_id'] == data['p1_id']
    assert ch.channel_details(data['p1_token'], data['public_id'])['all_members'][0]['name_first'] == 'Personone'
    assert ch.channel_details(data['p1_token'], data['public_id'])['all_members'][0]['name_last'] == 'One'
    assert ch.channel_details(data['p1_token'], data['public_id'])['all_members'][1] == {} # Person2 left
    assert ch.channel_details(data['p1_token'], data['public_id'])['all_members'][2]['u_id'] == data['p5_id']

    # View details of private channel
    assert ch.channel_details(data['p2_token'], data['private_id'])['name'] == 'PrivateChannel'
    assert ch.channel_details(data['p2_token'], data['private_id'])['owner_members'][0]['u_id'] == data['p2_id']
    assert ch.channel_details(data['p2_token'], data['private_id'])['owner_members'][0]['name_first'] == 'Persontwo'
    assert ch.channel_details(data['p2_token'], data['private_id'])['owner_members'][0]['name_last'] == 'Two'
    assert ch.channel_details(data['p2_token'], data['private_id'])['owner_members'][1]['u_id'] == data['p3_id']

    assert ch.channel_details(data['p2_token'], data['private_id'])['all_members'][0]['u_id'] == data['p2_id']
    assert ch.channel_details(data['p2_token'], data['private_id'])['all_members'][0]['name_first'] == 'Persontwo'
    assert ch.channel_details(data['p2_token'], data['private_id'])['all_members'][0]['name_last'] == 'Two'
    assert ch.channel_details(data['p2_token'], data['private_id'])['all_members'][1]['u_id'] == data['p3_id']
    assert ch.channel_details(data['p2_token'], data['private_id'])['all_members'][2]['u_id'] == data['p4_id']


# must be a member of the channel to view messages
def test_view_messages_authorisation(data):
    assert ch.channel_messages(data['p1_token'], data['public_id'], 0)
    assert ch.channel_messages(data['p2_token'], data['private_id'], 0)

    with pytest.raises(AccessError):
        ch.channel_messages(data['p2_token'], data['public_id'], 0) # p2 not in public channel
        ch.channel_messages(data['p1_token'], data['private_id'], 0) # p1 not in private channel
    
    ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    assert ch.channel_messages(data['p1_token'], data['private_id'], 0) # now person1 can view the messages
    

# TODO: loading and reading channel messages (checking start/end)
def test_temp(data):
    pass
    

# leaving a channel
def test_leave_success(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    '''
    Public: Person1 (O), Person3 (O)
    Private: Person2 (O), Person4
    '''

    assert ch.channel_leave(data['p4_token'], data['private_id']) # Person4 can leave private
    assert ch.channel_leave(data['p1_token'], data['public_id']) # Person1 can leave public


# a channel owner cannot leave if they are the last remaining owner
def test_owner_leaving(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])

    with pytest.raises(InputError):
        ch.channel_leave(data['p1_token'], data['public_id']) # Person1 is the only owner

    # Add person3 as an owner
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    assert ch.channel_leave(data['p1_token'], data['public_id']) # Now Person1 can leave successfully

    with pytest.raises(InputError):
        ch.channel_leave(data['p3_token'], data['public_id']) # But Person3 can't


# a member can't leave a channel that they are not in
def test_leaving_diff_channel(data):
    ch.channel_join(data['p3_token'], data['public_id'])
    with pytest.raises(AccessError):
        ch.channel_leave(data['p3_token'], data['private_id'])


# anyone who is not already in the channel can join a public channel
def test_join_public(data):
    assert ch.channel_join(data['p2_token'], data['public_id'])
    assert ch.channel_join(data['p3_token'], data['public_id'])
    assert ch.channel_join(data['flockr_owner_token'], data['public_id'])


# No one can join a private channel 
def test_join_private(data):
    with pytest.raises(AccessError):
        ch.channel_join(data['p1_token'], data['private_id'])
        ch.channel_join(data['p3_token'], data['private_id'])


# an existing member can't join again
def test_join_but_existing(data):
    with pytest.raises(InputError):
        ch.channel_join(data['p1_token'], data['public_id'])

    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_join(data['p4_token'], data['public_id'])
    with pytest.raises(InputError):
        ch.channel_join(data['p3_token'], data['public_id'])
        ch.channel_join(data['p4_token'], data['public_id'])


def test_leave_then_join(data):
    ch.channel_join(data['p2_token'], data['public_id'])
    assert ch.channel_leave(data['p2_token'], data['public_id'])
    assert ch.channel_join(data['p2_token'], data['public_id'])
    assert ch.channel_leave(data['p2_token'], data['public_id'])


# a preexisting owner must add a normal member in that channel to be successful
def test_addowner_success(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    assert ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    assert ch.channel_addowner(data['p2_token'], data['private_id'], data['p1_id'])


# you must be an owner to add someone as an owner
def test_addowner_but_not_owner(data):
    ch.channel_join(data['p2_token'], data['public_id'])
    ch.channel_join(data['p3_token'], data['public_id'])

    with pytest.raises(AccessError):
        ch.channel_addowner(data['p2_token'], data['public_id'], data['p3_id']) # Person2 not an owner

    ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id']) # Now they are
    assert ch.channel_addowner(data['p2_token'], data['public_id'], data['p3_id'])


# you can't make an owner an owner
def test_addowner_when_already_owner(data):
    ch.channel_invite(data['p2_token'], data['private_id'], data['p3_id'])
    ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id'])
    with pytest.raises(InputError):
        ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id']) # Person3 is already an owner
        ch.channel_addowner(data['p3_token'], data['private_id'], data['p2_id']) # Person2 is already an owner


# Both users must be in the same channel
def test_addowner_but_not_in_channel(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])

    with pytest.raises(InputError):
        ch.channel_addowner(data['p1_token'], data['public_id'], data['p4_id']) # Person4 is not in public
        ch.channel_addowner(data['p2_token'], data['private_id'], data['p3_id']) # Person3 is not in private


# When there are multiple owners, then the newest memeber has the right to remove the creator as a member
def test_removeowner_success(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p1_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    ch.channel_addowner(data['p2_token'], data['private_id'], data['p1_id'])
    assert ch.channel_removeowner(data['p2_token'], data['public_id'], data['p1_id'])
    assert ch.channel_removeowner(data['p1_token'], data['private_id'], data['p2_id'])


# you must be an owner to reomve someone as an owner
def test_removeowner_but_not_owner(data):
    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_join(data['p4_token'], data['public_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    with pytest.raises(AccessError):
        ch.channel_removeowner(data['p4_token'], data['public_id'], data['p3_id']) # Person4 is not an owner


# you must remove an owner and not an ordinary member
def test_removeowner_for_ordinary_member(data):
    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_join(data['p4_token'], data['public_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    with pytest.raises(InputError):
        ch.channel_removeowner(data['p1_token'], data['public_id'], data['p4_id']) # Person4 is not an owner


# Both users must be in the same channel
def test_removeowner_but_not_in_channel(data):
    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_invite(data['p2_token'], data['private_id'], data['p4_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    ch.channel_addowner(data['p2_token'], data['private_id'], data['p4_id'])

    with pytest.raises(InputError):
        ch.channel_removeowner(data['p1_token'], data['public_id'], data['p4_id']) # Person4 is an owner in another channel


# Can't remove the yourself
def test_self_removeowner(data):
    ch.channel_join(data['p3_token'], data['public_id'])
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])

    with pytest.raises(InputError):
        ch.channel_removeowner(data['p1_token'], data['public_id'], data['p1_id']) # Can't remove yourself
    
    ch.channel_removeowner(data['p3_token'], data['public_id'], data['p3_id'])
    with pytest.raises(InputError):
        ch.channel_removeowner(data['p3_token'], data['public_id'], data['p3_id']) # Can't remove yourself (last owner)


# invalid channels raise InputErrors
def test_invalid_channels(data):
    with pytest.raises(InputError):
        ch.channel_invite(data['p1_token'], 4645, data['p3_id'])
    with pytest.raises(InputError):
        ch.channel_join(data['p3_token'], 24324)
    with pytest.raises(InputError):
        ch.channel_details(data['p1_token'], 3235325)
    with pytest.raises(InputError):
        ch.channel_messages(data['p1_token'], 36632523, 0)

    ch.channel_join(data['p3_token'], data['public_id'])
    with pytest.raises(InputError):
        ch.channel_leave(data['p3_token'], 523545)
    with pytest.raises(InputError):
        ch.channel_addowner(data['p1_token'], 3453453, data['p3_id'])
    
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    with pytest.raises(InputError):
        ch.channel_removeowner(data['p1_token'], 436356, data['p3_id'])


# Invalid U_ID raises InputErrors
def test_invalid_u_id(data):
    with pytest.raises(InputError):
        ch.channel_invite(data['p1_token'], data['public_id'], 3454356)

    ch.channel_invite(data['p1_token'], data['public_id'], data['p3_id'])

    with pytest.raises(InputError):
        ch.channel_addowner(data['p1_token'], data['public_id'], 4365346)
    
    ch.channel_addowner(data['p1_token'], data['public_id'], data['p3_id'])
    with pytest.raises(InputError):
        ch.channel_removeowner(data['p1_token'], data['public_id'], 2354542)


# invalid tokens raise AccessErrors
def test_invalid_tokens(data):
    ch.channel_invite(data['p1_token'], data['public_id'], data['p2_id'])

    with pytest.raises(AccessError):
        ch.channel_invite(2736273, data['public_id'], data['p3_id'])
    with pytest.raises(AccessError):
        ch.channel_join(56453, data['public_id'])
    with pytest.raises(AccessError):
        ch.channel_details(23532, data['public_id'])
    with pytest.raises(AccessError):
        ch.channel_leave(563464, data['public_id'])
    with pytest.raises(AccessError):
        ch.channel_addowner(23141, data['public_id'], data['p2_id'])

    ch.channel_addowner(data['p1_token'], data['public_id'], data['p2_id'])
    with pytest.raises(AccessError):
        ch.channel_removeowner(23141, data['public_id'], data['p2_id'])
    with pytest.raises(AccessError):
        ch.channel_messages(232414, data['public_id'], 0)


# The FlockR owner is allowed to add standard users as owners
# even if they are not an owner of the channel
def test_flockr_addowner_success(data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    ch.channel_join(data['p3_token'], data['public_id'])
    assert ch.channel_addowner(data['flockr_owner_token'], data['public_id'], data['p3_id'])


# FlockR owner must to be a member of the channel to remove an owner
# They don't necessarily have to be a channel owner 
def test_flockr_removeowner_success(data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    
    ch.channel_invite(data['p2_token'], data['private_id'], data['flockr_owner_id'])
    assert ch.channel_removeowner(data['flockr_owner_token'], data['private_id'], data['p2_id'])


# If the flockR owner is not part of the channel, they don't get any piviledges
def test_flockr_removeowner_but_not_member(data):
    with pytest.raises(AccessError):
        ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
        ch.channel_removeowner(data['flockr_owner_token'], data['private_id'], data['p2_id'])


# FlockR members are allowed to join private channels
def test_flockr_join_private(data):
    assert ch.channel_join(data['flockr_owner_token'], data['private_id'])
    assert ch.channel_leave(data['flockr_owner_token'], data['private_id'])
    assert ch.channel_join(data['flockr_owner_token'], data['private_id'])


# FlockR owners are allowed to invite anyone who is not currently in the private channel
# even when they are not an owner of the channel
def test_flockr_invite_private(data):
    ch.channel_invite(data['p2_token'], data['private_id'], data['flockr_owner_id'])
    assert ch.channel_invite(data['flockr_owner_token'], data['private_id'], data['p3_id'])


# Adding the FlockR owner as a channel owner doesn't change much
def test_add_flockr_as_owner(data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_addowner(data['p1_token'], data['public_id'], data['flockr_owner_id'])
    with pytest.raises(InputError):
        ch.channel_addowner(data['p1_token'], data['public_id'], data['flockr_owner_id'])

    assert ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    with pytest.raises(AccessError):
        ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])


# Flockr members can leave channels but the channels must have an owner
def test_flockr_leaving_channel(data):
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    assert ch.channel_leave(data['flockr_owner_token'], data['public_id'])

    # Leaving a channel with no owners
    ch.channel_invite(data['p1_id'], data['public_id'], data['p3_token'])
    ch.channel_join(data['flockr_owner_token'], data['public_id'])
    ch.channel_removeowner(data['flockr_owner_token'], data['public_id'], data['p1_id'])
    
    with pytest.raises(InputError):
        # If FlockR owner leaves then Person3 is the only member left and there are no owners
        ch.channel_leave(data['flockr_owner_token'], data['public_id'])


