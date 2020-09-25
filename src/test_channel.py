import auth
import channel
import channels
from data import data

# channel_invite returns True if success (SUBJECT TO CHANGE)
def test_channel_invite():
    # A user creates a channel
    auth.auth_register("channelcreator@unsw.com", "pass1234", "Channel", "Creator")
    auth.auth_login("channelcreator@unsw.com", "pass1234")
    token = [ person['token'] for person in data['users'] if person['email'] == 'channelcreator@unsw.com' ][0]
    ch_id = channels.channels_create(token, "ValidChannelName", "public")
    
    # Invite other users
    auth.auth_register("randomuser@gmail.com", "qwerty", "Random", "User")
    random_id = [ person['u_id'] for person in data['users'] if person['email'] == 'randomuser@gmail.com' ][0]
    assert channel.channel_invite(token, ch_id, random_id) == True

    # Invite a user that already exists in the channel
    creator_id = [ person['u_id'] for person in data['users'] if person['email'] == 'channelcreator@unsw.com' ][0]
    assert channel.channel_invite(token, ch_id, creator_id) == False # Can't invite yourself
    assert channel.channel_invite(token, ch_id, random_id) == False

    # Invite a non-existant user to that channel
    assert channel.channel_invite(token, ch_id, 31415926) == False
    assert channel.channel_invite(token, ch_id, 4243) == False

    # Invite valid user to a non-existant channel
    assert channel.channel_invite(token, 75385, random_id) == False

    # Create a new private channel and invite a new user to that channel
    ch_id2 = channels.channels_create(token, "AnotherChannelName", "private")
    auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")
    trump_id = [ person['u_id'] for person in data['users'] if person['email'] == 'donaldtrump@america.com' ][0]
    assert channel.channel_invite(token, ch_id2, trump_id) == True
    assert channel.channel_invite(token, ch_id2, trump_id) == False
    assert channel.channel_invite(token, ch_id, trump_id) == True

def test_channel_details():
    pass

def test_channel_messages():
    pass

def test_channel_leave():
    pass

def test_channel_join():
    pass

def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass