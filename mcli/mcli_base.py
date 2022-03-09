"""
Shared utilities
"""

# Standard library modules
import argparse
import cmd
import re

# Installed packages
import requests

# The services check only that we pass an authorization,
# not whether it's valid
DEFAULT_AUTH = 'Bearer A'


def get_url(name, port, svc):
    return "http://{}:{}/api/v1/{}/".format(name, port, svc)


def parse_args():
    argp = argparse.ArgumentParser(
        'mcli',
        description='Command-line query interface to music service'
    )
    argp.add_argument(
        'name',
        help="DNS name or IP address of music server"
    )
    argp.add_argument(
        'port',
        type=int,
        help="Port number of music server"
    )
    return argp.parse_args()


def parse_quoted_strings(arg):
    """
    Parse a line that includes words and '-, and "-quoted strings.
    This is a simple parser that can be easily thrown off by odd
    arguments, such as entries with mismatched quotes.  It's good
    enough for simple use, parsing "-quoted names with apostrophes.
    """
    mre = re.compile(r'''(\w+)|'([^']*)'|"([^"]*)"''')
    args = mre.findall(arg)
    return [''.join(a) for a in args]
