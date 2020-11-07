from data import data
from error import InputError, AccessError
from auth import validate_first_name, validate_last_name, validate_email

import urllib
from PIL import Image # pip3 install Pillow
import pathlib
from flask import request
import os

import random
import string

IMG_FILENAME_LEN = 10
FILE_EXTENSIONS = ['JPG', 'JPEG']

def user_profile(token, u_id):
    '''
    Displays details about a certain user to the authenticated user

    Args:
        1. token (str): the token of the authenticated user who is viewing someone's profile
        2. u_id (int): identify the user who's details are being accessed

    Return:
        A dictionary containing details about the user including their,
        - email
        - name
        - handle

    An AccessError or InputError is raised when there are errors in the function call

    '''

    user_id = find_match('u_id', u_id)

    if user_id == []:
        raise InputError("Not a valid user")

    try:
        find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")

    return {
        'user': user_id[0]
    }

def user_profile_setname(token, name_first, name_last):
    '''
    Updates the authenticated user's first and last names with the given inputs

    Args:
        1. token (str): the token of the authenticated user who is changing their name
        2. name_first (str): The new first name
        3. name_last (str): The new surname

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_first_name(name_first) == False:
        raise InputError("Not a valid first name")

    if validate_last_name(name_last) == False:
        raise InputError("Not a valid last name")

    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")

    data['users'][u_it]['name_first'] = name_first
    data['users'][u_it]['name_last'] = name_last

    return { 
    }

def user_profile_setemail(token, email):
    '''
    Updates the authenticated user's email with the given input

    Args:
        1. token (str): the token of the authenticated user who is changing their name
        2. email (str): The updated emails

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    if validate_email(email) == False:
        raise InputError("Not a valid email")

    if find_match('email', email) != []:
        raise InputError("Email already in use")
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")
 
    data['users'][u_it]['email'] = email

    return {
    }

def user_profile_sethandle(token, handle_str):
    '''
    Updates the authenticated user's display handle with the given input

    Args:
        1. token (str): the token of the authenticated user who is changing their name
        2. handle_str (str): The updated handle

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''
    
    if validate_handle_str(handle_str) == False:
        raise InputError("Not a valid handle")

    if find_match('handle_str', handle_str) != []:
        raise InputError("handle already in use")
        
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("Not a valid token")

    data['users'][u_it]['handle_str'] = handle_str

    return {
    }

## ITERATION 3

def user_profile_uploadphoto(token, img_url, x_start, y_start, x_end, y_end):
    '''
    Update/Set a profile picture for the authenticated user.
    The profile picture must be from a web url and must be a jpg/jpeg file
    The image is cropped using the input x and y coordinates.
    The coordinates must be in range of the image dimensions.

    Args:
        1. token (str): the token of the authenticated user who is uploading a new profile picture
        2. img_url (str): The url of the uploaded image (before cropping)
        3. x_start (int): The x-coordinate for the top-left pixel of the new image
        4. y_start (int): The y-coordinate for the top-left pixel of the new image
        5. x_end (int): The x-coordinate for the bottom-right pixel of the new image
        6. y_end (int): The y-coordinate for the bottom-right pixel of the new image

    Return:
        An empty dictionary to indicate that the function call was successful

    An AccessError or InputError is raised when there are errors in the function call

    '''

    # find user
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("User not found")

    # check if image is jpg
    extension = img_url.rsplit('.', 1)[-1]
    if extension.upper() not in FILE_EXTENSIONS:
        raise InputError("Image must be of type JPG")
    
    # Check if valid image
    try:
        img = Image.open(urllib.request.urlopen(img_url))
    except:
        raise InputError("Image not found")

    # Check if dimensions are valid
    width, height = img.size
    if not valid_dimensions(x_start, x_end, width):
        raise InputError(f"X dimensions must be between 0 and {width}, inclusive")
    if not valid_dimensions(y_start, y_end, height):
        raise InputError(f"Y dimensions must be between 0 and {height}, inclusive")

    # Crop image
    img = img.crop((x_start, y_start, x_end, y_end))
    
    # Create 'static/' if it doesn't already exist (inside src -> project/src/static/)

    # Get the absolute path so that static is the same folder regardless of which
    # directory the script is run in
    path_script = pathlib.Path(__file__).parent.absolute()
    path_static = os.path.join(path_script, 'static')
    try:
        os.mkdir(path_static)
    except FileExistsError:
        pass

    # Generate a 10 char filename and use this to locate the save location for the jpg
    filename = generate_img_filename()
    p = os.path.join(path_static, filename)

    # Save the image
    img.save(p)

    # Modify the 'profile_img_url' key in users with its address
    data['users'][u_it]['profile_img_url'] = request.host_url + 'static/' + filename

    return {}

####################################################################

def validate_handle_str(handle_str):
    return 3 < len(handle_str) < 20
        
def find_match(parameter, match):
    return list(filter(lambda user: user[parameter] == match, data['users']))

def find_user(token):
    return next(i for i, user in enumerate(data['users']) if user['token'] == token)

def valid_dimensions(start, end, max):
    return 0 <= start < end <= max

# Generates a 10 digit string with integers and uppercase characters
# Does not need to check if the image already exists, since the probability is extremely low (num_images/36^10)
def generate_img_filename():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=IMG_FILENAME_LEN)) + '.jpg'


