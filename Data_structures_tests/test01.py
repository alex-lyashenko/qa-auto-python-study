import pytest


@pytest.fixture
def get_data_types(request):
    print(f"\nGetting data types by {request.node}")
    return {
        'list': [1, 2, 3, 4],
        'tuple': (1, 2, 3, 4),
        'set': {1, 2, 3},
        'dict': {'first_name': 'John', 'last_name': 'Doe'},
        'str': 'Test String',
        'int': 22,
    }


@pytest.fixture(scope='module')
def module_fixture(request):
    print(f"{request.scope} fixture output - start\n-----")

    def module_finalizer():
        print(f"\n-----\n{request.scope} fixture output - finish")

    request.addfinalizer(module_finalizer)


@pytest.fixture(scope='session')
def session_fixture(request):
    print(f"{request.scope} fixture output - start\n-----")

    def session_finalizer():
        print(f"\n-----\n{request.scope} fixture output - finish")

    request.addfinalizer(session_finalizer)


def test_list_length(session_fixture, module_fixture, get_data_types):

    assert len(get_data_types['list']) == 4


def test_tuple_value(session_fixture, module_fixture, get_data_types):

    assert get_data_types['tuple'][0] == 1


def test_sum_list_values(session_fixture, module_fixture, get_data_types):

    assert sum(get_data_types['list']) == 10


def test_dict_name_check(session_fixture, module_fixture, get_data_types):

    assert 'John' == get_data_types['dict']['first_name']


def test_dict_items_len(session_fixture, module_fixture, get_data_types):

    assert len(get_data_types['dict'].values()) >= 2


def test_dict_check_fullname(session_fixture, module_fixture, get_data_types):

    fullname = '{first_name} {last_name}'.format(**get_data_types['dict'])
    assert fullname == 'John Doe'


def test_str_check_word(session_fixture, module_fixture, get_data_types):

    assert 'Test' in get_data_types['str']


def test_is_integer_even(session_fixture, module_fixture, get_data_types):

    assert get_data_types['int'] % 2 == 0


def test_check_set_difference(session_fixture, module_fixture, get_data_types):

    assert len(get_data_types['set'].difference({2, 3})) > 0


def test_check_set_intersection(session_fixture, module_fixture, get_data_types):

    assert len(get_data_types['set'].intersection({2, 3})) == 2