import auth
import pytest
from other import clear
from error import InputError
from user import user_profile

###### Auth Register ######

# EXCEPTIONS #

def test_duplicate_name_handle():
    clear()
    # duplicate people
    user1 = auth.auth_register("clint@braton.com", "password", "Clint", "Barton")
    user2 = auth.auth_register("clint@notbarton.com", "password", "Clint", "Barton")

    user_1 = user_profile(user1['token'], user1['u_id'])
    user_2 = user_profile(user2['token'], user2['u_id'])

    assert user_1['handle_str'] != user_2['handle_str']
 
# Invalid Email
def test_invalid_email():
    clear()
    # Missing @ in email
    with pytest.raises(InputError):
        auth.auth_register("clintbarton.com", "password", "Clint", "Barton")
        
    # Missing domain in email
    with pytest.raises(InputError):
        auth.auth_register("steverodgers@.com", "password", "Steve", "Rodgers")
        
    # Invalid character in email username
    with pytest.raises(InputError):
        auth.auth_register("nata$haromanoff@avengers.com", "password", "Natasha", "Romanoff")
        
    # Missing email username
    with pytest.raises(InputError):
        auth.auth_register("@avengers.com", "password", "Pepper", "Potts")
    
# Duplicate Email
def test_duplicate_email_address():
    clear()
    result = auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    assert(result != None)
    
    # Checking duplicate register
    with pytest.raises(InputError):
        auth.auth_register("tonystark@avengers.com", "password", "Anthony", "Stark")

# Invalid Password
def test_invalid_password():
    clear()
    # Empty password
    with pytest.raises(InputError):
        auth.auth_register("nickfury@avengers.com", "", "Nick", "Fury")
        
    # Under 6 letter password
    with pytest.raises(InputError):
        auth.auth_register("nickfury@avengers.com", "123", "Nick", "Fury")
        
    # Edge case, 5 letter password
    with pytest.raises(InputError):
        auth.auth_register("nickfury@avengers.com", "12345", "Nick", "Fury")

# Invalid First Name
def test_invalid_first_name():
    clear()
    # Empty first name
    with pytest.raises(InputError):
        auth.auth_register("stanlee@avengers.com", "password", "", "Lee")
        
    # First name over 50 characters
    with pytest.raises(InputError):
        auth.auth_register("stanlee@avengers.com", "password", "stanstanstanstanstanstanstanstanstanstanstanstansta", "Lee")

#Invalid Last Name
def test_invalid_last_name():
    clear()
    # Empty last name
    with pytest.raises(InputError):
        auth.auth_register("stanlee@avengers.com", "password", "Stan", "")
    
    # Last name over 50 characters
    with pytest.raises(InputError):
        auth.auth_register("stanlee@avengers.com", "password", "Stan", "LeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLee")

# VALID CASES #

def test_alternative_valid_emails():
    clear()
    # Underscore in email username
    result = auth.auth_register("bruce_banner@avengers.com", "password", "Bruce", "Banner")
    assert(result != None)
    # Full stop in email username
    result = auth.auth_register("thor.odinson@avengers.com", "password", "Thor", "Odinson")
    assert(result != None)
    
def test_valid_passwords():
    clear()
    # Password with edge case amount of characters (6) and with all numbers
    result = auth.auth_register("nickfury@avengers.com", "123456", "Nick", "Fury")
    assert (result != None)
    
    # Password in all uppercase characters
    result = auth.auth_register("mariahill@avengers.com", "PASSWORD", "Maria", "Hill")
    assert(result != None)
    
    # Password with a mix of upper case, lower case and number characters
    result = auth.auth_register("happyhogan@avengers.com", "123FOURfive6", "Happy", "Hogan")
    assert(result != None)
    
def test_valid_first_name():
    clear()
    # First name with 1 character (edge case)
    result = auth.auth_register("stanlee@avengers.com", "password", "S", "Lee")
    assert(result != None)
    
    # First name with 50 characters (edge case)
    result = auth.auth_register("scottlang@avengers.com", "password", "ScottScottScottScottScottScottScottScottScottScott", "Lang")
    assert(result != None)
    
def test_valid_last_name():
    clear()
    # Last name with 1 character (edge case)
    result = auth.auth_register("peterparker@avengers.com", "password", "Peter", "P")
    assert(result != None)
    
    # Last name with 50 characters (edge case)
    result = auth.auth_register("peterquill@avengers.com", "password", "Peter", "QuillQuillQuillQuillQuillQuillQuillQuillQuillQuill")
    assert(result != None)


###### Auth Login & Auth Lougout ######

'''
First test case to check for valid email will be checked in auth_register. Thus it will be covered under the next test case (checking
whether an email belongs to a user)
'''

# EXCEPTIONS #

# Email does not belong to a user
def test_email_not_belong_to_user():
    clear()
    with pytest.raises(InputError):
        auth.auth_login("tonystark@avengers.com", "password")

# Password is invalid
def test_password_incorrect():
    clear()
    auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    with pytest.raises(InputError):
        auth.auth_login("tonystark@avengers.com", "hello1234")
        
# Logout with invalid token
def test_invalid_logout():
    clear()
    assert(auth.auth_logout(1)['is_success'] == False)
        
# VALID CASES #

# Test Register, Login, Logout
def test_register_login_logout():
    clear()
    
    # Register
    result = auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    token = result['token']
    u_id = result['u_id']

    assert token != None and u_id != None
    
    # Login
    result = auth.auth_login("tonystark@avengers.com", "password")
    u_id1 = result['u_id']
    token1 = result['token']

    assert u_id1 == u_id and token == token1
    
    # Logout
    assert(auth.auth_logout(token)['is_success'] == True)
    

    
    
    





