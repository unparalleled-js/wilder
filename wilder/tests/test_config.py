from wilder.config import create_config_object
from wilder.config import delete_config_if_exists
from wilder.config import set_client_settings
from wilder.config import WildConfig
from wilder.constants import Constants
from wilder.testutil import ignore_user_project_files

TEST_HOST = "example.com"
TEST_PORT = 8888
TEST_CLIENT_SETTINGS = {
    Constants.HOST: TEST_HOST,
    Constants.PORT: TEST_PORT,
    Constants.IS_ENABLED: True,
}
TEST_SETTINGS = {Constants.CLIENT: TEST_CLIENT_SETTINGS}


def get_test_config():
    """PLEASE use `ignore_use_config()` decor if using this method."""
    return set_client_settings(TEST_CLIENT_SETTINGS)


@ignore_user_project_files
def test_set_client_settings_when_first_time_sets():
    config = get_test_config()
    assert config.host == TEST_HOST
    assert config.port == TEST_PORT
    assert config.is_enabled


@ignore_user_project_files
def test_set_client_settings_when_first_time_but_told_to_disable_sets_and_disables():
    settings = dict(TEST_CLIENT_SETTINGS)
    settings[Constants.IS_ENABLED] = False
    set_client_settings(settings)
    config = create_config_object()
    assert config.host == TEST_HOST
    assert config.port == TEST_PORT
    assert not config.is_enabled


@ignore_user_project_files
def test_set_client_settings_when_already_exists_replaces_values():
    get_test_config()
    new_host = "host2"
    new_port = 123
    new_settings = {Constants.HOST: new_host, Constants.PORT: new_port}
    set_client_settings(new_settings)
    config = create_config_object()
    assert config.host == new_host
    assert config.port == new_port


@ignore_user_project_files
def test_delete_config_if_exists_deletes_saved_host_and_port():
    config = get_test_config()
    assert config.host == TEST_HOST
    assert config.port == TEST_PORT
    delete_config_if_exists()
    config = create_config_object()
    assert config.host is None
    assert config.port is None


class TestWildClientConfig:
    def test_init_sets_expected_properties(self):
        config = WildConfig(TEST_SETTINGS)
        assert config.host == TEST_HOST
        assert config.port == TEST_PORT

    def test_is_using_config_when_host_exists_returns_true(self):
        config = WildConfig(TEST_SETTINGS)
        assert config.is_using_config()

    def test_is_using_config_when_host_does_not_exist_returns_false(self):
        new_settings = dict(TEST_SETTINGS)
        new_settings[Constants.CLIENT][Constants.HOST] = None
        config = WildConfig(new_settings)
        assert not config.is_using_config()

    def test_is_using_config_when_host_is_empty_str_does_returns_false(self):
        new_settings = dict(TEST_SETTINGS)
        new_settings[Constants.CLIENT][Constants.HOST] = ""
        config = WildConfig(new_settings)
        assert not config.is_using_config()

    def test_is_using_config_when_host_is_number_returns_false(self):
        new_settings = dict(TEST_SETTINGS)
        new_settings[Constants.CLIENT][Constants.HOST] = 5000
        config = WildConfig(new_settings)
        assert not config.is_using_config()

    def test_json_returns_expected_json(self):
        config = WildConfig(TEST_SETTINGS)
        actual = config.json
        expected = TEST_SETTINGS
        assert actual == expected

    def test_set_host(self):
        config = WildConfig(TEST_SETTINGS)
        test_host = "what.new.host.example.com"
        config.host = test_host
        assert config.host == test_host

    def test_set_host_when_given_none_does_not_set(self):
        config = WildConfig(TEST_SETTINGS)
        config.host = None
        assert config.host is not None

    def test_set_port_when_given_number_sets(self):
        config = WildConfig(TEST_SETTINGS)
        test_port = 5050
        config.port = test_port
        assert config.port == test_port

    def test_set_port_when_given_numeric_string_sets_to_number(self):
        config = WildConfig(TEST_SETTINGS)
        test_port = 5050
        config.port = str(test_port)
        assert config.port == test_port

    def test_set_port_when_given_non_numeric_does_not_set(self):
        config = WildConfig(TEST_SETTINGS)
        bad_port = "5050q23fwdsv"
        config.port = bad_port
        assert config.port != bad_port

    def test_set_port_when_given_none_does_not_set(self):
        config = WildConfig(TEST_SETTINGS)
        config.port = None
        assert config.port is not None

    def test_set_is_enabled_when_given_bool_sets(self):
        config = WildConfig(TEST_SETTINGS)
        config.is_enabled = False
        assert not config.is_enabled
        config.is_enabled = True
        assert config.is_enabled

    def test_set_is_enabled_when_given_bool_strs_sets(self):
        config = WildConfig(TEST_SETTINGS)
        config.is_enabled = "False"
        assert not config.is_enabled
        config.is_enabled = "True"
        assert config.is_enabled

    def test_set_is_enabled_when_given_none_does_not_set(self):
        config = WildConfig(TEST_SETTINGS)
        config.is_enabled = None
        assert config.is_enabled is not None
