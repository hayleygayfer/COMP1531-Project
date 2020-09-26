import auth
import channel
import channels
import pytest
from error import InputError, AccessError
from data import data

# Returns either the token or u_id depending on first parameter 
def get_info_auth(data_type, email):
    return [ person[data_type] for person in data['users'] if person['email'] == email ][0]


# channel_invite returns True if success (SUBJECT TO CHANGE)
def test_channel_invite_InputErrors():
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
    with pytest.raises(InputError):
        channel.channel_invite(token, ch_id, person1_id) # Can't invite yourself
    with pytest.raises(InputError):
        channel.channel_invite(token, ch_id, person2_id) # Person2 already exists in channel

    # Invite a non-existant user to that channel
    with pytest.raises(InputError):
        channel.channel_invite(token, ch_id, 31415926)
    with pytest.raises(InputError):
        channel.channel_invite(token, ch_id, 4243)

    # Invite valid user to a non-existant channel
    with pytest.raises(InputError):
        channel.channel_invite(token, 75385, person2_id)

    # Invite a new user to that channel
    auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")
    trump_id = get_info_auth('u_id', 'donaldtrump@america.com')   
    assert channel.channel_invite(token, ch_id, trump_id) == True
    
    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2, Trump
    '''

def test_channel_invite_AccessErrors():
    # Scomo creates a public channel
    auth.auth_register("scottmorrison@auspm.com", "scomo", "Scott", "Morrison")
    auth.auth_login("scottmorrison@auspm.com", "scomo")
    token = get_info_auth('token', 'scottmorrison@auspm.com')
    pub_id = channels.channels_create(token, "PublicChannel", "public")

    # Abbott creates a private channel
    auth.auth_register("tonyabbott@auspm.com", "idontcare", "Tony", "Abbott")
    auth.auth_login("tonyabbott@auspm.com", "idontcare")
    abbott_id = get_info_auth('u_id', 'tonyabbott@auspm.com')
    token = get_info_auth('token', 'tonyabbott@auspm.com')
    prv_id = channels.channels_create(token, "PrivateChannel", "private")

    # Owners inviting other users
    auth.auth_register("kevinrudd@auspm.com", "idontcare", "Kevin", "Rudd")
    auth.auth_login("kevinrudd@auspm.com", "idontcare")
    rudd_id = get_info_auth('u_id', 'kevinrudd@auspm.com')
    assert channel.channel_invite(token, prv_id, rudd_id) == True

    auth.auth_register("juliagillard@auspm.com", "idontcare", "Julia", "Gillard")
    auth.auth_login("juliagillard@auspm.com", "idontcare")
    gillard_id = get_info_auth('u_id', 'juliagillard@auspm.com')
    token = get_info_auth('token', 'scottmorrison@auspm.com')
    assert channel.channel_invite(token, pub_id, gillard_id) == True

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O), Gillard
    PrivateChannel: Abbott (O), Rudd
    '''

    # Regular members inviting other users
    token = get_info_auth('token', 'kevinrudd@auspm.com')
    with pytest.raises(AccessError):
        channel.channel_invite(token, prv_id, gillard_id) # Rudd cannot invite Gillard to private
    with pytest.raises(AccessError):
        channel.channel_invite(token, prv_id, abbott_id) # Rudd cannot invite Abbott to public (since Rudd is not a member)
    
    token = get_info_auth('token', 'juliagillard@auspm.com')
    assert channel.channel_invite(token, pub_id, rudd_id) == True # Gillard can invite Rudd to public
    token = get_info_auth('token', 'kevinrudd@auspm.com')
    assert channel.channel_invite(token, prv_id, abbott_id) == True # NOW Rudd can invite Abbott

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O), Gillard, Rudd, Abbott
    PrivateChannel: Abbott (O), Rudd
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
    auth.auth_register("mario@nintendo.com", "mammamia", "Mario", "Idk")
    auth.auth_login("mario@nintendo.com", "mammamia")
    token = get_info_auth('token', 'mario@nintendo.com')
    pub_ch_id = channels.channels_create(token, "PublicChannel", "public")

    '''
    Users: Mario
    PublicChannel: Mario (O)
    '''

    # Check whether a new user can join this channel
    auth.auth_register("luigi@nintendo.com", "letsgo", "Luigi", "Idk")
    auth.auth_login("luigi@nintendo.com", "letsgo")
    token = get_info_auth('token', 'luigi@nintendo.com')
    assert channel.channel_join(token, pub_ch_id) == True

    auth.auth_register("princesspeach@nintendo.com", "mushroom", "Peach", "Toadstool")
    auth.auth_login("princesspeach@nintendo.com", "mushroom")
    token = get_info_auth('token', 'peach@nintendo.com')
    assert channel.channel_join(token, pub_ch_id) == True

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O), Luigi, Peach
    '''

    # Joining a channel that does not exist
    assert channel.channel_join(token, 3474214) == False

    # Joining a private channel
    prv_ch_id = channels.channels_create(token, "PrivateChannel", "private")
    token = get_info_auth('token', 'mario@nintendo.com')
    assert channel.channel_join(token, prv_ch_id) == False # Mario cannot join private
    token = get_info_auth('token', 'luigi@nintendo.com')
    assert channel.channel_join(token, prv_ch_id) == False # Luigi cannot join private

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O), Luigi, Peach
    PrivateChannel: Peach (O)
    '''

    # Joining a channel you're already in
    assert channel.channel_join(token, pub_ch_id) == False # Luigi already in public
    token = get_info_auth('token', 'princesspeach@nintendo.com')
    assert channel.channel_join(token, pub_ch_id) == False # Peach already in public

    # Leaving a public channel then joining again
    channel.channel_leave(token, pub_ch_id)
    assert channel.channel_join(token, pub_ch_id) == True # Peach can leave and enter again
    token = get_info_auth('token', 'luigi@nintendo.com')
    channel.channel_leave(token, pub_ch_id)
    assert channel.channel_join(token, pub_ch_id) == True # Luigi can leave and enter again

    # Leaving a private channel then joining again
    token = get_info_auth('token', 'princesspeach@nintendo.com')
    mario_id = get_info_auth('u_id', 'mario@nintendo.com')
    channel.channel_invite(token, prv_ch_id, mario_id)

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O), Luigi, Peach
    PrivateChannel: Peach (O), Mario
    '''
    
    token = get_info_auth('token', 'mario@nintendo.com')
    channel.channel_leave(token, prv_ch_id) # Mario has left private
    assert channel.channel_join(token, prv_ch_id) == False # He cannot join again


def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass


# IGNORE THIS
if __name__ == "__main__":
    u_id = get_info_auth('u_id', 'random@email.com')
    print(u_id)
    