import base64
import getpass
import json
import os
from pathlib import Path

from pydantic import BaseModel, SecretStr


def b64_secret(value):
    return base64.encodebytes(value.get_secret_value().encode())


class ConfigStore(BaseModel):
    default_password: SecretStr
    default_user: str

    _config_folder = os.path.join(Path.home(), ".dataspaces")
    _config_file = os.path.join(_config_folder, "config.json")

    class Config:
        json_encoders = {
            SecretStr: lambda v: b64_secret(v) if v else None,
        }

    @classmethod
    def load_from_file(cls):
        secret_fields = [
            field_name
            for field_name, field in cls.__fields__.items()
            if field.type_ == SecretStr
        ]

        _tmp = json.load(open(cls._config_file, "rb"))

        for field in secret_fields:
            if field in _tmp:
                _tmp[field] = base64.decodebytes(_tmp[field].encode()).decode()

        return cls(**_tmp)

    def save(self):
        if not os.path.exists(self._config_folder):
            os.mkdir(self._config_folder)

        with open(self._config_file, "w") as f:
            f.write(self.json())

    @classmethod
    def get_or_create(cls):
        try:
            return cls.load_from_file()
        except Exception:
            print(
                "No config has been registered yet. Please answer a few questions so we may create some."
            )
            _user = input("Please provide a default database user for dspaces.")
            _pass = getpass.getpass(
                "Please provide a default password to be used for dataspaces."
                "Note: this will not be secured; so do not reuse one."
            )

            store = cls(default_user=_user, default_password=_pass)
            store.save()
            return cls.load_from_file()
