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
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")
    # no channels created / joined
    assert channels.channels_list("person1@email.com") == {}

def test_user_in_no_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")
    # create user2
    auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login("person2@email.com", "password")
    # create user3
    auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login("person3@email.com", "password")

    # user1 creates a channel
    channels.channels_create("person1@email.com", "channel_1", True)
    # invites user2
    channel.channel_invite("person1@email.com", "channel_1", 2)
    # user3 is not in any channels
    assert channels.channels_list("person3@gmail.com") == []

def test_user_is_in_all_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")
    # create user2
    auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login("person2@email.com", "password")
    # create user3
    auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login("person3@email.com", "password")

    # user1 creates a channel
    channels.channels_create("person1@email.com", "channel_1", True)
    # user2 creates a channel
    channels.channels_create("person2@email.com", "channel_2", True)
    # user1 invites user2 to channel_1
    channel.channel_invite("person1@email.com", "channel_1", 2)
    # user1 and user2 invite user3 to both channels
    channel.channel_invite("person1@email.com", "channel_1", 3)
    channel.channel_invite("person2@email.com", "channel_2", 3)
    assert channels.channels_list("person3@gmail.com") == [
        {
            'channel_id': 1, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
                {
                    'u_id': 2,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },
        {
            'channel_id': 2, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': 2,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
                {
                    'u_id': 3,
                    'name_first': 'Person',
                    'name_last': 'Three'
                },
            ],
            'owner_members': [
                {
                    'u_id': 2,
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
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")
    # create user2
    auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login("person2@email.com", "password")
    # create user3
    auth.auth_register("person3@email.com", "password", "Person", "Three")
    auth.auth_login("person3@email.com", "password")

    # user1 creates a channel
    channels.channels_create("person1@email.com", "channel_1", True)
    # user2 creates a channel
    channels.channels_create("person2@email.com", "channel_2", True)
    # user1 invites user2 to channel_1
    channel.channel_invite("person1@email.com", "channel_1", 2)
    # user1 invites user3 to channel_1 channels
    channel.channel_invite("person1@email.com", "channel_1", 3)
    assert channels.channels_list("person3@gmail.com") == [
        {
            'channel_id': 1, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
                {
                    'u_id': 2,
                    'name_first': 'Person',
                    'name_last': 'Two'
                },
                {
                    'u_id': 3,
                    'name_first': 'Person',
                    'name_last': 'Three'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
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
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")

    # no channels exist
    assert channels.channels_listall("person1@email.com") == []

def test_total_channels():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")

    # user1 creates 3 channels
    channels.channels_create("person1@email.com", "channel_1", True)
    channels.channels_create("person1@email.com", "channel_2", True)
    channels.channels_create("person1@email.com", "channel_3", True)

    # 3 channels exist
    assert channels.channels_listall("person1@email.com") == [
        {
            'channel_id': 1, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
                {
            'channel_id': 2, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
                {
            'channel_id': 3, 
            'name': "channel_3", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
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
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")
    # create user2
    auth.auth_register("person2@email.com", "password", "Person", "Two")
    auth.auth_login("person2@email.com", "password")

    # user1 creates 3 channels
    channels.channels_create("person1@email.com", "channel_1", True)
    channels.channels_create("person1@email.com", "channel_2", True)
    channels.channels_create("person1@email.com", "channel_3", True)

    # user2 checks all channels
    assert channels.channels_listall("person2@email.com") == [
        {
            'channel_id': 1, 
            'name': "channel_1", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
                {
            'channel_id': 2, 
            'name': "channel_2", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },   
                {
            'channel_id': 3, 
            'name': "channel_3", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
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
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")

    with pytest.raises(InputError):
        channels.channels_create("person1@email.com", "channels____________1", True)

# VALID CASES #

def test_name_1_or_20_characters():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")

    assert channels.channels_create("person1@email.com", "channels___________1", True) == {'channel_id': 1}
    assert channels.channels_create("person1@email.com", "2", True) == {'channel_id': 2}


def test_public_private():
    clear()
    # create user1
    auth.auth_register("person1@email.com", "password", "Person", "One")
    auth.auth_login("person1@email.com", "password")

    channels.channels_create("person1@email.com", "channels_public", True)
    channels.channels_create("person1@email.com", "channels_private", False)

    assert channels.channels_listall("person1@email.com") == [
        {
            'channel_id': 1, 
            'name': "channel_public", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': True
        },  
        {
            'channel_id': 2, 
            'name': "channel_private", 
            'all_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                },
            ],
            'owner_members': [
                {
                    'u_id': 1,
                    'name_first': 'Person',
                    'name_last': 'One'
                }
            ],
            'is_public': False
        },   
    ]