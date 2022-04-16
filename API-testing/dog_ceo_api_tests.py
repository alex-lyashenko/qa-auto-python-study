import requests
import pytest


class APIClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="/", params=None):
        return requests.get(url=self.base_address + path, params=params)

@pytest.fixture(scope="session")
def api_client():
    base_url = 'https://dog.ceo/'
    return APIClient(base_address=base_url)


@pytest.mark.parametrize('number', [2, 3, 4])
def test_api_check_number_of_messages(api_client, number):

    result = api_client.get(path="api/breed/hound/images/random/" + str(number)).json()
    assert len(result['message']) == number


@pytest.mark.parametrize("input_data, expected_type", [(None, str), (2, list)])
def test_api_check_type_of_message(api_client, input_data, expected_type):

    path = 'api/breed/hound/images/random/'
    if isinstance(input_data, int):
        path += str(input_data)
    result = api_client.get(path=path).json()
    assert isinstance(result['message'], expected_type)


def test_api_check_breed_list(api_client):

    result = api_client.get(path='api/breeds/list/all').json()
    assert result['status'] == 'success'


@pytest.mark.parametrize("breed, expected_status", [('hound', 'success'), ('hound2', 'error')])
def test_api_check_breed(api_client, breed, expected_status):

    result = api_client.get(path='api/breed/{}/images'.format(breed)).json()
    assert result['status'] == expected_status


@pytest.mark.parametrize("breed, sub_bread_exists", [('hound', True), ('bulldog', True), ('chihuahua', False)])
def test_api_check_sub_breed(api_client, breed, sub_bread_exists):

    result = api_client.get(path='api/breeds/list/all'.format(breed)).json()
    assert bool(result['message'][breed]) == sub_bread_exists