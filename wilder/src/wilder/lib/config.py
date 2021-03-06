import json
import os

from wilder.lib.constants import Constants
from wilder.lib.user import get_config_path
from wilder.lib.util.conversion import to_bool
from wilder.lib.util.conversion import to_int
from wilder.lib.util.sh import load_json_from_file
from wilder.lib.util.sh import wopen


def set_client_settings(client_config_json):
    config_path = get_config_path()
    current_config_json = get_config_json()
    _config = create_config_object(current_config_json)

    new_host = client_config_json.get(Constants.HOST)
    new_port = client_config_json.get(Constants.PORT)
    new_is_enabled = client_config_json.get(Constants.IS_ENABLED)

    # If setting for first time and not given is_enabled, set to True
    no_host_currently_set = not _config.host
    init_is_enabled_set = new_is_enabled is not None
    if no_host_currently_set and not init_is_enabled_set:
        new_is_enabled = True

    _config.host = new_host
    _config.port = new_port
    _config.is_enabled = new_is_enabled
    json_to_save = _config.json
    _save_config_change(config_path, json_to_save)
    return _config


def _save_config_change(config_path, config_json):
    if os.path.exists(config_path):
        os.remove(config_path)
    with wopen(config_path, "w") as config_file:
        config_file.write(json.dumps(config_json, indent=2))


def get_config_json():
    config_path = get_config_path(create_if_not_exists=True)
    return load_json_from_file(config_path)


def _create_init_config_json():
    return {Constants.CLIENT: {Constants.HOST: None, Constants.PORT: None}}


def create_config_object(config_json=None):
    config_json = config_json or get_config_json()
    return WildConfig(config_json)


def delete_config_if_exists():
    config_path = get_config_path()
    if os.path.exists(config_path):
        os.remove(config_path)


def using_config():
    config = create_config_object()
    return config.is_using_config()


class WildConfig:
    def __init__(self, config_json):
        self.json = config_json

    def is_using_config(self):
        return self.host is not None and self.host != "" and isinstance(self.host, str)

    @property
    def client_settings(self):
        return self.json.get(Constants.CLIENT)

    @property
    def host(self):
        return self.client_settings.get(Constants.HOST)

    @host.setter
    def host(self, host):
        if host:
            self.client_settings[Constants.HOST] = host

    @property
    def port(self):
        return self.client_settings.get(Constants.PORT)

    @port.setter
    def port(self, port):
        port = to_int(port)
        if port:
            self.client_settings[Constants.PORT] = port

    @property
    def is_enabled(self):
        return self.client_settings.get(Constants.IS_ENABLED)

    @is_enabled.setter
    def is_enabled(self, is_enabled):
        val = to_bool(is_enabled)
        if val is not None:
            self.client_settings[Constants.IS_ENABLED] = val
