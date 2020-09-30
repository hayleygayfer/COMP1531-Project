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
    ch_id = channels.channels_create(p1_token, "MainChannel", True)['channel_id']
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
    auth.auth_register("scottmorrison@auspm.com", "iamscomo", "Scott", "Morrison")
    scomo_token = auth.auth_login("scottmorrison@auspm.com", "iamscomo")['token']

    abbott_id = auth.auth_register("tonyabbott@auspm.com", "idontcare", "Tony", "Abbott")['u_id']
    abbott_token = auth.auth_login("tonyabbott@auspm.com", "idontcare")['token']

    rudd_id = auth.auth_register("kevinrudd@auspm.com", "idontcare", "Kevin", "Rudd")['u_id']
    rudd_token = auth.auth_login("kevinrudd@auspm.com", "idontcare")['token']

    gillard_id = auth.auth_register("juliagillard@auspm.com", "idontcare", "Julia", "Gillard")['u_id']
    gillard_token = auth.auth_login("juliagillard@auspm.com", "idontcare")['token']

    # Scomo and Abbot creating channels
    pub_id = channels.channels_create(scomo_token, "PublicChannel", True)['channel_id']
    prv_id = channels.channels_create(abbott_token, "PrivateChannel", False)['channel_id']

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

# channel_leave returns a dictionary { name: , owner_members, all_members }
def test_channel_details():
    clear()
    # Create users
    scarecrow_ID = auth.auth_register("scarecrow@wizardofoz.com", "wantsbrain", "scarecrow", "wizardofoz")['u_id']
    scarecrow_token = auth.auth_login("scarecrow@wizardofoz.com", "wantsbrain")['token']

    auth.auth_register("tinman@wizardofoz.com", "wantsheard", "tinman", "wizardofoz")
    tinman_token = auth.auth_login("tinman@wizardofoz.com", "wantsheard")['token']

    croardylion_ID = auth.auth_register("cowardylion@wizardofoz.com", "wantscourage", "cowardylion", "wizardofoz")['u_id']
    cowardylion_token = auth.auth_login("cowardylion@wizardofoz.com", "wantscourage")['token']

    auth.auth_register("dorothy@wizardofoz.com", "wantshome", "dorothy", "wizardofoz")
    dorothy_token = auth.auth_login("dorothy@wizardofoz.com", "wantshome")['token']

    # Create channels 
    yellowbrickroadID = channels.channels_create(scarecrow_token, "YellowBrickRoadChannel", True)['channel_id']
    emeraldcityID = channels.channels_create(tinman_token, "EmeraldCityChannel", True)['channel_id']
    channel.channel_join(cowardylion_token, yellowbrickroadID)
    channel.channel_join(dorothy_token, emeraldcityID)

    # Invalid ID
    with pytest.raises(InputError):
        channel.channel_details(scarecrow_token, 20202021) # Channel ID does not exist being o
    
    with pytest.raises(InputError):
        channel.channel_details(dorothy_token, 82303392) # Channel ID does not exist just joining

    # Invalid authorisation 
    with pytest.raises(AccessError):
        channel.channel_details(tinman_token, yellowbrickroadID) # Not part of the channel being o
    
    with pytest.raises(AccessError):
        channel.channel_details(cowardylion_token, emeraldcityID) # Not part of the channel just joining
    
    # Check return when valid 
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['name'] == 'YellowBrickRoadChannel'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['owner_members'][0]['u_id'] == scarecrow_ID
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['owner_members'][0]['name_first'] == 'scarecrow'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['owner_members'][0]['name_last'] == 'wizardofoz'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][0]['u_id'] == scarecrow_ID
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][0]['name_first'] == 'scarecrow'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][0]['name_last'] == 'wizardofoz'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][1]['u_id'] == croardylion_ID
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][1]['name_first'] == 'cowardylion'
    assert channel.channel_details(scarecrow_token, yellowbrickroadID)['all_members'][1]['name_last'] == 'wizardofoz'


    

