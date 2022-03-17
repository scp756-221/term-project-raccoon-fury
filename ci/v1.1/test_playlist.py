"""
Test the *_original_artist routines.

These tests are invoked by running `pytest` with the
appropriate options and environment variables, as
defined in `conftest.py`.
"""

# Standard libraries

# Installed packages
import pytest

# Local modules
import playlist


@pytest.fixture
def plserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


def test_health(plserv):
    status_code = plserv.health()
    assert status_code == 200, f"Status code should be 200, got {status_code}"
