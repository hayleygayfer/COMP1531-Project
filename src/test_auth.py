import auth
import pytest

###### Auth Register ######

# VALID CASES

def test_valid_email():
    result = auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    assert(result != None)

def test_alternative_valid_emails():
    result = auth.auth_register("bruce_banner@avengers.com", "password", "Bruce", "Banner")
    assert(result != None)
    result = auth.auth_register("thor.odinson@avengers.com", "password", "Thor", "Odinson")
    assert(result != None)

# EXCEPTIONS

def test_invalid_email():
    with pytest.raises(InputError) as e:
        auth.auth_register("clintbarton.com", "password", "Clint", "Barton")
    with pytest.raises(InputError) as e:
        auth.auth_register("steverodgers@.com", "password", "Steve", "Rodgers")
    with pytest.raises(InputError) as e:
        auth.auth_register("nata$haromanoff@avengers.com", "password", "Natasha", "Romanoff")
    with pytest.raises(InputError) as e:
        auth.auth_register("@avengers.com", "password", "Pepper", "Potts")
    
def test_duplicate_email_address():
    with pytest.raises(InputError) as e:
        result = auth.auth_register("tonystark@avengers.com", "password", "Anthony", "Stark")

def test_invalid_password():
    
    
