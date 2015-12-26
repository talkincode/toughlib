#!/usr/bin/env python
#coding=utf-8

import yaml

class ConfigDict(dict):

    def __getattr__(self, key):
        try:
            result = self[key]
            if result and isinstance(result, dict):
                result = ConfigDict(result)
            return result
        except KeyError, k:
            raise AttributeError, k

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError, k:
            raise AttributeError, k

    def __repr__(self):
        return '<ConfigDict ' + dict.__repr__(self) + '>'


class Config(ConfigDict):

    def __init__(self, conf_file=None, **kwargs):
        assert(conf_file is not None)
        self.conf_file = conf_file
        with open(self.conf_file) as cf:
            self.update(yaml.load(cf))
        self.update(**kwargs)

    def save(self):
        with open(self.conf_file) as cf:
            yaml.dump(self, cf, default_flow_style=False)

    def __repr__(self):
        return '<Config ' + dict.__repr__(self) + '>'


def find_config(conf_file=None):
    return Config(conf_file)

if __name__ == "__main__":
    cfg = find_config("/tmp/tpconfig")
    print cfg
    print type(cfg.database.aa.a)







