import pytest
import auth
import user

from error import InputError, AccessError
from other import clear
from data import data


## Fixtures
@pytest.fixture
def userObject():
    clear()
    auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    user = auth.auth_login("tonystark@avengers.com", "password")
    return {'u_id': user['u_id'], 'token': user['token']}

###### User Profile ######

def test_valid_user_profile(userObject):
    response = user.user_profile(userObject['token'], userObject['u_id'])
    assert response['handle_str'] == 'tonystark'
    assert response['u_id'] == 1
    assert response['email'] == 'tonystark@avengers.com'
    assert response['name_first'] == 'Tony'
    assert response['name_last'] == 'Stark'

def test_no_users_user_profile():
    clear()
    # No users created -> invalid id
    with pytest.raises(InputError):
        user.user_profile('token', 1)

def test_invalid_u_id(userObject):
    # Testing invalid u_id
    with pytest.raises(InputError):
        user.user_profile(userObject['token'], 2)

def test_invalid_token(userObject):
    # Testing invalid token
    with pytest.raises(AccessError):
        user.user_profile('invalidtoken', userObject['u_id'])

    
###### User Profile Setname ######

# Valid Cases

def test_valid_set_first_name(userObject):
    initialUser = retrieveUser(userObject['u_id'])

    # Tests initial name
    assert initialUser['name_first'] == 'Tony'
    user.user_setname(userObject['token'], 'Anthony', 'Stark')
    updatedUser = retrieveUser(userObject['u_id'])

    # Tests changed name
    assert updatedUser['name_first'] == 'Anthony'


def test_valid_set_last_name(userObject):
    initialUser = retrieveUser(userObject['u_id'])

    # Tests initial name
    assert initialUser['last_name'] == 'Stark'
    user.user_setname(userObject['token'], 'Tony', 'Potts')
    updatedUser = retrieveUser(userObject['u_id'])

    # Tests changed name
    assert updatedUser['name_last'] == 'Potts'

# Invalid Cases

def test_set_invalid_first_name(userObject):
    # Edge Case: 0 length first name
    with pytest.raises(InputError):
        user.user_setname(userObject['token'], '', 'Stark')

    # Edge Case: 51 length first name
    with pytest.raises(InputError):
        user.user_setname(userObject['token'], 'Tonytonytonytonytonytonytonytonytonytonytonytonyton', 'Stark')

def test_set_invalid_last_name(userObject):
    # Edge Case: 0 length last name
    with pytest.raises(InputError):
        user.user_setname(userObject['token'], 'Tony', '')

    # Edge Case: 51 length last name
    with pytest.raises(InputError):
        user.user_setname(userObject['token'], 'Tony', 'StarkStarkStarkStarkStarkStarkStarkStarkStarkStarkS')
 
 def test_invalid_token_set_name(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_setname('invalidtoken', 'Anthony', 'Stark')


###### User Profile Setemail ######

# Valid Cases

def test_valid_set_email(userObject):
    initialUser = retrieveUser(userObject['u_id'])

    # Tests initial name
    assert initialUser['email'] == 'tonystark@avengers.com'
    user.user_setemail(userObject['token'], 'tony@avengers.com')
    updatedUser = retrieveUser(userObject['u_id'])

    # Tests changed name
    assert updatedUser['email'] == 'tony@avengers.com'

# Invalid Cases

def test_invalid_set_email(userObject):
    # Invalid Email Formats

    # Missing @ in email
    with pytest.raises(InputError):
        user.user_setemail(userObject['token'], 'tonystark.com')
        
    # Missing domain in email
    with pytest.raises(InputError):
        user.user_setemail(userObject['token'], 'tonystark@.com')
        
    # Invalid character in email username
    with pytest.raises(InputError):
        user.user_setemail(userObject['token'], 'tony$tark@avengers.com')
        
    # Missing email username
    with pytest.raises(InputError):
        user.user_setemail(userObject['token'], '@avengers.com')

def test_duplicate_email(userObject):
    auth.auth_register("steverodgers@avengers.com", "password", "Steve", "Rodgers")

    # Checks for duplicate email
    with pytest.raises(InputError):
        user.user_setemail(userObject['token'], 'steverodgers@avengers.com')

 def test_invalid_token_set_email(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_setemail('invalidtoken', 'tony@avengers.com')


###### User Profile Sethandle ######

# Valid Cases

def test_valid_set_handle(userObject):
    initialUser = retrieveUser(userObject['u_id'])

    # Tests initial name
    assert initialUser['handle_str'] == 'tonystark'
    user.user_sethandle(userObject['token'], 'tony')
    updatedUser = retrieveUser(userObject['u_id'])

    # Tests changed name
    assert updatedUser['handle_str'] == 'tony'

# Invalid Cases


def test_invalid_set_handle(userObject):

    # Handle Already Exists
    auth.auth_register("steverodgers@avengers.com", "password", "Steve", "Rodgers")
    with pytest.raises(InputError):
        user.user_sethandle(userObject['token'], 'steverodgers')
    
    # Edge Case: 3 characters handle (not inclusive)
    with pytest.raises(InputError):
        user.user_sethandle(userObject['token'], 'ton')

    # Edge Case: 20 Characters
    with pytest.raises(InputError):
        user.user_sethandle(userObject['token'], 'tony1234567891011121')

    
def test_invalid_token_set_handle(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_sethandle('invalidtoken', 'tony')


###### Helper Functions ######

# Retrieves information about a user
def retrieveUser(u_id):
    for user in data['users']:
        if u_id == user['u_id']:
            return user
    return None
