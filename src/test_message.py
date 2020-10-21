# test message.py

from message import message_send, message_remove, message_edit

import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from other import clear

### message ###

# fixtures #
@pytest.fixture
def data():
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

    return {
        'u1_id': u1_id,
        'u2_id': u2_id,
        'u3_id': u3_id,
        'token1': token1,
        'token2': token2,
        'token3': token3,
        'c1_id': c1_id,
        'c2_id': c2_id
    }

    
    # (u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id)

# test message_send #
"""
message_send(token, channel_id, message)
OUTPUT: { message_id }
"""

#### MESSAGE 0 IS THE MOST RECENT MESSAGE IN THE CHANNEL ####

# VALID CASES #
def test_message_user_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Send the message 
    message1 = message_send(data['token1'], data['c1_id'], "This is the first message in the channel")
    # Find the message in the channel through channel messages - returns dictionary specifically a list of messages
    message_in_channel = channel.channel_message(data['token1'], data['c1_id'], 0)['messages']
    # Find the message ID
    message_id_at_index_zero = message_in_channel[0]['message_id']
    # Compare the message sent ID and the channels message ID 
    assert message1 == message_id_at_index_zero

def test_message_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    message1 = message_send(data['token2'], data['c2_id'], "This is the first message in the channel")
    message_in_channel = channel.channel_message(data['token2'], data['c2_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

def test_message_non_alpha_characters(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Flocker owner sending message 
    message1 = message_send(data['token1'], data['c1_id'], "This message has many non alpha character: !@#$%^&*()")
    message_in_channel = channel.channel_message(data['token1'], data['c1_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

# INVALID CASES #
def test_message_greater_than_1000(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Character length of message - random words but proper length 

    # Check that 1000 works 
    message1 = message_send(data['token1'], data['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N")
    message_in_channel = channel.channel_message(data['token1'], data['c1_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero
    # Invalid if 10001
    with pytest.raises(InputError):
        message_send(data['token1'], data['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na")

def test_user_not_in_channel(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Person 3 is not in any channel 
    # Try them in channel 2 
    with pytest.raises(AccessError):
        message_send(data['token3'], data['c2_id'], "This user is not in the channel")

def test_user_logged_out(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Log out person 2 
    if auth.auth_logout(data['token2'])['is_success'] == True:
        with pytest.raises(AccessError):
            message_send(data['token2'], data['c2_id'], "This user is logged out")

def test_empty_message(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    with pytest.raises(InputError):
        message_send(data['token2'], data['c2_id'], "")

# test message_remove #
"""
message_remove(token, message_id)
OUTPUT: {}
"""

# VALID CASES #
def test_remove_user_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Send message from flocker owner - returns message ID
    message_id = message_send(data['token1'], data['c1_id'], "This message will be removed")
    # This message should be removed 
    assert message_remove(data['token1'], message_id)
    
def test_remove_flocker_owner_but_not_owner(data):
    channels.channel_join(data['token1'], data['c2_id'])

    message_id = message_send(data['token1'], data['c2_id'], "This message will be removed")
    # This message should be removed 
    assert message_remove(data['token1'], message_id)

def test_remove_request_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Authorised user sending message 
    message_id = message_send(data['token2'], data['c2_id'], "This message will be removed")
    # This message should be removed as authorised user making this request
    assert message_remove(data['token2'], message_id)

# INVALID CASES #
def test_message_no_longer_exists(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Create valid message
    message_id = message_send(data['token1'], data['c1_id'], "This is a valid message")
    # Remove message
    message_remove(data['token1'], message_id)
    # Try remove it again
    with pytest.raises(InputError):
        message_remove(data['token1'], message_id)

def test_not_users_message(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channels.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channels.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # Create a message sent by user 1 
    message_id = message_send(data['token1'], data['c1_id'], "This message was sent by one of the owners of the channel")
    # User 2 try and remove it 
    with pytest.raises(AccessError):
        message_remove(data['token2'], message_id)

def test_user_not_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1 just as member
    channels.channel_join(data['token2'], data['c1_id'])
    # Get them to send a message
    message_id = message_send(data['token2'], data['c1_id'], "This message was sent by one of the members of the channel")
    # Try to remove it
    with pytest.raises(AccessError):
        message_remove(data['token2'], message_id)


# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Send a message 
    message_id = message_send(data['token1'], data['c1_id'], "This message was sent by the owner of flocker")
    # Edit the message 
    assert message_edit(data['token1'], message_id, "This is the new message we just changed it completely but same same hey")

def test_edit_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channels.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channels.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # user two - owner - send message
    message_id = message_send(data['token2'], data['c1_id'], "This message was sent by an owner of this channel")

    assert message_edit(data['token2'], message_id, "This message should be able to be edited")


# INVALID CASES #
def test_not_valid_user(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Join as a member now owner
    channels.channel_join(data['token2'], data['c1_id'])
    # Send message
    message_id = message_send(data['token2'], data['c1_id'], "This message was sent by not an owner")
    # edited by 
    with pytest.raises(AccessError):
        message_edit(data['token2'], message_id, "This message should not be able to be edited")

def test_edit_not_by_person_who_sent(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channels.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channels.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # user two - owner - send message
    message_id = message_send(data['token2'], data['c1_id'], "This message was sent by an owner of this channel")   
    # user one try and edit 
    with pytest.raises(AccessError):
        message_edit(data['token1'], message_id, "This message should not be able to be edited")

# Check that if empty string the message gets deleted 
def test_empty_string (data):
    # Send first message 
    message1_id = message_send(data['token1'], data['c1_id'], "This is the first message sent")  
    # Send second message 
    message2_id = message_send(data['token1'], data['c1_id'], "This is the second message sent") 

    # Edit first message with empty string so should only be one message left 
    message_edit(data['token1'], message1_id, "")
    # Get the messages from channel
    message = channel.channel_message(data['token1'], data['c1_id'], 0)['messages'])
    # get the message id 
    message_id_at_index_zero = message[0]['message_id']
    # Compare the message sent ID and the channels message ID 
    assert message2_id == message_id_at_index_zero

