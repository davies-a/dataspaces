import base64
import json
import os

import pytest

from dspace.config import ConfigStore


def test_load_from_file():
    ConfigStore._config_file = "test/mocks/mock_valid_config.json"
    config = ConfigStore.load_from_file()
    assert config.default_user == "test"


def test_load_from_missing_file():
    ConfigStore._config_file = "test/mocks/nonexistent.json"
    with pytest.raises(Exception):
        ConfigStore.load_from_file()


def test_save_file():
    ConfigStore._config_file = "test/mocks/_test_config_save.json"

    ConfigStore(default_password="test", default_user="test").save()

    with open(ConfigStore._config_file, "r") as f:
        contents = json.load(f)
        assert contents["default_user"] == "test"
        assert base64.decodebytes(contents["default_password"].encode()) == b"test"

    os.remove(ConfigStore._config_file)
