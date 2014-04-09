#!/usr/bin/python

import os

class ConnectorConfig(object):
    def __init__(self, CompCode):
        self.CompCode = CompCode
        self.user = None
        self.url = None
        self.domain = None
        self.password = None
        missing = set(('url', 'user', 'domain'))
        with open(os.path.join(os.path.expanduser("~/genav_config"), CompCode)) as f:
            for line in f:
                if line.startswith('#'):
                    continue
                if line.endswith("\n"):
                    line = line[:-1]
                if line.endswith("\r"):
                    line = line[:-1]
                directive, argument = line.split(None, 1)
                if directive == 'user':
                    self.user = argument
                elif directive == 'url':
                    self.url = argument
                elif directive == 'domain':
                    self.domain = argument
                else:
                    raise ValueError("Unknown directive %s in config file" % (directive,))
                if directive in missing:
                    missing.remove(directive)
        if missing:
            raise ValueError("Missing directives in config file: %r" % (missing,))
        with open(os.path.join(os.path.expanduser("~/.genav_password"), CompCode)) as f:
            for line in f:
                if line.endswith("\n"):
                    line = line[:-1]
                if line.endswith("\r"):
                    line = line[:-1]
                self.password = line
                break
        if self.password is None:
            raise ValueError("Missing Wi-Flight API password")
