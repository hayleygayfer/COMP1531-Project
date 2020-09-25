import auth
import channel
import channels
from data import data

# Returns either the token or u_id depending on first parameter 
def get_info_auth(data_type, email):
    return [ person[data_type] for person in data['users'] if person['email'] == email ][0]


# channel_invite returns True if success (SUBJECT TO CHANGE)
def test_channel_invite():
    # Person1 creates a channel
    auth.auth_register("person1@unsw.com", "pass1234", "Person", "One")
    auth.auth_login("person1@unsw.com", "pass1234")
    person1_id = get_info_auth('u_id', 'person1@unsw.com')
    token = get_info_auth('token', 'person1@unsw.com')
    ch_id = channels.channels_create(token, "MainChannel", "public")

    '''
    Users: Person1
    ch_id (Public) Members: Person1 (O)
    '''
    
    # Person1 invites other users (Person2)
    auth.auth_register("person2@gmail.com", "qwerty", "Person", "Two")
    person2_id = get_info_auth('u_id','person2@gmail.com')
    assert channel.channel_invite(token, ch_id, person2_id) == True

    '''
    Users: Person1, Person2
    ch_id (Public) Members: Person1 (O), Person2
    '''

    # Person1 invite a user that already exists in the channel
    assert channel.channel_invite(token, ch_id, person1_id) == False # Can't invite yourself
    assert channel.channel_invite(token, ch_id, person2_id) == False # Person2 already exists in channel

    # Invite a non-existant user to that channel
    assert channel.channel_invite(token, ch_id, 31415926) == False
    assert channel.channel_invite(token, ch_id, 4243) == False

    # Invite valid user to a non-existant channel
    assert channel.channel_invite(token, 75385, person2_id) == False

    # Create a new private channel and invite a new user to that channel
    ch2_id = channels.channels_create(token, "PrivateChannel", "private")
    auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")
    trump_id = get_info_auth('u_id', 'donaldtrump@america.com')
    
    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2
    ch2_id (Private) Members: Person1 (O)
    '''    
    
    assert channel.channel_invite(token, ch2_id, trump_id) == True
    assert channel.channel_invite(token, ch2_id, trump_id) == False # Invite twice error
    assert channel.channel_invite(token, ch_id, trump_id) == True

    channel.channel_addowner(token, ch_id, person2_id)

    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2 (O), Trump
    ch2_id (Private) Members:  Person1 (O), Trump
    '''

    # Inviting people depending on your owner status
    auth.auth_register("person3@hotmail.com", "lonelysad", "Person", "Three")
    person3_id = [ person['u_id'] for person in data['users'] if person['email'] == 'person3@hotmail.com' ][0]

    '''
    Users: Person1, Person2, Trump, Person3
    ch_id (Public) Members: Person1 (O), Person2 (O), Trump
    ch2_id (Private) Members:  Person1 (O), Trump
    '''

    token = get_info_auth('token', 'person2@gmail.com')
    assert channel.channel_invite(token, ch_id, person3_id) == True # Person2 can invite Person3 to ch_id
    token = get_info_auth('token', 'donaldtrump@america.com')
    assert channel.channel_invite(token, ch_id, person3_id) == True # Trump can't invite Person3 to ch2_id

    '''
    Users: Person1, Person2, Trump, Person3
    ch_id (Public) Members: Person1 (O), Person2 (O), Trump, Person3
    ch2_id (Private) Members:  Person1 (O), Trump
    '''


def test_channel_details():
    pass

def test_channel_messages():
    pass

def test_channel_leave():
    pass

# channel_join returns True if success (SUBJECT TO CHANGE)
def test_channel_join():
    # Get a user to create a public channel
    auth.auth_register("master@public.com", "iamthemaster", "Master", "Channel")
    auth.auth_login("master@public.com", "iamthemaster")
    token = get_info_auth('token', 'master@public.com')
    ch_id = channels.channels_create(token, "PublicChannel", "public")

    # Check whether a new user can join this channel
    auth.auth_register("servant@join.com", "iamaservant", "Channel", "Joiner")
    auth.auth_login("servant@join.com", "iamaservant")
    token = get_info_auth('token', 'servant@join.com')
    assert channel.channel_join(token, ch_id) == True

    auth.auth_register("newbie@dummies.com", "password", "Newbie", "Rick")
    auth.auth_login("newbie@dummies.com", "password")
    token = get_info_auth('token', 'newbie@dummies.com')
    assert channel.channel_join(token, ch_id) == True

    # Joining a private channel
    private_ch_id = channels.channels_create(token, "NewbiePrivate", "private")
    token = get_info_auth('token', 'master@public.com')
    assert channel.channel_join(token, private_ch_id) == False
    token = get_info_auth('token', 'servant@join.com')
    assert channel.channel_join(token, private_ch_id) == False

    # Joining a channel you're already in
    assert channel.channel_join(token, ch_id) == False
    token = get_info_auth('token', 'newbie@dummies.com')
    assert channel.channel_join(token, ch_id) == False

    # Leaving a public channel then joining again
    channel.channel_leave(token, ch_id)
    assert channel.channel_join(token, ch_id) == True
    token = get_info_auth('token', 'servant@join.com')
    channel.channel_leave(token, ch_id)
    assert channel.channel_join(token, ch_id) == True

    # Leaving a private channel then joining again
    token = get_info_auth('token', 'newbie@dummies.com')
    master_id = get_info_auth('u_id', 'master@public.com')
    channel.channel_invite(token, private_ch_id, master_id)
    
    token = get_info_auth('token', 'master@public.com')
    channel.channel_leave(token, private_ch_id)
    assert channel.channel_join(token, private_ch_id) == False


def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass


# IGNORE THIS
if __name__ == "__main__":
    u_id = get_info_auth('u_id', 'random@email.com')
    print(u_id)
    