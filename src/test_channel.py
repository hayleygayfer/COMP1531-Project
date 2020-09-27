import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from other import clear


# channel_invite returns a dictionary {is_success: True/False}
def test_channel_invite_InputErrors():
    clear()
    # Create users
    person1_id = auth.auth_register("person1@unsw.com", "pass1234", "Person", "One")['u_id']
    p1_token = auth.auth_login("person1@unsw.com", "pass1234")['token']

    person2_id = auth.auth_register("person2@gmail.com", "qwerty", "Person", "Two")['u_id']
    trump_id = auth.auth_register("donaldtrump@america.com", "idklol", "Donald", "Trump")['u_id']

    '''
    Users: Person1, Person2, Trump
    '''

    # Person1 creates a channel and invites other users
    ch_id = channels.channels_create(p1_token, "MainChannel", "public")
    assert channel.channel_invite(p1_token, ch_id, person2_id)['is_success'] == True

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
    assert channel.channel_invite(p1_token, ch_id, trump_id)['is_success'] == True
    
    '''
    Users: Person1, Person2, Trump
    ch_id (Public) Members: Person1 (O), Person2, Trump
    '''

def test_channel_invite_AccessErrors():
    clear()
    # Create users
    auth.auth_register("scottmorrison@auspm.com", "scomo", "Scott", "Morrison")
    scomo_token = auth.auth_login("scottmorrison@auspm.com", "scomo")['token']

    abbott_id = auth.auth_register("tonyabbott@auspm.com", "idontcare", "Tony", "Abbott")['u_id']
    abbott_token = auth.auth_login("tonyabbott@auspm.com", "idontcare")['token']

    rudd_id = auth.auth_register("kevinrudd@auspm.com", "idontcare", "Kevin", "Rudd")['u_id']
    rudd_token = auth.auth_login("kevinrudd@auspm.com", "idontcare")['token']

    gillard_id = auth.auth_register("juliagillard@auspm.com", "idontcare", "Julia", "Gillard")['u_id']
    gillard_token = auth.auth_login("juliagillard@auspm.com", "idontcare")['token']

    # Scomo and Abbot creating channels
    pub_id = channels.channels_create(scomo_token, "PublicChannel", "public")
    prv_id = channels.channels_create(abbott_token, "PrivateChannel", "private")

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O)
    PrivateChannel: Abbott (O)
    '''

    # Inviting other users
    assert channel.channel_invite(abbott_token, prv_id, rudd_id)['is_success'] == True
    assert channel.channel_invite(scomo_token, pub_id, gillard_id)['is_success'] == True

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
    
    assert channel.channel_invite(gillard_token, pub_id, rudd_id)['is_success'] == True # Gillard can invite Rudd to public
    assert channel.channel_invite(rudd_token, prv_id, abbott_id)['is_success'] == True # NOW Rudd can invite Abbott

    '''
    Users: Scomo, Abbott, Rudd, Gillard
    PublicChannel: Scomo (O), Gillard, Rudd, Abbott
    PrivateChannel: Abbott (O), Rudd
    '''


def test_channel_details():
    clear()

def test_channel_messages():
    clear()

# channel_leave returns a dictionary {is_success: True/False}
def test_channel_leave():
    clear()
    # Create users
    auth.auth_register("diglett@pokemon.com", "arenatrap", "Diglett", "Pokemon")
    diglett_token = auth.auth_login("diglett@pokemon.com", "arenatrap")['token']

    ponyta_id = auth.auth_register("ponyta@pokemon.com", "horndrillXD", "Ponyta", "Pokemon")['u_id']
    ponyta_token = auth.auth_login("ponyta@pokemon.com", "horndrillXD")['token']

    auth.auth_register("gyarados@pokemon.com", "notadragontype", "Gyarados", "Pokemon")
    gyarados_token = auth.auth_login("gyarados@pokemon.com", "notadragontype")['token']

    auth.auth_register("dratini@pokemon.com", "notawatertype", "Dratini", "Pokemon")
    dratini_token = auth.auth_login("dratini@pokemon.com", "notawatertype")['token']

    # Users create and join channels
    moleID = channels.channels_create(diglett_token, "MoleChannel", "public")
    splashID = channels.channels_create(gyarados_token, "SplashChannel", "public")
    channel.channel_join(ponyta_token, splashID)
    channel.channel_join(dratini_token, splashID)

    '''
    MoleChannel: Diglett (O)
    SplashChannel: Gyarados (O), Ponyta, Dratini
    '''

    # Ensure Ponyta can leave
    assert channel.channel_leave(ponyta_token, splashID)['is_success'] == True
    channel.channel_join(ponyta_token, moleID)

    '''
    MoleChannel: Diglett (O), Ponyta
    SplashChannel: Gyarados (O), Dratini
    '''

    # Leaving a channel you're not in
    with pytest.raises(AccessError):
        channel.channel_leave(ponyta_token, splashID) # Ponyta is not in Splash
    with pytest.raises(AccessError):
        channel.channel_leave(dratini_token, moleID) # Dratini is not in Mole

    # Channels that don't exist
    with pytest.raises(InputError):
        channel.channel_leave(ponyta_token, 82372873)
    with pytest.raises(InputError):
        channel.channel_leave(dratini_token, 9374)

    # Owners leaving channels
    with pytest.raises(InputError):
        channel.channel_leave(diglett_token, moleID) # If diglett leaves there are no owners
    channel.channel_addowner(diglett_token, moleID, ponyta_id)
    assert channel.channel_leave(diglett_token, moleID)['is_success'] == True # NOW Diglett can leave since Ponyta is an owner

    '''
    MoleChannel: Ponyta (O)
    SplashChannel: Gyarados (O), Dratini
    '''

# channel_join returns a dictionary {is_success: True/False}
def test_channel_join():
    clear()
    # Create users
    mario_id = auth.auth_register("mario@nintendo.com", "mammamia", "Mario", "Idk")['u_id']
    mario_token = auth.auth_login("mario@nintendo.com", "mammamia")['token']

    auth.auth_register("luigi@nintendo.com", "letsgo", "Luigi", "Idk")
    luigi_token = auth.auth_login("luigi@nintendo.com", "letsgo")['token']

    auth.auth_register("princesspeach@nintendo.com", "mushroom", "Peach", "Toadstool")
    peach_token = auth.auth_login("princesspeach@nintendo.com", "mushroom")['token']

    # Mario and Peach create a public and private channel respectively
    pub_ch_id = channels.channels_create(mario_token, "PublicChannel", "public")
    prv_ch_id = channels.channels_create(peach_token, "PrivateChannel", "private")

    '''
    Users: Mario, Luigi, Peach
    PublicChannel: Mario (O)
    PrivateChannel: Peach (O)
    '''

    # Check whether other users can join the public channel
    assert channel.channel_join(luigi_token, pub_ch_id)['is_success'] == True
    assert channel.channel_join(peach_token, pub_ch_id)['is_success'] == True

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
    assert channel.channel_join(peach_token, pub_ch_id)['is_success'] == True # Peach can leave and enter again

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
    clear()
    # Create users
    comp_id = auth.auth_register("compgod@unsw.edu", "computerscience", "Comp", "God")['u_id']
    comp_token = auth.auth_login("compgod@unsw.edu", "computerscience")['token']

    math_id = auth.auth_register("mathgod@unsw.edu", "calculus", "Math", "God")['u_id']
    math_token = auth.auth_login("mathgod@unsw.edu", "calculus")['token']

    engg_id = auth.auth_register("enggod@unsw.edu", "engineering", "Eng", "God")['u_id']
    engg_token = auth.auth_login("enggod@unsw.edu", "engineering")['token']

    # Creating channels and adding users
    gods_channel_id = channels.channels_create(comp_token, "TheGods", "public")
    alt_channel_id = channels.channels_create(math_id, "Alternate", "public")
    channel.channel_invite(comp_token, gods_channel_id, math_id)
    channel.channel_invite(comp_token, gods_channel_id, engg_id)
    channel.channel_invite(math_token, gods_channel_id, engg_id)

    '''
    GodsChannel: Comp (O), Math, Eng
    AltChannel: Math (O), Eng
    '''
    
    # Adding owners without access permission
    with pytest.raises(AccessError):
        channel.channel_addowner(engg_token, gods_channel_id, math_id) # Eng cant add Math as owner

    # Adding owners success
    assert channel.channel_addowner(comp_token, gods_channel_id, math_id)['is_success'] == True
    assert channel.channel_addowner(math_token, alt_channel_id, engg_id)['is_success'] == True
    
    '''
    GodsChannel: Comp (O), Math (O), Eng
    AltChannel: Math (O), Eng (O)
    '''

    # Adding owners when they are already owners
    with pytest.raises(InputError):
        channel.channel_addowner(math_token, gods_channel_id, comp_id) # Comp is an owner of GodsChannel by default
    with pytest.raises(InputError):
        channel.channel_addowner(comp_token, gods_channel_id, math_id) # Math is already an owner of GodsChannel
    with pytest.raises(InputError):
        channel.channel_addowner(engg_token, alt_channel_id, math_id) # Math is an owner of AltChannel by default

    # Making yourself an owner
    with pytest.raises(InputError):
        channel.channel_addowner(comp_token, gods_channel_id, comp_id)
    with pytest.raises(AccessError):
        channel.channel_addowner(engg_token, gods_channel_id, engg_id)

    # Making someone who is not in the channel an owner
    with pytest.raises(InputError):
        channel.channel_addowner(math_token, alt_channel_id, comp_id) # Comp is not in AltChannel

    # After they join, then the above step is successful
    channel.channel_join(comp_id, alt_channel_id)
    assert channel.channel_addowner(math_token, alt_channel_id, comp_id)['is_success'] == True

    # Testing with invalid channels/users
    with pytest.raises(InputError):
        channel.channel_addowner(comp_token, gods_channel_id, 64476)
    with pytest.raises(InputError):
        channel.channel_addowner(comp_token, 24874, engg_id)

    '''
    GodsChannel: Comp (O), Math (O), Eng
    AltChannel: Math (O), Eng (O), Comp (O)
    '''


def test_channel_removeowner():
    clear()


# IGNORE THIS
if __name__ == "__main__":
    u_id = auth.auth_register("person1@unsw.com", "pass1234", "Person", "One")['u_id']
    print(u_id)
    u2_id = auth.auth_register("person2@unsw.com", "pass1234", "Person", "One")['u_id']
    print(u2_id)
