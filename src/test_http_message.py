import requests
import json 
from echo_http_test import url
import pytest

SUCCESS = 200
ERROR = 400

@pytest.fixture
def user_list(url):
    requests.delete(url + 'clear')
    
    LogResponse1 = auth(url, "person1@email.com", "password", "Person", "One")
    LogResponse2 = auth(url, "person2@email.com", "password", "Person", "Two")
    LogResponse3 = auth(url, "person3@email.com", "password", "Person", "Three")

    return {
        'token1': LogResponse1['token'],
        'token2': LogResponse2['token'],
        'token3': LogResponse3['token'],
        'u1_id': LogResponse1['u_id'],
        'u2_id': LogResponse2['u_id'],
        'u3_id': LogResponse3['u_id']
    }

@pytest.fixture
def channel_list(url, user_list):
    # person one and person two create channels
    c1 = channels_create(url, user_list['token1'], "channel_1", True)
    c2 = channels_create(url, user_list['token2'], "channel_2", True)

    return {
        'c1_id': c1['channel_id'],
        'c2_id': c2['channel_id'],
    }

#################################################################
## HELPER FUNCTIONS

def auth(url_auth, email, password, n1, n2):
    payload = {"email": email, "password": password, "name_first": n1, "name_last": n2}
    requests.post(url_auth + "auth/register", json=payload)
    payload = {"email": email, "password": password}
    response = requests.post(url_auth + "auth/login", json=payload)
    return response.json()

def channels_create(url_create, token, name, is_pub):
    payload = {"token": token, "name": name, "is_public": is_pub}
    response = requests.post(url_create + "channels/create", json=payload)
    return response.json()

def message_send(url_send, token, channel_id, msg):
    payload = {"token": token, "channel_id": channel_id, "message": msg}
    response = requests.post(url_send + "message/send", json=payload)
    return {
        'status': response.status_code,
        'message_id': response.json().get('message_id')
    }

def message_remove(url_rem, token, message_id):
    payload = {"token": token, "message_id": message_id}
    response = requests.delete(url_rem + "message/remove", json=payload)
    return response.status_code

def message_edit(url_edit, token, message_id, message):
    payload = {"token": token, "message_id": message_id, "message": message}
    response = requests.put(url_edit + "message/edit", json=payload)
    return response.status_code

def channel_messages(url_msg, token, channel_id, start):
    payload = {'token': token, 'channel_id': channel_id, 'start': start}
    response = requests.get(url_msg + "channel/messages", params=payload)
    return {
        'status': response.status_code,
        'messages': response.json().get('messages'),
        'start': response.json().get('start'),
        'end': response.json().get('end')
    }

def channel_join(url_join, token, channel_id):
    payload = {"token": token, "channel_id": channel_id}
    response = requests.post(url_join + "channel/join", json=payload)
    return response.status_code

def channel_addowner(url_add, token, channel_id, u_id):
    payload = {"token": token, "channel_id": channel_id, "u_id": u_id}
    response = requests.post(url_add + "channel/addowner", json=payload)
    return response.status_code

def message_react(url_react, token, message_id, react_id):
    payload = {'token': token, 'message_id': message_id, 'react_id': react_id}
    response = requests.post(url_react + "message/react", json=payload)
    return response.status_code

def message_unreact(url_unreact, token, message_id, react_id):
    payload = {'token': token, 'message_id': message_id, 'react_id': react_id}
    response = requests.post(url_unreact + "message/unreact", json=payload)
    return response.status_code

def message_pin(url_pin, token, message_id):
    payload = {'token': token, 'message_id': message_id}
    response = requests.post(url_pin + "message/pin", json=payload)
    return response.status_code

def message_unpin(url_unpin, token, message_id):
    payload = {'token': token, 'message_id': message_id}
    response = requests.post(url_unpin + "message/unpin", json=payload)
    return response.status_code

# MESSAGE 0 IS THE MOST RECENT MESSAGE IN THE CHANNEL #
##################################################################

# test message_send #
"""
message_send(token, channel_id, message)
OUTPUT: { message_id }
"""

# VALID CASES #

