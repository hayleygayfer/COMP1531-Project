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

IMG_LEN = 10

def user_profile(token, u_id):

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
    # find user
    try:
        u_it = find_user(token)
    except StopIteration:
        raise AccessError("User not found")

    # check if image is jpg
    ext = img_url.rsplit('.', 1)[-1]
    allowed_ext = ['JPG', 'JPEG']
    if ext.upper() not in allowed_ext:
        print(ext)
        raise InputError("Image must be of type JPG")
    
    # Check if valid image
    try:
        img = Image.open(urllib.request.urlopen(img_url))
    except:
        raise InputError("Image not found")

    width, height = img.size

    # Check if dimensions are valid
    if not valid_dimensions(x_start, x_end, width):
        print(x_start, x_end, width, 0 <= x_start, x_start < x_end, x_end <= width)
        raise InputError("x dimensions are not valid")
    if not valid_dimensions(y_start, y_end, height):
        raise InputError("y dimensions are not valid")

    # Crop image
    img = img.crop((x_start, y_start, x_end, y_end))
    
    # Create 'static/' is it doesn't already exist
    try:
        os.mkdir('static')
    except FileExistsError:
        pass

    # Generate a 10 char filename and use this to locate the save location for the jpg
    filename = generate_img_filename()
    p = pathlib.Path('static/' + filename)
    img.save(p)

    # Modify the 'profile_img_url' key in users with its address
    data['users'][u_it]['profile_img_url'] = os.path.join(request.host_url, p)

    return {}



def validate_handle_str(handle_str):
    return 3 < len(handle_str) < 20
        
def find_match(parameter, match):
    return list(filter(lambda user: user[parameter] == match, data['users']))

def find_user(token):
    return next(i for i, user in enumerate(data['users']) if user['token'] == token)

def valid_dimensions(start, end, max):
    return 0 <= start < end <= max

def generate_img_filename():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=IMG_LEN)) + '.jpg'

'''
def generate_url(url, x1, x2, y1, y2):
    # TODO: modify return

    For outputs with data pertaining to a user, a profile_img_url is present. When images are uploaded for a user profile,
    after processing them you should store them on the server such that your server now locally has a copy of the cropped 
    image of the original file linked. Then, the profile_img_url should be a URL to the server, such as
    http://localhost:5001/imgurl/adfnajnerkn23k4234.jpg (a unique url you generate).


    return "https://gitlab.cse.unsw.edu.au/uploads/-/system/appearance/header_logo/1/unsw_logo_2016.jpg"
'''
