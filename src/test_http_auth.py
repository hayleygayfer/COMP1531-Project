import requests
import json 
from echo_http_test import url
import auth
import pytest

###### Auth Register ######

# EXCEPTIONS #

# Invalid Email
def test_invalid_email_http(url):
    requests.delete(url + 'clear')
    # Missing @ in email
    payload = {"email":"clintbarton.com", "password": "password", "name_first": "Clint", "name_last": "Barton"}
    response = requests.post(url + "auth/register", json=payload)
    print(response.json())
    assert (response.status_code == 400)
        
    # Missing domain in email
    payload = {"email":"steverodgers@.com", "password": "password", "name_first": "Steve", "name_last": "Rodgers"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)
        
    # Invalid character in email username
    payload = {"email":"nata$haromanoff@avengers.com", "password": "password", "name_first": "Natasha", "name_last": "Romanoff"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)
        
    # Missing email username
    payload = {"email":"@avengers.com", "password": "password", "name_first": "Pepper", "name_last": "Potts"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)

# Duplicate Email
def test_duplicate_email_address_http(url):
    requests.delete(url + 'clear')
    payload = {"email":"tonystark@avengers.com", "password": "password", "name_first": "Tony", "name_last": "Stark"}
    response = requests.post(url + "auth/register", json=payload)
    print(response.json())
    assert (response.status_code == 200)

    payload = {"email":"tonystark@avengers.com", "password": "password", "name_first": "Anthony", "name_last": "Stark"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)


# Invalid Password
def test_invalid_password_http(url):
    requests.delete(url + 'clear')
    # Empty password
    payload = {"email":"nickfury@avengers.com", "password": "", "name_first": "Nick", "name_last": "Fury"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)

        
    # Under 6 letter password
    payload = {"email":"nickfury@avengers.com", "password": "123", "name_first": "Nick", "name_last": "Fury"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)
        
    # Edge case, 5 letter password
    payload = {"email":"nickfury@avengers.com", "password": "12345", "name_first": "Nick", "name_last": "Fury"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)

# Invalid First Name
def test_invalid_first_name_http(url):
    requests.delete(url + 'clear')
    # Empty first name
    payload = {"email":"stanlee@avengers.com", "password": "password", "name_first": "", "name_last": "Lee"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)
        
    # First name over 50 characters
    payload = {"email":"stanlee@avengers.com", "password": "password", "name_first": "stanstanstanstanstanstanstanstanstanstanstanstansta", "name_last": "Lee"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)


#Invalid Last Name
def test_invalid_last_name_http(url):
    requests.delete(url + 'clear')
    # Empty last name
    payload = {"email":"stanlee@avengers.com", "password": "password", "name_first": "Stan", "name_last": ""}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)
    
    # Last name over 50 characters
    payload = {"email":"stanlee@avengers.com", "password": "password", "name_first": "Stan", "name_last": "LeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLee"}
    response = requests.post(url + "auth/register", json=payload)
    assert (response.status_code == 400)


# VALID CASES #

def test_alternative_valid_emails_http(url):
    requests.delete(url + 'clear')

    # Underscore in email username
    payload = {"email":"bruce_banner@avengers.com", "password": "password", "name_first": "Bruce", "name_last": "Banner"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 1
    
    # Full stop in email username
    payload = {"email":"thor.odinson@avengers.com", "password": "password", "name_first": "Thor", "name_last": "Odinson"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 2


def test_valid_passwords_http(url):
    requests.delete(url + 'clear')

    # Password with edge case amount of characters (6) and with all numbers
    payload = {"email":"nickfury@avengers.com", "password": "123456", "name_first": "Nick", "name_last": "Fury"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 1

    
    # Password in all uppercase characters
    payload = {"email":"mariahill@avengers.com", "password": "PASSWORD", "name_first": "Maria", "name_last": "Hill"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 2


    
    # Password with a mix of upper case, lower case and number characters
    payload = {"email":"happyhogan@avengers.com", "password": "123FOURfive6", "name_first": "Happy", "name_last": "Hogan"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 3

    

def test_valid_first_name_http(url):
    requests.delete(url + 'clear')

    # First name with 1 character (edge case)
    payload = {"email":"stanlee@avengers.com", "password": "password", "name_first": "S", "name_last": "Lee"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 1

    
    # First name with 50 characters (edge case)
    payload = {"email":"scottlang@avengers.com", "password": "password", "name_first": "ScottScottScottScottScottScottScottScottScottScott", "name_last": "Lang"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 2


def test_valid_last_name_http(url):
    requests.delete(url + 'clear')
    
    # Last name with 1 character (edge case)
    payload = {"email":"peterparker@avengers.com", "password": "password", "name_first": "Peter", "name_last": "P"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 1

    
    # Last name with 50 characters (edge case)
    payload = {"email":"peterquill@avengers.com", "password": "password", "name_first": "Peter", "name_last": "QuillQuillQuillQuillQuillQuillQuillQuillQuillQuill"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 2


###### Auth Login & Auth Lougout ######

# EXCEPTIONS #

# Email does not belong to a user
def test_email_not_belong_to_user_http(url):
    requests.delete(url + 'clear')

    payload = {"email":"tonystark@avengers.com", "password": "password"}
    response = requests.post(url + "auth/login", json=payload)
    assert (response.status_code == 400)


# Password is invalid
def test_password_incorrect_http(url):
    requests.delete(url + 'clear')

    payload = {"email":"tonystark@avengers.com", "password": "password", "name_first": "Tony", "name_last": "Stark"}
    response = requests.post(url + "auth/register", json=payload)
    assert response.json()['u_id'] == 1

    payload = {"email":"tonystark@avengers.com", "password": "hello1234"}
    response = requests.post(url + "auth/login", json=payload)
    assert (response.status_code == 400)
        
# Logout with invalid token
def test_invalid_logout(url):
    requests.delete(url + 'clear')

    payload = {'token': 'invalidtoken'}
    response = requests.post(url + 'auth/logout', json=payload)
    assert response.json() == {'is_success': False}
        
# VALID CASES #

# Test Register, Login, Logout
def test_register_login_logout_http(url):
    requests.delete(url + 'clear')
    
    # Register
    payload = {"email":"tonystark@avengers.com", "password": "password", "name_first": "Tony", "name_last": "Stark"}
    response = requests.post(url + "auth/register", json=payload)
    token = response.json()['token']
    u_id = response.json()['u_id']

    assert token != None and u_id != None
    
    # Login
    payload = {"email":"tonystark@avengers.com", "password": "password"}
    response = requests.post(url + "auth/login", json=payload)
    u_id1 = response.json()['u_id']
    token1 = response.json()['token']

    assert u_id1 == u_id and token == token1
    
    # Logout
    payload = {'token': token1}
    response = requests.post(url + 'auth/logout', json=payload)
    assert response.json() == {'is_success': True}
