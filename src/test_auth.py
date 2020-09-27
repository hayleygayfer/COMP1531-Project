import auth
import pytest

###### Auth Register ######

# EXCEPTIONS

def test_invalid_email():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("clintbarton.com", "password", "Clint", "Barton")
    with pytest.raises(InputError) as e:
        auth.auth_register("steverodgers@.com", "password", "Steve", "Rodgers")
    with pytest.raises(InputError) as e:
        auth.auth_register("nata$haromanoff@avengers.com", "password", "Natasha", "Romanoff")
    with pytest.raises(InputError) as e:
        auth.auth_register("@avengers.com", "password", "Pepper", "Potts")
    
def test_duplicate_email_address():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("tonystark@avengers.com", "password", "Anthony", "Stark")

def test_invalid_password():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "", "Nick", "Fury")
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "123", "Nick", "Fury")
    with pytest.raises(InputError) as e:
        auth.auth_register("nickfury@avengers.com", "12345", "Nick", "Fury")

def test_invalid_first_name():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "", "Lee")
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "stanstanstanstanstanstanstanstanstanstanstanstansta", "Lee")

def test_invalid_last_name():
    clear()
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "Stan", "")
    with pytest.raises(InputError) as e:
        auth.auth_register("stanlee@avengers.com", "password", "Stan", "LeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLeeLee")

# VALID CASES

def test_valid_email():
    clear()
    result = auth.auth_register("tonystark@avengers.com", "password", "Tony", "Stark")
    assert(result != None)

def test_alternative_valid_emails():
    clear()
    result = auth.auth_register("bruce_banner@avengers.com", "password", "Bruce", "Banner")
    assert(result != None)
    result = auth.auth_register("thor.odinson@avengers.com", "password", "Thor", "Odinson")
    assert(result != None)
    
def test_valid_passwords():
    clear()
    result = auth.auth_register("nickfury@avengers.com", "123456", "Nick", "Fury")
    assert (result != None)
    result = auth.auth_register("mariahill@avengers.com", "PASSWORD", "Maria", "Hill")
    assert(result != None)
    result = auth.auth_register("happyhogan@avengers.com", "123FOURfive6", "Happy", "Hogan")
    assert(result != None)
    
def test_valid_first_name():
    clear()
    result = auth.auth_register("stanlee@avengers.com", "password", "S", "Lee")
    assert(result != None)
    result = auth.auth_register("scottlang@avengers.com", "password", "ScottScottScottScottScottScottScottScottScottScott", "Lang")
    assert(result != None)
    
def test_valid_last_name():
    clear()
    result = auth.auth_register("peterparker@avengers.com", "password", "Peter", "P")
    assert(result != None)
    result = auth.auth_register("peterquill@avengers.com", "password", "Peter", "QuillQuillQuillQuillQuillQuillQuillQuillQuillQuill")
    assert(result != None)

    
