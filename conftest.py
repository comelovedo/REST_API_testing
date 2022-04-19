from api import PetFriends
from settings import valid_password, valid_email
import pytest

pf = PetFriends()


@pytest.fixture(autouse=True)
def get_key():
    """ We check that the api key request returns status 200 and the result contains the word key"""

    # We send a request and save the received response with the status code in status, and the response text in result
    status, pytest.key = pf.get_api_key(valid_email, valid_password)
    # We compare the received data with our expectations
    assert status == 200
    assert 'key' in pytest.key

    yield

    # Check that the response status = 200 and the pet name matches the given one
    assert pytest.status == 200