def test_message_user_owner_http(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token1'], channel_list['c1_id'], "This is the first message in the channel")
    message_ID = response['message_id']
    assert response['status'] == SUCCESS

    # Get message from channel messages
    messages = channel_messages(url, user_list['token1'], channel_list['c1_id'], 0)['messages']
    message_id_at_index_zero = messages[0]['message_id']
    assert message_ID == message_id_at_index_zero

def test_message_user_member(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token2'], channel_list['c2_id'], "This is the first message in the channel")
    message_ID = response['message_id']
    assert response['status'] == SUCCESS

    # Get message from channel messages
    messages = channel_messages(url, user_list['token2'], channel_list['c2_id'], 0)['messages']
    message_id_at_index_zero = messages[0]['message_id']
    assert message_ID == message_id_at_index_zero

def test_message_non_alpha_characters(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token1'], channel_list['c1_id'], "This message has many non alpha character: !@#$%^&*()")
    message_ID = response['message_id']
    assert response['status'] == SUCCESS

    # Get message from channel messages
    messages = channel_messages(url, user_list['token1'], channel_list['c1_id'], 0)['messages']
    message_id_at_index_zero = messages[0]['message_id']
    assert message_ID == message_id_at_index_zero

# INVALID CASES #
def test_message_greater_than_1000(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token1'], channel_list['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. N")
    message_ID = response['message_id']
    assert response['status'] == SUCCESS

    # Get message from channel messages
    messages = channel_messages(url, user_list['token1'], channel_list['c1_id'], 0)['messages']
    message_id_at_index_zero = messages[0]['message_id']
    assert message_ID == message_id_at_index_zero

    # Send message with invalid amount
    response = message_send(url, user_list['token1'], channel_list['c1_id'], "Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, sit amet adipiscing sem neque sed ipsum. Na")
    assert response['status'] == ERROR

def test_user_not_in_channel(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token3'], channel_list['c2_id'], "This user is not in the channel")
    assert response['status'] == ERROR

def test_user_logged_out(url, user_list, channel_list):
    # Auth logout 
    payload = {'token': user_list['token2']}
    response = requests.post(url + "auth/logout", json=payload)
    assert response.status_code == SUCCESS

    # Send message
    response = message_send(url, user_list['token2'], channel_list['c2_id'], "This user is logged out")
    assert response['status'] == ERROR

def test_empty_message(url, user_list, channel_list):
    # Send message
    response = message_send(url, user_list['token2'], channel_list['c2_id'], "")
    assert response['status'] == ERROR

# test message_remove #
"""
message_remove(token, message_id)
OUTPUT: {}
"""

# VALID CASES #
def test_remove_user_owner(url, user_list, channel_list):
    # Send message
    message_ID = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be removed")['message_id']

    # Remove message
    assert message_remove(url, user_list['token1'], message_ID) == SUCCESS

def test_remove_flocker_owner_but_not_owner(url, user_list, channel_list):
    # Join channel  
    assert channel_join(url, user_list['token1'], channel_list['c2_id']) == SUCCESS

    # Send message
    message_ID = message_send(url, user_list['token1'], channel_list['c2_id'], "This message will be removed")['message_id']

    # Remove message
    assert message_remove(url, user_list['token1'], message_ID) == SUCCESS


def test_remove_request_user_member(url, user_list, channel_list):
    # Send message
    message_ID = message_send(url, user_list['token2'], channel_list['c2_id'], "This message will be removed")['message_id']

    # Remove message
    assert message_remove(url, user_list['token2'], message_ID) == SUCCESS

# INVALID CASES #
def test_message_no_longer_exists(url, user_list, channel_list):
    # Send message
    message_ID = message_send(url, user_list['token1'], channel_list['c1_id'], "This is a valid message")['message_id']

    # Remove message
    assert message_remove(url, user_list['token1'], message_ID) == SUCCESS

    # Remove message again
    assert message_remove(url, user_list['token2'], message_ID) == ERROR

def test_not_users_message(url, user_list, channel_list):
    # Join channel
    assert channel_join(url, user_list['token2'], channel_list['c1_id']) == SUCCESS

    # Add owner
    assert channel_addowner(url, user_list['token1'], channel_list['c1_id'], user_list['u2_id']) == SUCCESS

    # Send message
    message_ID = message_send(url, user_list['token1'], channel_list['c1_id'], "This message was sent by one of the owners of the channel")['message_id']

    # Remove message 
    assert message_remove(url, user_list['token2'], message_ID) == ERROR

def test_user_not_owner(url, user_list, channel_list):
    # Join channel
    assert channel_join(url, user_list['token2'], channel_list['c1_id']) == SUCCESS

    # Send message
    message_ID = message_send(url, user_list['token2'], channel_list['c1_id'], "This message was sent by one of the members of the channel")['message_id']

    # Remove message 
    assert message_remove(url, user_list['token2'], message_ID) == ERROR

# test message_edit #
"""
message_edit(token, message_id, message)
OUTPUT: {}
"""

# VALID CASES #
def test_edit_user_owner(url, user_list, channel_list):
    # Send message
    message_ID = message_send(url, user_list['token1'], channel_list['c1_id'], "This message was sent by the owner of flocker")['message_id']

    # Edit message 
    assert message_edit(url, user_list['token1'], message_ID, "This is the new message we just changed it completely but same same hey") == SUCCESS


def test_edit_user_member(url, user_list, channel_list):
    # Join channel
    assert channel_join(url, user_list['token2'], channel_list['c1_id']) == SUCCESS

    # Add owner
    assert channel_addowner(url, user_list['token1'], channel_list['c1_id'], user_list['u2_id']) == SUCCESS
    
    # Send message
    message_ID = message_send(url, user_list['token2'], channel_list['c1_id'], "This message was sent by an owner of this channel")['message_id']

    # Edit message
    assert message_edit(url, user_list['token2'], message_ID, "This message should be able to be edited") == SUCCESS


# INVALID CASES #
def test_not_valid_user(url, user_list, channel_list):
    # Join channel
    assert channel_join(url, user_list['token2'], channel_list['c1_id']) == SUCCESS

    # Send message
    message_ID = message_send(url, user_list['token2'], channel_list['c1_id'], "This message was sent by not an owner")['message_id']

    # Edit message
    assert message_edit(url, user_list['token2'], message_ID, "This message should not be able to be edited") == ERROR


def test_edit_not_by_person_who_sent(url, user_list, channel_list):
    # Join channel
    assert channel_join(url, user_list['token2'], channel_list['c1_id']) == SUCCESS

    # Add owner
    assert channel_addowner(url, user_list['token1'], channel_list['c1_id'], user_list['u2_id']) == SUCCESS

    # Send message
    message_ID = message_send(url, user_list['token2'], channel_list['c1_id'], "This message was sent by an owner of this channel")['message_id']

    # Edit message
    assert message_edit(url, user_list['token1'], message_ID, "This message should not be able to be edited") == ERROR


def test_empty_string (url, user_list, channel_list):
    # Send message
    message_ID1 = message_send(url, user_list['token1'], channel_list['c1_id'], "This is the first message sent")['message_id']
    message_ID2 = message_send(url, user_list['token1'], channel_list['c1_id'], "This is the second message sent")['message_id']

    # Edit message
    assert message_edit(url, user_list['token1'], message_ID2, "") == SUCCESS

    # Get message from channel messages
    messages = channel_messages(url, user_list['token1'], channel_list['c1_id'], 0)['messages']
    message_id_at_index_zero = messages[0]['message_id']
    assert message_ID1 == message_id_at_index_zero


# TODO: message/sendlater

# message/react

## VALID CASES ##

def test_react_owner_not_own_success(url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])

    # msg1_id = msg.message_send(data['token2'], data['c1_id'], "This message will be reacted by person 1")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "This message will be reacted by person 1")['message_id']
    
    # assert msg.message_react(data['token1'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token1'], msg1_id, 1) == SUCCESS

# React by member in the channel - not their message
def test_react_member_not_own_success (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])

    # msg1_id = msg.message_send(data['token2'], data['c1_id'], "This message will be reacted by person 2")['message_id']
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be reacted by person 2")['message_id']

    # assert msg.message_react(data['token2'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token2'], msg1_id, 1) == SUCCESS

def test_react_owner_own_success (url, user_list, channel_list):
    # msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be reacted by person 1 who sent it")['message_id']
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be reacted by person 1 who sent it")['message_id']

    # assert msg.message_react(data['token1'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token1'], msg1_id, 1) == SUCCESS

def test_react_member_own_success (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])

    #msg1_id = msg.message_send(data['token2'], data['c1_id'], "This message will be reacted by person 2 for their own message")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "This message will be reacted by person 2 for their own message")['message_id']

    #assert msg.message_react(data['token2'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token2'], msg1_id, 1) == SUCCESS

# React by a user and then reacted by another user
def test_react_by_two_users (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    # channel.channel_join(data['token3'], data['c1_id'])
    channel_join(url, user_list['token3'], channel_list['c1_id'])
    # msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message was sent by person 1 but will be reacted by two people")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "This message was sent by person 1 but will be reacted by two people")['message_id']
    # assert msg.message_react(data['token2'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token2'], msg1_id, 1) == SUCCESS
    # assert msg.message_react(data['token3'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token3'], msg1_id, 1) == SUCCESS


## INVALID CASES ##

def test_react_message_id_not_in_channel (url, user_list, channel_list):
    # msg1_id = msg.message_send(data['token2'], data['c2_id'], "This message was sent in channel 2")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message was sent in channel 2")['message_id']
    # with pytest.raises(InputError):
    # msg.message_react(data['token1'], msg1_id, 1)
    assert message_react(url, user_list['token1'], msg1_id, 1) == ERROR

def test_react_invalid_react (url, user_list, channel_list):
    # msg1_id = msg.message_send(data['token2'], data['c2_id'], "This will be reacted by an invalid message id")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This will be reacted by an invalid message id")['message_id']
    # with pytest.raises(InputError):
    # msg.message_react(data['token2'], msg1_id, 2)
    assert message_react(url, user_list['token2'], msg1_id, 2) == ERROR

def test_react_already_reacted_by_user (url, user_list, channel_list):
    # msg1_id = msg.message_send(data['token2'], data['c2_id'], "Will be reacted by the user twice ")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "Will be reacted by the user twice")['message_id']
    # assert msg.message_react(data['token2'], msg1_id, 1) == SUCCESS
    assert message_react(url, user_list['token2'], msg1_id, 1) == SUCCESS
    # with pytest.raises(InputError):
    # msg.message_react(data['token2'], msg1_id, 1)
    assert message_react(url, user_list['token2'], msg1_id, 1) == ERROR

# message/unreact

## VALID CASES ##
def test_unreact_owner_not_own_success (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    # msg1_id = msg.message_send(data['token2'], data['c1_id'], "This message will be unreacted by person 1")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "This message will be unreacted by person 1")['message_id']
    # msg.message_react(data['token1'], msg1_id, 1)
    message_react(url, user_list['token1'], msg1_id, 1)
    #assert msg.message_unreact(data['token1'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token1'], msg1_id, 1) == SUCCESS

def test_unreact_member_not_own_success (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    # msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be unreacted by person 2")['message_id']
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be unreacted by person 2")['message_id']
    # msg.message_react(data['token2'], msg1_id, 1)
    message_react(url, user_list['token2'], msg1_id, 1)
    # assert msg.message_unreact(data['token2'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token2'], msg1_id, 1) == SUCCESS

def test_unreact_owner_own_success (url, user_list, channel_list):
    #  msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message will be unreacted by person 1 who sent it")['message_id']
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be unreacted by person 1 who sent it")['message_id']
    # msg.message_react(data['token1'], msg1_id, 1)
    message_react(url, user_list['token1'], msg1_id, 1)
    # assert msg.message_unreact(data['token1'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token1'], msg1_id, 1) == SUCCESS

def test_unreact_member_own_success (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    # msg1_id = msg.message_send(data['token2'], data['c1_id'], "This message will be unreacted by person 2 for their own message")['message_id']
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "This message will be unreacted by person 2 for their own message")['message_id']
    #  msg.message_react(data['token2'], msg1_id, 1)
    message_react(url, user_list['token2'], msg1_id, 1)
    # assert msg.message_unreact(data['token2'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token2'], msg1_id, 1) == SUCCESS

def test_unreact_unreact_by_two_users (url, user_list, channel_list):
    # channel.channel_join(data['token2'], data['c1_id'])
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    # channel.channel_join(data['token3'], data['c1_id'])
    channel_join(url, user_list['token3'], channel_list['c1_id'])
    # msg1_id = msg.message_send(data['token1'], data['c1_id'], "This message was sent by person 1 but will be unreacted by two people")['message_id']
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message was sent by person 1 but will be unreacted by two people")['message_id']
    # msg.message_react(data['token2'], msg1_id, 1)
    message_react(url, user_list['token2'], msg1_id, 1) 
    # msg.message_react(data['token3'], msg1_id, 1)
    message_react(url, user_list['token3'], msg1_id, 1) 
    # assert msg.message_unreact(data['token2'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token2'], msg1_id, 1) == SUCCESS
    # assert msg.message_unreact(data['token3'], msg1_id, 1) == SUCCESS
    assert message_unreact(url, user_list['token3'], msg1_id, 1) == SUCCESS

# message/pin
'''
pin(token, message_id) = {}
'''

## VALID CASES ##

# Pin one message
def test_single_msg_pin(url, user_list, channel_list):
    # Send messages
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned")['message_id']
    message_send(url, user_list['token1'], channel_list['c1_id'], "This message will not be pinned")

    # Pin message
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS

# Pin two messages
def test_double_msg_pin(url, user_list, channel_list):
    # Send messages
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned")['message_id']
    msg2_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will also be pinned")['message_id']

    # Pin messages
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS
    assert message_pin(url, user_list['token1'], msg2_id) == SUCCESS

# A channel owner can pin a message sent by a regular member
def test_pin_by_owner(url, user_list, channel_list):
    # Join channel and send message
    channel_join(url, user_list['token3'], channel_list['c2_id'])
    msg1_id = message_send(url, user_list['token3'], channel_list['c2_id'], "This message was sent by a regular member and it will be pinned")['message_id']

    # Owner pins
    assert message_pin(url, user_list['token2'], msg1_id) == SUCCESS

# The Flockr owner does not have to be a channel owner to pin a message
def test_pin_flockr_owner(url, user_list, channel_list):
    # FO joins channel
    channel_join(url, user_list['token1'], channel_list['c2_id'])

    # Onwer sends message
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message was sent by an owner and it will be pinned")['message_id']

    # FO pins message
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS

## INVALID CASES ##

# Pinning a message which is already pinned
def test_pin_existing(url, user_list, channel_list):
    # Send message
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned")['message_id']
    
    # Pin message
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS
    
    # Pin the same message
    assert message_pin(url, user_list['token1'], msg1_id) == ERROR

# Pinning a message in a channel which you are not in
def test_pin_in_another_channel(url, user_list, channel_list):
    # Send message
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message will be pinned by a channel owner")['message_id']
    msg2_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message cannot be pinned")['message_id']

    # Pin one
    assert message_pin(url, user_list['token2'], msg1_id) == SUCCESS

    # P3 becomes an owner of the other channel
    channel_join(url, user_list['token3'], channel_list['c1_id'])
    channel_addowner(url, user_list['token1'], channel_list['c1_id'], user_list['u3_id'])
    
    # Neither P3 or P1 can pin the other message in C2
    assert message_pin(url, user_list['token3'], msg2_id) == ERROR
    assert message_pin(url, user_list['token1'], msg2_id) == ERROR

# A normal member cannot pin a message even if it is their own
def test_pin_but_not_owner(url, user_list, channel_list):
    # Join channel
    channel_join(url, user_list['token2'], channel_list['c1_id'])

    # Send message
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "I am a normal owner. I cannot pin this :(")['message_id']
    
    # Cannot pin this message
    assert message_pin(url, user_list['token2'], msg1_id) == ERROR


# message_unpin
'''
message_unpin(token, message_id) = {}
'''


# Unpin a pinned message
def test_single_msg_unpin(url, user_list, channel_list):
    # Send message
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned")['message_id']

    # Pin message
    message_pin(url, user_list['token1'], msg1_id)

    # Unpin the same message
    assert message_unpin(url, user_list['token1'], msg1_id) == SUCCESS

# Unpin multiple pinned messages
def test_double_msg_unpin(url, user_list, channel_list):
    # Send messages
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned")['message_id']
    msg2_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will also be pinned")['message_id']
    
    # Pin both messages
    message_pin(url, user_list['token1'], msg1_id)
    message_pin(url, user_list['token1'], msg2_id)

    # Unpin both messages
    assert message_unpin(url, user_list['token1'], msg1_id) == SUCCESS
    assert message_unpin(url, user_list['token1'], msg2_id) == SUCCESS

# A channel owner can unpin a message send by someone else
def test_unpin_by_another_owner(url, user_list, channel_list):
    # Join channel and send a message
    channel_join(url, user_list['token3'], channel_list['c2_id'])
    msg1_id = message_send(url, user_list['token3'], channel_list['c2_id'], "This message was sent by a regular member and it will be pinned")['message_id']

    # Owner pins
    message_pin(url, user_list['token2'], msg1_id)

    # Add P3 as an owner and get them to unpin
    channel_addowner(url, user_list['token2'], channel_list['c2_id'], user_list['u3_id'])
    assert message_unpin(url, user_list['token3'], msg1_id) == SUCCESS

# The Flockr owner does not have to be a channel owner to pin a message
def test_unpin_flockr_owner(url, user_list, channel_list):
    # Send and pin a message
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message was sent by an owner and it will be pinned")['message_id']
    message_pin(url, user_list['token2'], msg1_id)

    # Join and attempt to unpin
    channel_join(url, user_list['token1'], channel_list['c2_id'])
    assert message_unpin(url, user_list['token1'], msg1_id) == SUCCESS

# You can repin a message when it has been unpinned
def test_pin_unpin(url, user_list, channel_list):
    # Send a message
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message will be pinned over and over")['message_id']

    # Start annoying everyone
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS
    assert message_unpin(url, user_list['token1'], msg1_id) == SUCCESS
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS
    assert message_unpin(url, user_list['token1'], msg1_id) == SUCCESS

## INVALID CASES ##

# Unpinning a message which is not pinned
def test_unpin_normal_msg(url, user_list, channel_list):
    # Send a message
    msg1_id = message_send(url, user_list['token1'], channel_list['c1_id'], "This message cannot be unpinned")['message_id']
    
    # Attempt to unpin
    assert message_unpin(url, user_list['token1'], msg1_id) == ERROR

# Unpinning a message in a channel which you are not in
def test_unpin_in_another_channel(url, user_list, channel_list):
    # Send and pin a message
    msg1_id = message_send(url, user_list['token2'], channel_list['c2_id'], "This message can only be unpinned by a channel owner")['message_id']
    assert message_pin(url, user_list['token2'], msg1_id) == SUCCESS

    # Another user joins another channel and becomes owner
    channel_join(url, user_list['token3'], channel_list['c1_id'])
    channel_addowner(url, user_list['token1'], channel_list['c1_id'], user_list['u3_id'])

    # Attempt to unpin from another channel
    assert message_unpin(url, user_list['token3'], msg1_id) == ERROR
    assert message_unpin(url, user_list['token1'], msg1_id) == ERROR

# A normal member cannot unpin a message even if it is their own
def test_unpin_but_not_owner(url, user_list, channel_list):
    # Join channel
    channel_join(url, user_list['token2'], channel_list['c1_id'])
    
    # Send message and get owner to pin it
    msg1_id = message_send(url, user_list['token2'], channel_list['c1_id'], "I am a normal owner. I cannot unpin this :(")['message_id']
    assert message_pin(url, user_list['token1'], msg1_id) == SUCCESS

    # Message sender is not owner and cannot unpin
    assert message_unpin(url, user_list['token2'], msg1_id) == ERROR
