import auth
import channel
import channels
import pytest

from error import InputError, AccessError
from data import data
from other import clear

### channels_list ###

# VALID CASES #
def test_no_channels():
    clear()
    pass

def test_user_in_no_channels():
    clear()
    pass

def test_user_is_in_all_channels():
    clear()
    pass

def test_user_is_in_some_channels():
    clear()
    pass

### channels_listall ###

# VALID CASES #
def test_no_total_channels():
    clear()
    pass

def test_total_channels():
    clear()
    pass

### channels_create ###

# EXCEPTIONS #
def test_name_over_20_characters():
    clear()
    pass

# VALID CASES #
def test_public():
    clear()
    pass

def test_private():
    clear()
    pass