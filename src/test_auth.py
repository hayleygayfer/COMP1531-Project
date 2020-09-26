# test the auth functions

from auth import *

def test_auth_register():
    auth_register("test@email.com", "password123", "John", "Doe")

def test_auth_login():
    auth_login("test@email.com", "password123")

def test_auth_logout():
    auth_logout("test@email.com")