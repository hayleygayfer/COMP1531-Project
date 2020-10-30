import requests
import json 
from echo_http_test import url
import auth
import pytest

## Fixtures
@pytest.fixture
def userObject(url):
    requests.delete(url + 'clear')
    payload = {"email":"tonystark@avengers.com", "password": "password", "name_first": "Tony", "name_last": "Stark"}
    response = requests.post(url + "auth/register", json=payload)
    return response.json()

###### User Profile ######

def test_valid_user_profile_http(userObject, url):
    params = {'token': userObject['token'], 'u_id': userObject['u_id']}
    response = requests.get(url + 'user/profile', params=params)
    assert response.status_code == 200
    user = response.json().get('user')
    assert user['handle_str'] == 'tonystark'
    assert user['u_id'] == 1
    assert user['email'] == 'tonystark@avengers.com'
    assert user['name_first'] == 'Tony'
    assert user['name_last'] == 'Stark'

def test_no_users_user_profile_http(url):
    requests.delete(url + 'clear')
    # No users created -> invalid u_id
    params = {'token': 'token', 'u_id': 1}
    response = requests.get(url + 'user/profile', params=params)
    assert response.status_code == 400

def test_invalid_u_id_http(userObject, url):
    # Testing invalid u_id
    params = {'token': userObject['token'], 'u_id': 2}
    response = requests.get(url + 'user/profile', params=params)
    assert response.status_code == 400

def test_invalid_token(userObject, url):
    # Testing invalid token
    params = {'token': 'invalidtoken', 'u_id': userObject['u_id']}
    response = requests.get(url + 'user/profile', params=params)
    assert response.status_code == 400


###### User Profile Setname ######

# Valid Cases

def test_valid_set_first_name(userObject, url):
    initialUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests initial name
    assert initialUser['name_first'] == 'Tony'

    # Changes name
    payload = {'token': userObject['token'], 'name_first': 'Anthony', 'name_last': 'Stark' }
    requests.put(url + 'user/profile/setname', json=payload)
    updatedUser = retrieveUser(userObject['token'], userObject['u_id'], url)
    # Tests changed name
    assert updatedUser['name_first'] == 'Anthony'


def test_valid_set_last_name(userObject, url):
    initialUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests initial name
    assert initialUser['name_last'] == 'Stark'

    # Changes name
    payload = {'token': userObject['token'], 'name_first': 'Tony', 'name_last': 'Potts' }
    requests.put(url + 'user/profile/setname', json=payload)
    updatedUser = retrieveUser(userObject['token'], userObject['u_id'], url)


    # Tests changed name
    assert updatedUser['name_last'] == 'Potts'

# Invalid Cases

def test_set_invalid_first_name(userObject, url):
    # Edge Case: 0 length first name
    payload = {'token': userObject['token'], 'name_first': '', 'name_last': 'Stark' }
    response = requests.put(url + 'user/profile/setname', json=payload)
    assert response.status_code == 400

    # Edge Case: 51 length first name
    payload = {'token': userObject['token'], 'name_first': 'Tonytonytonytonytonytonytonytonytonytonytonytonyton', 'name_last': 'Stark' }
    response = requests.put(url + 'user/profile/setname', json=payload)
    assert response.status_code == 400


def test_set_invalid_last_name(userObject, url):
    # Edge Case: 0 length last name
    payload = {'token': userObject['token'], 'name_first': 'Tony', 'name_last': '' }
    response = requests.put(url + 'user/profile/setname', json=payload)
    assert response.status_code == 400

    # Edge Case: 51 length last name
    payload = {'token': userObject['token'], 'name_first': 'Tony', 'name_last': 'StarkStarkStarkStarkStarkStarkStarkStarkStarkStarkS' }
    response = requests.put(url + 'user/profile/setname', json=payload)
    assert response.status_code == 400


def test_invalid_token_set_name(userObject, url):
    # Invalid Token
    payload = {'token': 'invalidtoken', 'name_first': 'Tony', 'name_last': 'Stark' }
    response = requests.put(url + 'user/profile/setname', json=payload)
    assert response.status_code == 400


###### User Profile Setemail ######

# Valid Cases

def test_valid_set_email(userObject, url):
    initialUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests initial name
    assert initialUser['email'] == 'tonystark@avengers.com'

    # Changes email
    payload = {'token': userObject['token'], 'email': 'tony@avengers.com'}
    requests.put(url + 'user/profile/setemail', json=payload)

    updatedUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests changed name
    assert updatedUser['email'] == 'tony@avengers.com'

# Invalid Cases

def test_invalid_set_email(userObject, url):
    # Invalid Email Formats

    # Missing @ in email
    payload = {'token': userObject['token'], 'email': 'tonystark.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400
        
    # Missing domain in email
    payload = {'token': userObject['token'], 'email': 'tonystark@.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400

    # Invalid character in email username
    payload = {'token': userObject['token'], 'email': 'tony$tark@avengers.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400
        
    # Missing email username
    payload = {'token': userObject['token'], 'email': '@avengers.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400


def test_duplicate_email(userObject, url):
    payload = {"email":"steverodgers@avengers.com", "password": "password", "name_first": "Steve", "name_last": "Rodgers"}
    response = requests.post(url + "auth/register", json=payload)

    # Checks for duplicate email
    payload = {'token': userObject['token'], 'email': 'steverodgers@avengers.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400


def test_invalid_token_set_email(userObject, url):
    # Invalid Token
    payload = {'token': 'invalidtoken', 'email': 'tonystark@avengers.com'}
    response = requests.put(url + 'user/profile/setemail', json=payload)
    assert response.status_code == 400


###### User Profile Sethandle ######

# Valid Cases

def test_valid_set_handle(userObject, url):
    initialUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests initial name
    assert initialUser['handle_str'] == 'tonystark'

    # Changes handle
    payload = {'token': userObject['token'], 'handle_str': 'tony'}
    requests.put(url + 'user/profile/sethandle', json=payload)
    updatedUser = retrieveUser(userObject['token'], userObject['u_id'], url)

    # Tests changed name
    assert updatedUser['handle_str'] == 'tony'

# Invalid Cases


def test_invalid_set_handle(userObject, url):

    # Handle Already Exists
    payload = {"email":"steverodgers@avengers.com", "password": "password", "name_first": "Steve", "name_last": "Rodgers"}
    response = requests.post(url + "auth/register", json=payload)

    payload = {'token': userObject['token'], 'handle_str': 'steverodgers'}
    response = requests.put(url + 'user/profile/sethandle', json=payload)
    assert response.status_code == 400
    
    # Edge Case: 3 characters handle (not inclusive)
    payload = {'token': userObject['token'], 'handle_str': 'ton'}
    response = requests.put(url + 'user/profile/sethandle', json=payload)
    assert response.status_code == 400

    # Edge Case: 20 Characters
    payload = {'token': userObject['token'], 'handle_str': 'tony1234567891011121'}
    response = requests.put(url + 'user/profile/sethandle', json=payload)
    assert response.status_code == 400

    
def test_invalid_token_set_handle(userObject, url):
    # Invalid Token
    payload = {'token': 'invalidtoken', 'handle_str': 'tony'}
    response = requests.put(url + 'user/profile/sethandle', json=payload)
    assert response.status_code == 400

###### Helper Functions ######

# Retrieves information about a user
def retrieveUser(token, u_id, url):
    params = {'token': token, 'u_id': int(u_id)}
    response = requests.get(url + 'user/profile', params=params)
    return response.json().get('user')
