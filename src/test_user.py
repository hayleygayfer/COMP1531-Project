import pytest
import auth
import user

from error import InputError, AccessError
from other import clear

from urllib import request
from PIL import Image # pip3 install Pillow

SUCCESS = {}

## Fixtures
@pytest.fixture
def userObject():
    clear()
    auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    flockr_user = auth.auth_login("tonystark@avengers.com", "password")
    return {'u_id': flockr_user['u_id'], 'token': flockr_user['token']}

###### User Profile ######

def test_valid_user_profile(userObject):
    response = user.user_profile(userObject['token'], userObject['u_id'])['user']
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
    initialUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests initial name
    assert initialUser['name_first'] == 'Tony'
    user.user_profile_setname(userObject['token'], 'Anthony', 'Stark')
    updatedUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests changed name
    assert updatedUser['name_first'] == 'Anthony'


def test_valid_set_last_name(userObject):
    initialUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests initial name
    assert initialUser['name_last'] == 'Stark'
    user.user_profile_setname(userObject['token'], 'Tony', 'Potts')
    updatedUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests changed name
    assert updatedUser['name_last'] == 'Potts'

# Invalid Cases

def test_set_invalid_first_name(userObject):
    # Edge Case: 0 length first name
    with pytest.raises(InputError):
        user.user_profile_setname(userObject['token'], '', 'Stark')

    # Edge Case: 51 length first name
    with pytest.raises(InputError):
        user.user_profile_setname(userObject['token'], 'Tonytonytonytonytonytonytonytonytonytonytonytonyton', 'Stark')

def test_set_invalid_last_name(userObject):
    # Edge Case: 0 length last name
    with pytest.raises(InputError):
        user.user_profile_setname(userObject['token'], 'Tony', '')

    # Edge Case: 51 length last name
    with pytest.raises(InputError):
        user.user_profile_setname(userObject['token'], 'Tony', 'StarkStarkStarkStarkStarkStarkStarkStarkStarkStarkS')
 
def test_invalid_token_set_name(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_profile_setname('invalidtoken', 'Anthony', 'Stark')


###### User Profile Setemail ######

# Valid Cases

def test_valid_set_email(userObject):
    initialUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests initial name
    assert initialUser['email'] == 'tonystark@avengers.com'
    user.user_profile_setemail(userObject['token'], 'tony@avengers.com')
    updatedUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests changed name
    assert updatedUser['email'] == 'tony@avengers.com'

# Invalid Cases

def test_invalid_set_email(userObject):
    # Invalid Email Formats

    # Missing @ in email
    with pytest.raises(InputError):
        user.user_profile_setemail(userObject['token'], 'tonystark.com')
        
    # Missing domain in email
    with pytest.raises(InputError):
        user.user_profile_setemail(userObject['token'], 'tonystark@.com')
        
    # Invalid character in email username
    with pytest.raises(InputError):
        user.user_profile_setemail(userObject['token'], 'tony$tark@avengers.com')
        
    # Missing email username
    with pytest.raises(InputError):
        user.user_profile_setemail(userObject['token'], '@avengers.com')

def test_duplicate_email(userObject):
    auth.auth_register("steverodgers@avengers.com", "password", "Steve", "Rodgers")

    # Checks for duplicate email
    with pytest.raises(InputError):
        user.user_profile_setemail(userObject['token'], 'steverodgers@avengers.com')

def test_invalid_token_set_email(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_profile_setemail('invalidtoken', 'tony@avengers.com')


###### User Profile Sethandle ######

# Valid Cases

def test_valid_set_handle(userObject):
    initialUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests initial name
    assert initialUser['handle_str'] == 'tonystark'
    user.user_profile_sethandle(userObject['token'], 'tony')
    updatedUser = user.user_profile(userObject['token'], userObject['u_id'])['user']

    # Tests changed name
    assert updatedUser['handle_str'] == 'tony'

# Invalid Cases


def test_invalid_set_handle(userObject):

    # Handle Already Exists
    auth.auth_register("steverodgers@avengers.com", "password", "Steve", "Rodgers")
    with pytest.raises(InputError):
        user.user_profile_sethandle(userObject['token'], 'steverodgers')
    
    # Edge Case: 3 characters handle (not inclusive)
    with pytest.raises(InputError):
        user.user_profile_sethandle(userObject['token'], 'ton')

    # Edge Case: 20 Characters
    with pytest.raises(InputError):
        user.user_profile_sethandle(userObject['token'], 'tony1234567891011121')

    
def test_invalid_token_set_handle(userObject):
    # Invalid Token
    with pytest.raises(AccessError):
        user.user_profile_sethandle('invalidtoken', 'tony')

###### User Profile Upload Photo ######

# Valid Cases

# Upload a jpg/jpeg image with valid coordinates
def test_uploadphoto_success(userObject):
    assert user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 1, 1) == SUCCESS

    assert user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/1/14/Un_super_paysage.jpeg", 0, 0, 1, 1) == SUCCESS

# Invalid Cases

# Not uploading a jpg file
def test_uploadphoto_not_jpg(userObject):
    # png
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "http://www.pngmart.com/files/7/Red-Smoke-Transparent-Images-PNG.png", 0, 0, 1, 1)

    # gif
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "http://www.pngmart.com/files/7/Red-Smoke-Transparent-Images-PNG.png", 0, 0, 1, 1)

    # svg
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://svgsilh.com/svg/1801287.svg", 0, 0, 1, 1)

# Uploading an invalid image
def test_non_existant_img(userObject):
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://google.com/my_image.jpg", 0, 0, 1, 1)
    
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://web.flock.com/?/flock.jpg", 0, 0, 1, 1)

# Cropping an image with invalid dimensions
def test_invalid_dimensions(userObject):
    # Image Dimensions: 3456 x 2304 pixels

    # Out of range
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 3457, 2305)

    # Perfect fit
    assert user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 3456, 2304) == SUCCESS

    # x_start > x_end
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 0, 10, 100)

    # y_start > y_end
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 100, 100, 10)

    # x_start = x_end
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 100, 100, 300)

    # empty box
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 100, 100, 100)

    # negative
    with pytest.raises(InputError):
        user.user_profile_uploadphoto(userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", -1, -2, 100, 200)


