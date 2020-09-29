import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from data import data
from other import clear

### channels_list ###

# VALID CASES #
def test_no_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")
    # no channels created / joined
    assert channels.channels_list(token1) == {}

def test_user_in_no_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")
    # create user2
    (u2_id, token2) = auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login(token2, "password")
    # create user3
    (u3_id, token3) = auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login(token3, "password")

    # user1 creates a channel
    channels.channels_create(token1, "channel_1", True)
    # invites user2
    channel.channel_invite(token1, "channel_1", u2_id)
    # user3 is not in any channels
    assert channels.channels_list(token3) == []

def test_user_is_in_all_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")
    # create user2
    (u2_id, token2) = auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login(token2, "password")
    # create user3
    (u3_id, token3) = auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login(token3, "password")

    # user1 creates a channel
    c1_id = channels.channels_create(token1, "channel_1", True)
    # user2 creates a channel
    c2_id = channels.channels_create(token2, "channel_2", True)
    # user1 invites user2 to channel_1
    channel.channel_invite(token1, "channel_1", u2_id)
    # user1 and user2 invite user3 to both channels
    channel.channel_invite(token1, "channel_1", u3_id)
    channel.channel_invite(token2, "channel_2", u3_id)
    assert channels.channels_list(token3) == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
                {
                    'u_id': u2_id,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },
        {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': u2_id,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
                {
                    'u_id': u3_id,
                    'name_first': 'Person',
                    'name_last': 'Three'
                },
            ],
            'owner_members': [
                {
                    'u_id': u2_id,
                    'name_first': 'Person',
                    'name_last': 'Two'
                }
            ],
            'is_public': True
        },
    ]

def test_user_is_in_some_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")
    # create user2
    (u2_id, token2) = auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login(token2, "password")
    # create user3
    (u3_id, token3) = auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login(token3, "password")

    # user1 creates a channel
    c1_id = channels.channels_create(token1, "channel_1", True)
    # user2 creates a channel
    channels.channels_create(token2, "channel_2", True)
    # user1 invites user2 to channel_1
    channel.channel_invite(token1, "channel_1", u2_id)
    # user1 invites user3 to channel_1 channels
    channel.channel_invite(token1, "channel_1", u3_id)
    assert channels.channels_list(token3) == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
                {
                    'u_id': u2_id,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
                {
                    'u_id': u3_id,
                    'name_first': 'Person',
                    'name_last': 'Three'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },
    ]

### channels_listall ###

# VALID CASES #
def test_no_total_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")

    # no channels exist
    assert channels.channels_listall(token1) == []

def test_total_channels():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")

    # user1 creates 3 channels
    c1_id = channels.channels_create(token1, "channel_1", True)
    c2_id = channels.channels_create(token1, "channel_2", True)
    c3_id = channels.channels_create(token1, "channel_3", True)

    # 3 channels exist
    assert channels.channels_listall(token1) == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
                {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
                {
            'channel_id': c3_id, 
            'name': "channel_3", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
    ]

def test_total_channels_not_created_by_user():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")
    # create user2
    (u2_id, token2) = auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login(token2, "password")

    # user1 creates 3 channels
    c1_id = channels.channels_create(token1, "channel_1", True)
    c2_id = channels.channels_create(token1, "channel_2", True)
    c3_id = channels.channels_create(token1, "channel_3", True)

    # user2 checks all channels
    assert channels.channels_listall(token2) == [
        {
            'channel_id': c1_id, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
                {
            'channel_id': c2_id, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
                {
            'channel_id': c3_id, 
            'name': "channel_3", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
    ]

### channels_create ###

# EXCEPTIONS #
def test_name_over_20_characters():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")

    with pytest.raises(InputError):
        channels.channels_create(token1, "channels____________1", True)

# VALID CASES #

def test_name_1_or_20_characters():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")

    assert channels.channels_create(token1, "channels___________1", True) == {'channel_id': 1}
    assert channels.channels_create(token1, "2", True) == {'channel_id': 2}


def test_public_private():
    clear()
    # create user1
    (u1_id, token1) = auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login(token1, "password")

    cpublic_id = channels.channels_create(token1, "channels_public", True)
    cprivate_id = channels.channels_create(token1, "channels_private", False)

    assert channels.channels_listall(token1) == [
        {
            'channel_id': cpublic_id, 
            'name': "channel_public", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
        {
            'channel_id': cprivate_id, 
            'name': "channel_private", 
            'all_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': u1_id,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': False
        },   
    ]