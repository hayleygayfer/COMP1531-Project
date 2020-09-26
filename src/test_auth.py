# test the auth functions

from auth import *

def test_auth_register():
    assert auth_register("test@email.com", "password123", "John", "Doe") == {'u_id': 2, 'token': "test@email.com"}
    assert auth_login("test@email.com", "password123") == {'u_id': 2, 'token': "test@email.com"}
    assert auth_logout("test@email.com") == {'is_success': True}

#def test_auth_login():
#    auth_login("test@email.com", "password123")

#def test_auth_logout():
#    auth_logout("test@email.com")