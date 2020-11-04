# test message.py

import message as msg

import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from other import clear

from datetime import datetime, timedelta

SUCCESS = {}

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

    time_current = datetime.now()

    return {
        'u1_id': u1_id,
        'u2_id': u2_id,
        'u3_id': u3_id,
        'token1': token1,
        'token2': token2,
        'token3': token3,
        'c1_id': c1_id,
        'c2_id': c2_id,
        'time_current': time_current,
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
    message1 = msg.message_send(data['token1'], data['c1_id'], "This is the first message in the channel")['message_id']
    # Find the message in the channel through channel messages - returns dictionary specifically a list of messages
    message_in_channel = channel.channel_messages(data['token1'], data['c1_id'], 0)['messages']
    # Find the message ID
    message_id_at_index_zero = message_in_channel[0]['message_id']
    # Compare the message sent ID and the channels message ID 
    assert message1 == message_id_at_index_zero

def test_message_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    message1 = msg.message_send(data['token2'], data['c2_id'], "This is the first message in the channel")['message_id']
    message_in_channel = channel.channel_messages(data['token2'], data['c2_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

def test_message_non_alpha_characters(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Flocker owner sending message 
    message1 = msg.message_send(data['token1'], data['c1_id'], "This message has many non alpha character: !@#$%^&*()")['message_id']
    message_in_channel = channel.channel_messages(data['token1'], data['c1_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero

# INVALID CASES #
def test_message_greater_than_1000(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Character length of message - random words but proper length 

    # Check that 1000 works 
    message1 = msg.message_send(data['token1'], data['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N")['message_id']
    message_in_channel = channel.channel_messages(data['token1'], data['c1_id'], 0)['messages']
    message_id_at_index_zero = message_in_channel[0]['message_id']
    assert message1 == message_id_at_index_zero
    # Invalid if 10001
    with pytest.raises(InputError):
        msg.message_send(data['token1'], data['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na")['message_id']

def test_user_not_in_channel(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Person 3 is not in any channel 
    # Try them in channel 2 
    with pytest.raises(AccessError):
        msg.message_send(data['token3'], data['c2_id'], "This user is not in the channel")['message_id']

def test_user_logged_out(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Log out person 2 
    if auth.auth_logout(data['token2'])['is_success'] == True:
        with pytest.raises(AccessError):
            msg.message_send(data['token2'], data['c2_id'], "This user is logged out")['message_id']

def test_empty_message(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    with pytest.raises(InputError):
        msg.message_send(data['token2'], data['c2_id'], "")['message_id']

# test message_remove #
"""
message_remove(token, message_id)
OUTPUT: {}
"""

# VALID CASES #
def test_remove_user_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Send message from flocker owner - returns message ID
    message_id = msg.message_send(data['token1'], data['c1_id'], "This message will be removed")['message_id']
    # This message should be removed 
    assert msg.message_remove(data['token1'], message_id)
    
def test_remove_flocker_owner_but_not_owner(data):
    channel.channel_join(data['token1'], data['c2_id'])

    message_id = msg.message_send(data['token1'], data['c2_id'], "This message will be removed")['message_id']
    # This message should be removed 
    assert msg.message_remove(data['token1'], message_id)

def test_remove_request_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Authorised user sending message 
    message_id = msg.message_send(data['token2'], data['c2_id'], "This message will be removed")['message_id']
    # This message should be removed as authorised user making this request
    assert msg.message_remove(data['token2'], message_id)

# INVALID CASES #
def test_message_no_longer_exists(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Create valid message
    message_id = msg.message_send(data['token1'], data['c1_id'], "This is a valid message")['message_id']
    # Remove message
    msg.message_remove(data['token1'], message_id)
    # Try remove it again
    with pytest.raises(InputError):
        msg.message_remove(data['token1'], message_id)

def test_not_users_message(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channel.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channel.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # Create a message sent by user 1 
    message_id = msg.message_send(data['token1'], data['c1_id'], "This message was sent by one of the owners of the channel")['message_id']
    # User 2 try and remove it 
    with pytest.raises(AccessError):
        msg.message_remove(data['token2'], message_id)

def test_user_not_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1 just as member
    channel.channel_join(data['token2'], data['c1_id'])
    # Get them to send a message
    message_id = msg.message_send(data['token2'], data['c1_id'], "This message was sent by one of the members of the channel")['message_id']
    # Try to remove it
    with pytest.raises(AccessError):
        msg.message_remove(data['token2'], message_id)


# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Send a message 
    message_id = msg.message_send(data['token1'], data['c1_id'], "This message was sent by the owner of flocker")['message_id']
    # Edit the message 
    assert msg.message_edit(data['token1'], message_id, "This is the new message we just changed it completely but same same hey")

def test_edit_user_member(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channel.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channel.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # user two - owner - send message
    message_id = msg.message_send(data['token2'], data['c1_id'], "This message was sent by an owner of this channel")['message_id']

    assert msg.message_edit(data['token2'], message_id, "This message should be able to be edited")


# INVALID CASES #
def test_not_valid_user(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Join as a member now owner
    channel.channel_join(data['token2'], data['c1_id'])
    # Send message
    message_id = msg.message_send(data['token2'], data['c1_id'], "This message was sent by not an owner")['message_id']
    # edited by 
    with pytest.raises(AccessError):
        msg.message_edit(data['token2'], message_id, "This message should not be able to be edited")

def test_edit_not_by_person_who_sent(data):
    # u1_id, u2_id, u3_id, token1, token2, token3, c1_id, c2_id = flockr_state
    # Add another person 2 to channel 1
    channel.channel_join(data['token2'], data['c1_id'])
    # Make them owner so they can remove message 
    channel.channel_addowner(data['token1'], data['c1_id'], data['u2_id'])
    # user two - owner - send message
    message_id = msg.message_send(data['token2'], data['c1_id'], "This message was sent by an owner of this channel")['message_id']   
    # user one try and edit 
    with pytest.raises(AccessError):
        msg.message_edit(data['token1'], message_id, "This message should not be able to be edited")

# Check that if empty string the message gets deleted 
def test_empty_string (data):
    # Send first message 
    message1_id = msg.message_send(data['token1'], data['c1_id'], "This is the first message sent")['message_id']  
    # Send second message 
    message2_id = msg.message_send(data['token1'], data['c1_id'], "This is the second message sent")['message_id'] 

    # Edit first message with empty string so should only be one message left 
    msg.message_edit(data['token1'], message2_id, "")
    # Get the messages from channel
    message = channel.channel_messages(data['token1'], data['c1_id'], 0)['messages']
    # get the message id 
    message_id_at_index_zero = message[0]['message_id']
    # Compare the message sent ID and the channels message ID 
    assert message1_id == message_id_at_index_zero



## ITERATION 3 TESTS ##

# TODO: message_sendlater
# message_pin
'''
sendlater(token, channel_id, message, time_sent)
OUTPUT : {message_id}
'''
## VALID CASES ##
# Sendlater at a valid time in the future (to a channel token is a part of)
def test_sendlater_success(data):
    # Sendlater message 4 days later, token1 is a part of channel_id1
    time_delta = timedelta(days = 4)
    future_time = data['time_current'] + time_delta

    assert msg.message_sendlater(data['token1'], data['c1_id'], "This message is a sendlater message", future_time)

    # Sendlater message 4 minutes later, token1 is a part of channel_id1
    time_delta = timedelta(minutes = 4)
    future_time = data['time_current'] + time_delta

    assert msg.message_sendlater(data['token1'], data['c1_id'], "This message is a sendlater message", future_time)


## INVALID CASES ##
# Sendlater to invalid channel (InputError)
def test_sendlater_invalid_channel(data):
    # Valid time delta
    time_delta = timedelta(minutes = 4)
    future_time = data['time_current'] + time_delta

    # Channel_id invalid
    with pytest.raises(InputError):
        msg.message_sendlater(data['token1'], 4645, "Sent to invalid channel_id", future_time)

# Sendlater message more than 1000 chars (InputError)
def test_sendlater_invalid_message_len(data):
    # Valid time delta
    time_delta = timedelta(minutes = 4)
    future_time = data['time_current'] + time_delta

    # A string of 1001 chars 
    long_string = "x" * 1001

    # Message is more than 1000 characters
    with pytest.raises(InputError):
        msg.message_sendlater(data['token1'], data['c1_id'], long_string, future_time)
   

# Sendlater invalid time_sent - in the past (InputError)
def test_sendlater_invalid_time(data):
    # Valid time delta
    time_delta = timedelta(minutes = 4)
    # Time in the past
    future_time = data['time_current'] - time_delta

    # Channel_id invalid
    with pytest.raises(InputError):
        msg.message_sendlater(data['token1'], 4645, "Sendlater time in pass is not possible", future_time)

# Sendlater to a channel which you are not in (AccessError)
def test_sendlater_in_another_channel(data):
    # Valid time delta
    time_delta = timedelta(minutes = 4)
    future_time = data['time_current'] + time_delta

    # Token1 is not a part of c2_id
    with pytest.raises(AccessError):
        msg.message_sendlater(data['token1'], data['c2_id'], "Sent to invalid channel_id", future_time)

    # Token2 invites token1 to c2_id
    channel.channel_invite(data['token2'], data['c2_id'], data['u1_id'])

    assert msg.message_sendlater(data['token1'], data['c2_id'], "Now part of channel", future_time)
    

# TODO: message_react

# TODO: message_unreact


# message_pin
'''
message_pin(token, message_id) = {}
'''

## VALID CASES ##

# Pin one message
def test_single_msg_pin(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned")['message_id']
    msg.message_send(data['token1'], data['c1_id'], "This message will not be pinned") 
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS

# Pin two messages
def test_double_msg_pin(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned")['message_id']
    msg2_id = msg.message_send(data['token1'], data['c1_id'], "This message will also be pinned")['message_id']
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS
    assert msg.message_pin(data['token1'], msg2_id) == SUCCESS

# A channel owner can pin a message sent by a regular member
def test_pin_by_owner(data):
    channel.channel_join(data['token3'], data['c2_id'])
    msg1_id = msg.message_send(data['token3'], data['c2_id'], "This message was sent by a regular member and it will be pinned")['message_id']
    assert msg.message_pin(data['token2'], msg1_id) == SUCCESS

# The Flockr owner does not have to be a channel owner to pin a message
def test_pin_flockr_owner(data):
    channel.channel_join(data['token1'], data['c2_id'])
    msg1_id = msg.message_send(data['token2'], data['c2_id'], "This message was sent by an owner and it will be pinned")['message_id']
    # FO can pin another owner's message but they must be in the channel
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS


## INVALID CASES ##

# Pinning a message which is already pinned
def test_pin_existing(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned")['message_id']
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS
    with pytest.raises(InputError):
        msg.message_pin(data['token1'], msg1_id) # Already pinned

# Pinning a message in a channel which you are not in
def test_pin_in_another_channel(data):
    msg1_id = msg.message_send(data['token2'], data['c2_id'], "This message will be pinned by a channel owner")['message_id']
    msg2_id = msg.message_send(data['token2'], data['c2_id'], "This message cannot be pinned")['message_id']
    assert msg.message_pin(data['token2'], msg1_id) == SUCCESS # P2 is permitted to pin

    channel.channel_join(data['token3'], data['c1_id'])
    channel.channel_addowner(data['token1'], data['c1_id'], data['u3_id'])
    with pytest.raises(AccessError):
        msg.message_pin(data['token3'], msg2_id) # P3 (An owner of C1 is not in C2)

    with pytest.raises(AccessError):
        msg.message_pin(data['token1'], msg2_id) # P1 (Flockr Owner) is not in C2 either

# A normal member cannot pin a message even if it is their own
def test_pin_but_not_owner(data):
    channel.channel_join(data['token2'], data['c1_id'])
    msg1_id = msg.message_send(data['token2'], data['c1_id'], "I am a normal owner. I cannot pin this :(")['message_id']
    # P2 is a regular member in C1 who has just sent a message
    with pytest.raises(AccessError):
        # Since they are not an owner, they cannot pin this message
        msg.message_pin(data['token2'], msg1_id)



# message_unpin
'''
message_unpin(token, message_id) = {}
'''

## VALID CASES ##

# Unpin a pinned message
def test_single_msg_unpin(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned")['message_id']
    msg.message_send(data['token1'], data['c1_id'], "This message will not be pinned") 
    msg.message_pin(data['token1'], msg1_id)
    assert msg.message_unpin(data['token1'], msg1_id) == SUCCESS

# Unpin multiple pinned messages
def test_double_msg_unpin(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned")['message_id']
    msg2_id = msg.message_send(data['token1'], data['c1_id'], "This message will also be pinned")['message_id']
    msg.message_pin(data['token1'], msg1_id)
    msg.message_pin(data['token1'], msg2_id)
    assert msg.message_unpin(data['token1'], msg1_id) == SUCCESS
    assert msg.message_unpin(data['token1'], msg2_id) == SUCCESS

# A channel owner can unpin a message send by someone else
def test_unpin_by_another_owner(data):
    channel.channel_join(data['token3'], data['c2_id'])
    msg1_id = msg.message_send(data['token3'], data['c2_id'], "This message was sent by a regular member and it will be pinned")['message_id']
    msg.message_pin(data['token2'], msg1_id)

    # Add P3 as an owner and get them to unpin
    channel.channel_addowner(data['token2'], data['c2_id'], data['u3_id'])
    assert msg.message_unpin(data['token3'], msg1_id) == SUCCESS

# The Flockr owner does not have to be a channel owner to pin a message
def test_unpin_flockr_owner(data):
    channel.channel_join(data['token1'], data['c2_id'])
    msg1_id = msg.message_send(data['token2'], data['c2_id'], "This message was sent by an owner and it will be pinned")['message_id']
    
    # P2 is channel owner and P1 is not (but they are the flockr owner so they are still permitted to unpin)
    msg.message_pin(data['token2'], msg1_id)
    assert msg.message_unpin(data['token1'], msg1_id) == SUCCESS

# You can repin a message when it has been unpinned
def test_pin_unpin(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be pinned over and over")['message_id']
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS
    assert msg.message_unpin(data['token1'], msg1_id) == SUCCESS
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS
    assert msg.message_unpin(data['token1'], msg1_id) == SUCCESS


## INVALID CASES ##

# Unpinning a message which is not pinned
def test_unpin_normal_msg(data):
    msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message cannot be unpinned")['message_id']
    with pytest.raises(InputError):
        msg.message_unpin(data['token1'], msg1_id) # Is not already pinned

# Unpinning a message in a channel which you are not in
def test_unpin_in_another_channel(data):
    msg1_id = msg.message_send(data['token2'], data['c2_id'], "This message can only be unpinned by a channel owner")['message_id']
    assert msg.message_pin(data['token2'], msg1_id) == SUCCESS # P2 is permitted to pin

    channel.channel_join(data['token3'], data['c1_id'])
    channel.channel_addowner(data['token1'], data['c1_id'], data['u3_id'])

    # P1 and P3 and in one channel and P2 is in the other
    with pytest.raises(AccessError):
        msg.message_unpin(data['token3'], msg1_id) # P3 (An owner of C1 is not in C2)
    with pytest.raises(AccessError):
        msg.message_unpin(data['token1'], msg1_id) # P1 (Flockr Owner) is not in C2 either

# A normal member cannot unpin a message even if it is their own
def test_unpin_but_not_owner(data):
    channel.channel_join(data['token2'], data['c1_id'])
    msg1_id = msg.message_send(data['token2'], data['c1_id'], "I am a normal owner. I cannot unpin this :(")['message_id']
    assert msg.message_pin(data['token1'], msg1_id) == SUCCESS

    # P2 is a regular member in C1 who has just sent a message which has been pinned by an owner
    with pytest.raises(AccessError):
        # Since they are not an owner, they cannot unpin this message
        msg.message_unpin(data['token2'], msg1_id)