def test_channel_messages():
    clear()
    # Create Users
    MrIncredible_id = auth.auth_register("MrIncredible@theincredibles.com", "strength", "MrIncredible", "theincredibles")['u_id']
    MrIncredible_token = auth.auth_login("tom@theincredibles.com", "chasingmice")['token']

    MrsIncredible_id = auth.auth_register("MrsIncredible@theincredibles.com", "shapeshifting", "MrsIncredible", "theincredibles")['u_id']
    MrsIncredible_token = auth.auth_login("MrsIncredible@theincredibles.com", "shapeshifting")['token']

    Violet_id = auth.auth_register("Violet@theincredibles.com", "invisible", "Violet", "theincredibles")['u_id']
    Violet_token = auth.auth_login("Violet@theincredibles.com", "invisible")['token']

    Jack_id = auth.auth_register("Jack@theincredibles.com", "multiplication", "Jack", "theincredibles")['u_id']
    Jack_token = auth.auth_login("Jack@theincredibles.com", "multiplication")['token']

    Dash_id = auth.auth_register("Dash@theincredibles.com", "speed", "Dash", "theincredibles")['u_id']
    Dash_token = auth.auth_login("Dash@theincredibles.com", "speed")['token']

    # Create channels
    metroville_id = channels.channels_create(MrIncredible_token, "PublicChannel", True)['channel_id']
    nomanisn_id = channels.channels_create(MrsIncredible_token, "PrivateChannel", True)['channel_id']
    channel.channel_join(Violet_token, metroville_id)
    channel.channel_join(Jack_token, metroville_id)
    channel.channel_join(Dash_token, nomanisn_id)

    # Channel ID is invalid
    with pytest.raises(InputError):
        channel.channel_messages(MrIncredible_token, 1232123)
    
    with pytest.raises(InputError):
        channel.channel_messages(MrsIncredible_token, 1232129472)

    # Authorised user is not part of the channel
    with pytest.raises(AccessError):
        channel.channel_messages(MrsIncredible_token, metroville_id) # owner and not part of the channel
    
    with pytest.raises(AccessError):
        channel.channel_messages(Violet_token, nomanisn_id) # not owner and not part of the channel
        
    # Check start is greater than 
    

