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
    # Create users
    auth.auth_register("person1@unsw.com", "pass1234", "Person", "One")
    auth.auth_login("person1@unsw.com", "pass1234")
    person1_id = get_info_auth('u_id', 'person1@unsw.com')
    p1_token = get_info_auth('token', 'person1@unsw.com')

    auth.auth_register("person2@gmail.com", "qwerty", "Person", "Two")
    person2_id = get_info_auth('u_id','person2@gmail.com')
    auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")
    trump_id = get_info_auth('u_id', 'donaldtrump@america.com')

    '''
    Users: Person1, Person2, Trump
    '''

    # Person1 creates a channel and invites other users

    ch_id = channels.channels_create(p1_token, "MainChannel", "public")
    assert channel.channel_invite(p1_token, ch_id, person2_id) == True

    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2
    '''

    # Person1 invite a user that already exists in the channel
    with pytest.raises(InputError):
        channel.channel_invite(p1_token, ch_id, person1_id) # Can't invite yourself
    with pytest.raises(InputError):
        channel.channel_invite(p1_token, ch_id, person2_id) # Person2 already exists in channel

    # Invite a non-existant user to that channel
    with pytest.raises(InputError):
        channel.channel_invite(p1_token, ch_id, 31415926)
    with pytest.raises(InputError):
        channel.channel_invite(p1_token, ch_id, 4243)

    # Invite valid user to a non-existant channel
    with pytest.raises(InputError):
        channel.channel_invite(p1_token, 75385, person2_id)

    # Now finally invite Trump to that channel
    assert channel.channel_invite(p1_token, ch_id, trump_id) == True
    
    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2, Trump
    '''

def test_channel_invite_AccessErrors():
    # Create users
    auth.auth_register("scottmorrison@auspm.com", "scomo", "Scott", "Morrison")
    auth.auth_login("scottmorrison@auspm.com", "scomo")
    scomo_token = get_info_auth('token', 'scottmorrison@auspm.com')

    auth.auth_register("tonyabbott@auspm.com", "idontcare", "Tony", "Abbott")
    auth.auth_login("tonyabbott@auspm.com", "idontcare")
    abbott_id = get_info_auth('u_id', 'tonyabbott@auspm.com')
    abbott_token = get_info_auth('token', 'tonyabbott@auspm.com')

    auth.auth_register("kevinrudd@auspm.com", "idontcare", "Kevin", "Rudd")
    auth.auth_login("kevinrudd@auspm.com", "idontcare")
    rudd_id = get_info_auth('u_id', 'kevinrudd@auspm.com')
    rudd_token = get_info_auth('token', 'kevinrudd@auspm.com')

    auth.auth_register("juliagillard@auspm.com", "idontcare", "Julia", "Gillard")
    auth.auth_login("juliagillard@auspm.com", "idontcare")
    gillard_id = get_info_auth('u_id', 'juliagillard@auspm.com')
    gillard_token = get_info_auth('token', 'juliagillard@auspm.com')

    # Scomo and Abbot creating channels
    pub_id = channels.channels_create(scomo_token, "PublicChannel", "public")
    prv_id = channels.channels_create(abbott_token, "PrivateChannel", "private")

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O)
    PrivateChannel: Abbott (O)
    '''

    # Inviting other users
    assert channel.channel_invite(abbott_token, prv_id, rudd_id) == True
    assert channel.channel_invite(scomo_token, pub_id, gillard_id) == True

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O), Gillard
    PrivateChannel: Abbott (O), Rudd
    '''

    # Regular members inviting other users
    with pytest.raises(AccessError):
        channel.channel_invite(rudd_token, prv_id, gillard_id) # Rudd cannot invite Gillard to private
    with pytest.raises(AccessError):
        channel.channel_invite(rudd_token, prv_id, abbott_id) # Rudd cannot invite Abbott to public (since Rudd is not a member)
    
    assert channel.channel_invite(gillard_token, pub_id, rudd_id) == True # Gillard can invite Rudd to public
    assert channel.channel_invite(rudd_token, prv_id, abbott_id) == True # NOW Rudd can invite Abbott

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
    # Create users
    auth.auth_register("mario@nintendo.com", "mammamia", "Mario", "Idk")
    auth.auth_login("mario@nintendo.com", "mammamia")
    mario_id = get_info_auth('u_id', 'mario@nintendo.com')
    mario_token = get_info_auth('token', 'mario@nintendo.com')

    auth.auth_register("luigi@nintendo.com", "letsgo", "Luigi", "Idk")
    auth.auth_login("luigi@nintendo.com", "letsgo")
    luigi_token = get_info_auth('token', 'luigi@nintendo.com')

    auth.auth_register("princesspeach@nintendo.com", "mushroom", "Peach", "Toadstool")
    auth.auth_login("princesspeach@nintendo.com", "mushroom")
    peach_token = get_info_auth('token', 'peach@nintendo.com')

    # Mario and Peach create a public and private channel respectively
    pub_ch_id = channels.channels_create(mario_token, "PublicChannel", "public")
    prv_ch_id = channels.channels_create(peach_token, "PrivateChannel", "private")

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O)
    PrivateChannel: Peach (O)
    '''

    # Check whether other users can join the public channel
    assert channel.channel_join(luigi_token, pub_ch_id) == True
    assert channel.channel_join(peach_token, pub_ch_id) == True

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O), Luigi, Peach
    PrivateChannel: Peach (O)
    '''

    # Joining a channel that does not exist
    with pytest.raises(InputError):
        channel.channel_join(luigi_token, 3474214)

    # Joining a private channel
    with pytest.raises(AccessError):
        channel.channel_join(mario_token, prv_ch_id) # Mario cannot join private
    with pytest.raises(AccessError):
        channel.channel_join(luigi_token, prv_ch_id) # Luigi cannot join private

    # Joining a channel you're already in
    with pytest.raises(InputError):
        channel.channel_join(peach_token, pub_ch_id) # Peach already in public

    # Leaving a public channel then joining again
    channel.channel_leave(peach_token, pub_ch_id)
    assert channel.channel_join(peach_token, pub_ch_id) == True # Peach can leave and enter again

    # Leaving a private channel then joining again
    channel.channel_invite(peach_token, prv_ch_id, mario_id)

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O), Luigi, Peach
    PrivateChannel: Peach (O), Mario
    '''

    channel.channel_leave(mario_token, prv_ch_id) # Mario has left private
    with pytest.raises(AccessError):
        channel.channel_join(mario_token, prv_ch_id) # He cannot join again


def test_channel_addowner():
    pass

def test_channel_removeowner():
    pass


# IGNORE THIS
if __name__ == "__main__":
    u_id = get_info_auth('u_id', 'random@email.com')
    print(u_id)
    