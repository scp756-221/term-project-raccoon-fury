"""
Simple command-line interface to music service
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


def parse_args():
    argp = argparse.ArgumentParser(
        's3',
        description='Test s3 connection'
        )
    argp.add_argument(
        'name',
        help="DNS name or IP address"
        )
    argp.add_argument(
        'port',
        type=int,
        help="Port number"
        )
    return argp.parse_args()

def get_url(name, port):
    return "http://{}:{}/api/v1/playlist/".format(name, port)

if __name__ == '__main__':
    args = parse_args()
    url = get_url(args.name, args.port)
    r = requests.get(url+'health',
        headers={'Authorization': DEFAULT_AUTH}
    )
    if r.status_code != 200:
        print("Non-successful status code:", r.status_code)
    else:
        print("Successful status code:", r.status_code)
