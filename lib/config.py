import os
import json
import copy

from dotenv import Dotenv

sentinel = object()

class StoredData:

    ATTRIBUTES = { 'team': [], 'alumni': [] }

    def __init__(self, filename):
        self._attributes = copy.deepcopy(StoredData.ATTRIBUTES)
        self._filename = filename
        self._load()

    def __getattr__(self, attr):
        try:
            return self._attributes[attr]
        except KeyError:
            raise AttributeError("No such attribute " + repr(attr))

    def __setattr__(self, attr, value):
        if attr in StoredData.ATTRIBUTES:
            self._attributes[attr] = value
            self._save()
        elif attr.startswith('_'):
            super().__setattr__(attr, value)
        else:
            raise AttributeError("No such attribute " + repr(attr))

    def _save(self):
        dump_dict = {}

        for attr, val in self._attributes.items():
            dump_dict[attr] = val

        with open(self._filename, 'w') as f:
            json.dump(dump_dict, f, indent=2)

    def _load(self):
        f = None
        try:
            f = open(self._filename)
            data = json.load(f)
        except (FileNotFoundError, ValueError):
            return
        else:
            for key in self._attributes:
                self._attributes[key] = data[key]
        finally:
            if f is not None:
                f.close()


class Config:

    ATTRIBUTES = {
        'filename': str,
        'user_agent': str
    }

    def __init__(self, envfile=None):
        self._envfile_attrs = {}

        if envfile is not None:
            self._envfile_attrs = Dotenv(envfile)

    def get(self, attr, default=sentinel):
        try:
            return getattr(self, attr)
        except ValueError:
            if default != sentinel:
                return default
            else:
                raise

    def __getattr__(self, attr):
        if attr in Config.ATTRIBUTES:
            attr_name = 'STAS_' + attr.upper()
            if attr_name in os.environ:
                value = os.environ[attr_name]
            elif attr_name in self._envfile_attrs:
                value = self._envfile_attrs[attr_name]
            else:
                raise ValueError("Environment variable " + repr(attr_name) + " not set")

            try:
                return Config.ATTRIBUTES[attr](value)
            except ValueError:
                msg = "Cannot coerce {attr} to correct type {type}"
                raise ValueError(msg.format(attr=attr, type=Config.ATTRIBUTES[attr]))
        else:
            raise AttributeError("Unknown attribute " + repr(attr))
