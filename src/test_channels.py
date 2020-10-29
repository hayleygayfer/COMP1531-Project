import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from other import clear

### channels_list ###

# EXCEPTIONS #
def test_invalid_user():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']

    with pytest.raises(AccessError):
        channels.channels_list(1111)

# VALID CASES #
def test_no_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']
    print(token1)
    # no channels created / joined
    assert channels.channels_list(token1)['channels'] == []


def test_user_in_no_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']
    # create user2
    u2_id = auth.auth_register("person2@email.com", "password", "Person", "Two")['u_id']
    auth.auth_login("person2@email.com", "password")
    # create user3
    auth.auth_register("person3@email.com", "password", "Person", "Three")
    token3 = auth.auth_login("person3@email.com", "password")['token']

    # user1 creates a channel
    ch_id = channels.channels_create(token1, "channel_1", True)['channel_id']
    # invites user2
    channel.channel_invite(token1, ch_id, u2_id)
    # user3 is not in any channels
    assert channels.channels_list(token3)['channels'] == []

def test_user_is_in_all_channels():
    clear()
    # create user1
    u1_id = auth.auth_register("person1@email.com", "password", "Person", "One")['u_id']
    token1 = auth.auth_login("person1@email.com", "password")['token']
    # create user2
    u2_id = auth.auth_register("person2@email.com", "password", "Person", "Two")['u_id']
    token2 = auth.auth_login("person2@email.com", "password")['token']
    # create user3
    u3_id = auth.auth_register("person3@email.com", "password", "Person", "Three")['u_id']
    token3 = auth.auth_login("person3@email.com", "password")['token']

    # user1 creates a channel
    c1_id = channels.channels_create(token1, "channel_1", True)['channel_id']
    # user2 creates a channel
    c2_id = channels.channels_create(token2, "channel_2", True)['channel_id']
    # user1 invites user2 to channel_1
    channel.channel_invite(token1, c1_id, u2_id)
    # user1 and user2 invite user3 to both channels
    channel.channel_invite(token1, c1_id, u3_id)
    channel.channel_invite(token2, c2_id, u3_id)
    assert channels.channels_list(token3)['channels'] == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [u1_id, u2_id, u3_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },
        {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [u2_id, u3_id],
            'owner_members': [u2_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },
    ]

def test_user_is_in_some_channels():
    clear()
    # create user1
    u1_id = auth.auth_register("person1@email.com", "password", "Person", "One")['u_id']
    token1 = auth.auth_login("person1@email.com", "password")['token']
    # create user2
    u2_id = auth.auth_register("person2@email.com", "password", "Person", "Two")['u_id']
    token2 = auth.auth_login("person2@email.com", "password")['token']
    # create user3
    u3_id = auth.auth_register("person3@email.com", "password", "Person", "Three")['u_id']
    token3 = auth.auth_login("person3@email.com", "password")['token']

    # user1 creates a channel
    c1_id = channels.channels_create(token1, "channel_1", True)['channel_id']
    # user2 creates a channel
    channels.channels_create(token2, "channel_2", True)
    # user1 invites user2 to channel_1
    channel.channel_invite(token1, c1_id, u2_id)
    # user1 invites user3 to channel_1 channels
    channel.channel_invite(token1, c1_id, u3_id)
    assert channels.channels_list(token3)['channels'] == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [u1_id, u2_id, u3_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },
    ]
    # user2 and user3 will not see the same list
    assert channels.channels_list(token2) != channels.channels_list(token3)
    # user1 and user3 will see the same list
    assert channels.channels_list(token1) == channels.channels_list(token3)

### channels_listall ###

# EXCEPTIONS #
def test_invalid_user_all():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']

    with pytest.raises(AccessError):
        channels.channels_listall(1111)

# VALID CASES #
def test_no_total_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']

    # no channels exist
    assert channels.channels_listall(token1)['channels'] == []

def test_total_channels():
    clear()
    # create user1
    u1_id = auth.auth_register("person1@email.com", "password", "Person", "One")['u_id']
    token1 = auth.auth_login("person1@email.com", "password")['token']

    # user1 creates 3 channels
    c1_id = channels.channels_create(token1, "channel_1", True)['channel_id']
    c2_id = channels.channels_create(token1, "channel_2", True)['channel_id']
    c3_id = channels.channels_create(token1, "channel_3", True)['channel_id']

    # 3 channels exist
    assert channels.channels_listall(token1)['channels'] == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },  
                {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },   
                {
            'channel_id': c3_id, 
            'name': "channel_3", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },   
    ]
    # check that user1 is in all channels
    assert channels.channels_listall(token1) == channels.channels_list(token1)

def test_total_channels_not_created_by_user():
    clear()
    # create user1
    u1_id = auth.auth_register("person1@email.com", "password", "Person", "One")['u_id']
    token1 = auth.auth_login("person1@email.com", "password")['token']
    # create user2
    auth.auth_register("person2@email.com", "password", "Person", "Two")
    token2 = auth.auth_login("person2@email.com", "password")['token']

    # user1 creates 3 channels
    c1_id = channels.channels_create(token1, "channel_1", True)['channel_id']
    c2_id = channels.channels_create(token1, "channel_2", True)['channel_id']
    c3_id = channels.channels_create(token1, "channel_3", True)['channel_id']

    # user2 checks all channels
    assert channels.channels_listall(token2)['channels'] == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },  
                {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },   
                {
            'channel_id': c3_id, 
            'name': "channel_3", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },   
    ]
    # user1 and user2 see the same list
    assert channels.channels_listall(token1) == channels.channels_listall(token2)

### channels_create ###

# EXCEPTIONS #
def test_name_over_20_characters():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']

    with pytest.raises(InputError):
        channels.channels_create(token1, "channels____________1", True)

def test_invalid_token():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")['token']

    with pytest.raises(AccessError):
        channels.channels_create("not_valid", "channel_1", True)

# VALID CASES #

def test_name_1_or_20_characters():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    token1 = auth.auth_login("person1@email.com", "password")['token']

    assert channels.channels_create(token1, "channels___________1", True) != None
    assert channels.channels_create(token1, "2", True) != None


def test_public_private():
    clear()
    # create user1
    u1_id = auth.auth_register("person1@email.com", "password", "Person", "One")['u_id']
    token1 = auth.auth_login("person1@email.com", "password")['token']

    cpublic_id = channels.channels_create(token1, "channels_public", True)['channel_id']
    print(cpublic_id)
    cprivate_id = channels.channels_create(token1, "channels_private", False)['channel_id']
    print(cprivate_id)

    assert channels.channels_listall(token1)['channels'] == [
        {
            'channel_id': cpublic_id, 
            'name': "channels_public", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': True,
            'messages': [],
            'message_count': 0
        },  
        {
            'channel_id': cprivate_id, 
            'name': "channels_private", 
            'all_members': [u1_id],
            'owner_members': [u1_id],
            'is_public': False,
            'messages': [],
            'message_count': 0
        },   
    ]