# channel_leave returns a dictionary {is_success: True/False}
def test_channel_leave():
    clear()
    # Create users
    auth.auth_register("diglett@pokemon.com", "arenatrap", "Diglett", "Pokemon")
    diglett_token = auth.auth_login("diglett@pokemon.com", "arenatrap")['token']

    auth.auth_register("ponyta@pokemon.com", "horndrillXD", "Ponyta", "Pokemon")['u_id']
    ponyta_token = auth.auth_login("ponyta@pokemon.com", "horndrillXD")['token']

    auth.auth_register("gyarados@pokemon.com", "notadragontype", "Gyarados", "Pokemon")
    gyarados_token = auth.auth_login("gyarados@pokemon.com", "notadragontype")['token']

    auth.auth_register("dratini@pokemon.com", "notawatertype", "Dratini", "Pokemon")
    dratini_token = auth.auth_login("dratini@pokemon.com", "notawatertype")['token']

    # Users create and join channels
    moleID = channels.channels_create(diglett_token, "MoleChannel", True)['channel_id']
    splashID = channels.channels_create(gyarados_token, "SplashChannel", True)['channel_id']
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
    '''
    ONLY USE THIS CODE IF WE DECIDE TO INCLUDE THE POSSIBLE ASSUMPTIONS IN THE .TXT FILE

    # Owners leaving channels
    with pytest.raises(InputError):
        channel.channel_leave(diglett_token, moleID) # If diglett leaves there are no owners
    channel.channel_addowner(diglett_token, moleID, ponyta_id)
    assert channel.channel_leave(diglett_token, moleID)['is_success'] == True # NOW Diglett can leave since Ponyta is an owner
    '''

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
    pub_ch_id = channels.channels_create(mario_token, "PublicChannel", True)['channel_id']
    prv_ch_id = channels.channels_create(peach_token, "PrivateChannel", False)['channel_id']

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
    gods_channel_id = channels.channels_create(comp_token, "TheGods", True)['channel_id']
    alt_channel_id = channels.channels_create(math_id, "Alternate", True)['channel_id']
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
    # Create users
    blossom_id = auth.auth_register("blossom@powerpuff.com", "colourpink", "blossom", "powerpuff")['u_id']
    blossom_token = auth.auth_login("blossom@powerpuff.com", "colourpink")['token']

    bubbles_id = auth.auth_register("bubbles@powerpuff.com", "colourblue", "bubbles", "powerpuff")['u_id']
    bubbles_token = auth.auth_login("bubbles@powerpuff.com", "colourblue")['token']

    buttercup_id = auth.auth_register("buttercup@powerpuff.com", "colourgreen", "buttercup", "powerpuff")['u_id']
    buttercup_token = auth.auth_login("buttercup@powerpuff.com", "colourgreen")['token']

    # Create channel 
    girls_channel_id = channels.channels_create(blossom_token, "girls_channel", True)['channel_id']
    power_channel_id = channels.channels_create(bubbles_token, "power_channel", True)['channel_id']
    channel.channel_join(buttercup_token, girls_channel_id)

    # Channel ID is not valid and invalid channel and invalid token
    with pytest.raises(InputError):
        channel.channel_removeowner(blossom_token, girls_channel_id, 1232123)
    
    with pytest.raises(InputError):
        channel.channel_removeowner(blossom_token, 13579, blossom_id)

    # User id u_id is not an owner of the channel
    with pytest.raises(InputError):
        channel.channel_removeowner(buttercup_token, girls_channel_id, buttercup_id)

    # Removing someone not in the channel
    with pytest.raises(InputError):
        channel.channel_removeowner(bubbles_token, girls_channel_id, blossom_id)

    # Removing someone without access permission
    with pytest.raises(AccessError):
        channel.channel_removeowner(buttercup_token, girls_channel_id, blossom_id)

    # Checking that the removal works
    channel.channel_addowner(blossom_token, girls_channel_id, buttercup_id)
    assert channel.channel_removeowner(buttercup_token, girls_channel_id, blossom_id)['is_success'] == True
    assert channel.channel_removeowner(buttercup_token, girls_channel_id, buttercup_id)['is_success'] == True
    assert channel.channel_removeowner(bubbles_token, power_channel_id, bubbles_id)['is_success'] == True

def test_invalid_tokens():
    clear()
    # Create users
    tom_id = auth.auth_register("tom@tomandjerry.com", "chasingmice", "Tom", "Cat")['u_id']
    tom_token = auth.auth_login("tom@tomandjerry.com", "chasingmice")['token']

    jerry_id = auth.auth_register("jerry@tomandjerry.com", "eatingcheese", "Jerry", "Mouse")['u_id']
    auth.auth_login("jerry@tomandjerry.com", "eatingcheese")['token']

    spike_id = auth.auth_register("spike@tomandjerry.com", "chewingbone", "Spike", "Dog")['u_id']
    auth.auth_login("spike@tomandjerry.com", "chewingbone")['token']

    # Create a public channel
    channel_id = channels.channels_create(tom_token, "TomAndJerry", True)['channel_id']
    channel.channel_invite(tom_token, channel_id, jerry_id)

    # Token AccessErrors
    with pytest.raises(AccessError):
        channel.channel_invite(2736273, channel_id, spike_id)
    with pytest.raises(AccessError):
        channel.channel_join(56453, channel_id)
    with pytest.raises(AccessError):
        channel.channel_details(23532, channel_id)
    with pytest.raises(AccessError):
        channel.channel_leave(563464, channel_id)
    with pytest.raises(AccessError):
        channel.channel_addowner(23141, channel_id, jerry_id)
    with pytest.raises(AccessError):
        channel.channel_removeowner(23141, channel_id, tom_id)
    '''
    with pytest.raises(AccessError):
        channel.channel_messages(232414, channel_id, start)
    '''


# IGNORE THIS
if __name__ == "__main__":
    u_id = auth.auth_register("person1@unsw.com", "pass1234", "Person", "One")['u_id']
    print(u_id)
    u2_id = auth.auth_register("person2@unsw.com", "pass1234", "Person", "One")['u_id']
    print(u2_id)
