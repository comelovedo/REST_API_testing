from api import PetFriends
from settings import valid_password, valid_email, invalid_email, invalid_age, invalid_name
import os

pf = PetFriends()


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result


def test_get_api_key_for_invalid_user(email=invalid_email, password=valid_password):
    """" Check that a key request for a non-existent user does not return status 200"""

    # We send a request and save the received response with the status code in status
    status = pf.get_api_key(email, password)
    assert status != 403


def test_get_all_pets_with_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0


def test_add_new_pet_with_valid_data(name='Барбоскин', animal_type='двортерьер',
                                     age='4', pet_photo='images/cat_1.jpeg'):
    """Checking that you can add a pet with correct data"""

    # Get the full path of the pet image and save it to the variable pet photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Requested api key and save to auth_key variable
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # We compare the received answer with the expected result
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_name(name=invalid_name, animal_type='двортерьер',
                                       age='4', pet_photo='images/cat_1.jpeg'):
    """Checking that you can add a pet with an invalid name"""

    # Get the full path of the pet image and save it to the variable pet photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # We request the api key and save it to the auth_key variable
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # We compare the received answer with the expected result
    assert status == 200
    assert result['name'] == name


def test_add_new_pet_with_invalid_age(name=invalid_name, animal_type='двортерьер',
                                      age=invalid_age, pet_photo='images/cat_1.jpeg'):
    """Checking that you can add a pet with an invalid name"""

    # Get the full path of the pet image and save it to the variable pet photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # We request the api key and save it to the auth_key variable
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Adding a pet
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # We compare the received answer with the expected result
    assert status == 200
    assert result['name'] == name


def test_add_information_about_pet_without_photo(name='Пингвинятина', animal_type='Млекосос', age='54'):
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    status, result = pf.add_information_about_new_pet_without_photo(auth_key, name, animal_type, age)
    assert status == 200


def test_add_photo_for_pet(pet_photo='images/1877085.jpeg'):
    # Get the full path of the pet image and save it to the pet_photo variable
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # We request the api key and save it to the auth_key variable and request a list of our pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Adding a photo
    pet_id = my_pets['pets'][1]['id']
    status, result = pf.add_photo_of_pet(auth_key, pet_id, pet_photo)
    # We compare the received answer with the expected result

    assert status == 200


def test_successful_delete_self_pet():
    """Checking the possibility of deleting a pet"""

    # We get the auth_key and request a list of our pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Check - if the list of your pets is not empty, Take the id of the first pet
    # from the list and send a deletion request and again request a list of our pets
    assert len(my_pets['pets']) > 0
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # We take the id of the first pet from the list and send a deletion request

    # Once again we ask for a list of our pets
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Check that the response status is 200 and there is no id of the deleted pet in the list of pets
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_pet_info_negative_age(name='Мурзик', animal_type='Котэ', age=-5):
    """Check the possibility of updating information about a pet with a negative age value"""

    # We get the auth_key key and a list of our pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # If the list is not empty, then we try to update its name, type and age
    assert len(my_pets['pets']) > 0
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Check that the response status = 200 and the pet name matches the given one
    assert status == 200
    assert result['name'] == name


def test_successful_update_self_pet_info(name='Мурзик', animal_type='Котэ', age=5):
    """Checking the possibility of updating information about the pet"""

    # We get the auth_key key and a list of our pets
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # If the list is not empty, then we try to update its name, type and age
    assert len(my_pets['pets']) > 0, "There is no my pets"
    status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Check that the response status = 200 and the pet name matches the given one
    assert status == 200
    assert result['name'] == name
