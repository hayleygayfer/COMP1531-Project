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
def flockr_state():
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

    return (u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id)

# test message_send #
"""
message_send(token, channel_id, message)
OUTPUT: { message_id }
"""

#### MESSAGE 0 IS THE MOST RECENT MESSAGE IN THE CHANNEL ####

# VALID CASES #
def test_message_user_owner(flockr_state):
    # Send the message 
    message1 = message_send(token1, c1_id, "This is the first message in the channel")
    # Find the message in the channel through channel messages - returns dictionary specifically a list of messages
    message_in_channel = channel.channel_message(token1, c1_id, 0)['messages']
    # Find the message ID
    message_id_at_index_zero = message_in_channel[0]['message_id']
    # Compare the message sent ID and the channels message ID 
    assert message1 == message_id_at_index_zero

def test_message_user_member(flockr_state):
    message1 = message_send(token2, c2_id, "This is the first message in the channel")
    message_in_channel = channel.channel_message(token2, c2_id, 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

def test_message_non_alpha_characters(flockr_state):
    # Flocker owner sending message 
    message1 = message_send(token1, c1_id, "This message has many non alpha character: !@#$%^&*()")
    message_in_channel = channel.channel_message(token1, c1_id, 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

# INVALID CASES #
def test_message_greater_than_1000(flockr_state):
    # Check that 1000 works 
    message1 = message_send(token1, c1_id, "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N")
    message_in_channel = channel.channel_message(token1, c1_id, 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero
    # Invalid if 10001
    with pytest.raises(InputError):
        message_send(token1, c1_id, "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na")

def test_user_not_in_channel(flockr_state):
    pass

def test_user_logged_out(flockr_state):
    pass

def test_empty_message(flockr_state):
    pass

# test message_remove #
"""
message_remove(token, message_id)
OUTPUT: {}
"""

# VALID CASES #
def test_remove_user_owner(flockr_state):
    pass

def test_remove_request_user_member(flockr_state):
    pass

# INVALID CASES #
def test_message_no_longer_exists(flockr_state):
    pass

def test_not_users_message(flockr_state):
    pass

def test_user_not_owner(flockr_state):
    pass

# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(flockr_state):
    pass

def test_edit_user_member(flockr_state):
    pass

# INVALID CASES #
def test_not_valid_user(flockr_state):
    pass

def test_edit_not_in_channel(flockr_state):
    pass


