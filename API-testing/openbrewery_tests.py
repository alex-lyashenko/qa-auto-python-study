import requests
import pytest


class APIClient:
    def __init__(self, base_address):
        self.base_address = base_address

    def get(self, path="/", params=None):
        return requests.get(url=self.base_address + path, params=params)

@pytest.fixture(scope="session")
def api_client():
    base_url = 'https://api.openbrewerydb.org/'
    return APIClient(base_address=base_url)


@pytest.mark.parametrize('per_page', [2, 3, 4])
def test_api_check_per_page_parameter(api_client, per_page):

    result = api_client.get(path="breweries", params={'per_page': per_page}).json()
    assert len(result) == per_page


def test_api_check_fields_list(api_client):

    fields = ['id', 'name', 'brewery_type', 'street', 'address_2', 'address_3', 'city', 'state', 'county_province',
              'postal_code', 'country', 'longitude', 'latitude', 'phone', 'website_url', 'updated_at', 'created_at']
    result = api_client.get(path='breweries', params={'per_page': 1}).json()
    brewery = result[0]
    assert set(brewery.keys()) == set(fields)


@pytest.mark.parametrize('state, expected_state_title', [('new_york', 'New York'), ('colorado', 'Colorado')])
def test_api_check_state_filter(api_client, state, expected_state_title):

    result = api_client.get(path='breweries', params={'by_state': state}).json()
    states = [brewery['state'] for brewery in result]
    assert set(states) == set([expected_state_title])


@pytest.mark.parametrize('query', ['cat', 'dog'])
def test_api_check_search(api_client, query):

    result = api_client.get(path='breweries', params={'by_name': query}).json()
    names = [brewery['name'].lower() for brewery in result]
    matched_names = list(filter(lambda name: query in name, names))
    assert len(names) == len(matched_names)


@pytest.mark.parametrize('brewery_id, expected_status_code', [('madtree-brewing-cincinnati', 200), (200000, 404)])
def test_check_api_status_code(api_client, brewery_id, expected_status_code):

    result = api_client.get(path=f'breweries/{brewery_id}')
    assert result.status_code == expected_status_code