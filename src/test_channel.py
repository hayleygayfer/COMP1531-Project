import auth
import channel
import channels

# channel_invite returns True if success (SUBJECT TO CHANGE)
def test_channel_invite():
    # A user creates a channel
    auth.auth_register("channelcreator@unsw.com", "pass1234", "Channel", "Creator")
    ''' token = <insert code to grab token> '''
    ch_id = channels.channels_create(token, "ValidChannelName", "public")
    
    # Invite other users
    auth.auth_register("randomuser@gmail.com", "qwerty", "Random", "User")
    ''' random_id = <insert code to grad u_id of random user> '''
    assert channel.channel_invite(token, ch_id, random_id) == True

    # Invite a user that already exists in the channel
    ''' creator_id = <insert code to grab u_id of channel creator> '''
    assert channel.channel_invite(token, ch_id, creator_id) == False # Can't invite yourself
    assert channel.channel_invite(token, ch_id, random_id) == False

    # Invite a non-existant user to that channel
    assert channel.channel_invite(token, ch_id, 31415926) == False
    assert channel.channel_invite(token, ch_id, 4243) == False

    # Invite valid user to a non-existant channel
    assert channel.channel_invite(token, 75385, random_id) == False

    # Create a new channel and invite a new user to that channel
    ch_id2 = channels.channels_create(token, "AnotherChannelName", "public")
    auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")
    ''' trump_id = <insert code to grab trump's u_id> '''
    assert channel.channel_invite(token, ch_id2, trump_id) == True
    assert channel.channel_invite(token, ch_id2, trump_id) == False
    assert channel.channel_invite(token, ch_id, trump_id) == True

    # Private channel??

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