import requests
import json 
from echo_http_test import url
import auth
import pytest

SUCCESS = 200
ERROR = 400

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


###### User Profile Upload Photo ######

# Valid Cases

# Upload a jpg/jpeg image with valid coordinates
def test_uploadphoto_success(userObject, url):
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 1, 1) == SUCCESS

    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/1/14/Un_super_paysage.jpeg", 0, 0, 1, 1) == SUCCESS

# Invalid Cases

# Not uploading a jpg file
def test_uploadphoto_not_jpg(userObject, url):
    # png
    assert photo(url, userObject['token'], "http://www.pngmart.com/files/7/Red-Smoke-Transparent-Images-PNG.png", 0, 0, 1, 1) == ERROR

    # gif
    assert photo(url, userObject['token'], "http://www.pngmart.com/files/7/Red-Smoke-Transparent-Images-PNG.png", 0, 0, 1, 1) == ERROR

    # svg
    assert photo(url, userObject['token'], "https://svgsilh.com/svg/1801287.svg", 0, 0, 1, 1) == ERROR

# Uploading an invalid image
def test_non_existant_img(userObject, url):
    assert photo(url, userObject['token'], "https://google.com/my_image.jpg", 0, 0, 1, 1) == ERROR
    
    assert photo(url, userObject['token'], "https://web.flock.com/?/flock.jpg", 0, 0, 1, 1) == ERROR

# Cropping an image with invalid dimensions
def test_invalid_dimensions(userObject, url):
    # Image Dimensions: 3456 x 2304 pixels

    # Out of range
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 3457, 2305) == ERROR

    # Perfect fit
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 0, 3456, 2304) == SUCCESS

    # x_start > x_end
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 0, 10, 100) == ERROR

    # y_start > y_end
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 0, 100, 100, 10) == ERROR

    # x_start = x_end
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 100, 100, 300) == ERROR

    # empty box
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", 100, 100, 100, 100) == ERROR

    # negative
    assert photo(url, userObject['token'], "https://upload.wikimedia.org/wikipedia/commons/a/a5/Red_Kitten_01.jpg", -1, -2, 100, 200) == ERROR



###### Helper Functions ######

# Retrieves information about a user
def retrieveUser(token, u_id, url):
    params = {'token': token, 'u_id': int(u_id)}
    response = requests.get(url + 'user/profile', params=params)
    return response.json().get('user')

def photo(url_photo, token, image_url, x1, y1, x2, y2):
    payload = {'token': token, 'img_url': image_url, 'x_start': x1, 'y_start': y1, 'x_end': x2, 'y_end': y2}
    response = requests.post(url_photo + "user/profile/uploadphoto", json=payload)
    return response.status_code
