import auth
import pytest

###### Auth Register ######

# EXCEPTIONS #

# Invalid Email
def test_invalid_email():
    clear()
    # Missing @ in email
    with pytest.raises(InputError) as e:
        auth.auth_register("clintbarton.com", "password", "Clint", "Barton")
        
    # Missing domain in email
    with pytest.raises(InputError) as e:
        auth.auth_register("steverodgers@.com", "password", "Steve", "Rodgers")
        
    # Invalid character in email username
    with pytest.raises(InputError) as e:
        auth.auth_register("nata$haromanoff@avengers.com", "password", "Natasha", "Romanoff")
        
    # Missing email username
    with pytest.raises(InputError) as e:
        auth.auth_register("@avengers.com", "password", "Pepper", "Potts")
    
# Duplicate Email
def test_duplicate_email_address():
    clear()
    result = auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    assert(result != None)
    
    # Checking duplicate register
    with pytest.raises(InputError) as e:
        auth.auth_register("tonystark@avengers.com", "password", "Anthony", "Stark")

# Invalid Password
def test_invalid_password():
    clear()
    # Empty password
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "", "Nick", "Fury")
        
    # Under 6 letter password
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "123", "Nick", "Fury")
        
    # Edge case, 5 letter password
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "12345", "Nick", "Fury")

# Invalid First Name
def test_invalid_first_name():
    clear()
    # Empty first name
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "", "Lee")
        
    # First name over 50 characters
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "stanstanstanstanstanstanstanstanstanstanstanstansta", "Lee")

#Invalid Last Name
def test_invalid_last_name():
    clear()
    # Empty last name
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "Stan", "")
    
    # Last name over 50 characters
    with pytest.raises(InputError) as e:
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

    
