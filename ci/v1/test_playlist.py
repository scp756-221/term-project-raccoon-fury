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
import music


@pytest.fixture
def plserv(request, playlist_url, auth):
    return playlist.Playlist(playlist_url, auth)


@pytest.fixture
def mserv(request, music_url, auth):
    return music.Music(music_url, auth)


@pytest.fixture
def song(request):
    # Recorded 1956
    return ('Elvis Presley', 'Hound Dog')


@pytest.fixture
def song2(request):
    # Recorded 1967
    return ('Aretha Franklin', 'Respect')


def test_health(plserv):
    status_code = plserv.health()
    assert status_code == 200, f"Status code should be 200, got {status_code}"


def test_create_delete(plserv, mserv, song):
    # Create playlist
    trc, m_id = mserv.create(song[0], song[1])
    assert trc == 200
    name = "playlist-test"
    trc, p_id = plserv.create(name, m_id)
    assert trc == 200

    # Read playlist
    trc, playlistName, songs = plserv.read(p_id)
    assert (trc == 200 and playlistName == name and songs == [m_id])

    # Delete objects
    plserv.delete(p_id)
    mserv.delete(m_id)


def test_add_delete_song(plserv, mserv, song, song2):
    # Create playlist
    trc, m_id = mserv.create(song[0], song[1])
    name = "playlist-test"
    trc, p_id = plserv.create(name, m_id)

    # Add song to playlist
    trc, m_id_2 = mserv.create(song2[0], song2[1])
    trc = plserv.add_song(p_id, m_id_2)
    assert trc == 200
    trc, playlistName, songs = plserv.read(p_id)
    assert (trc == 200 and playlistName == name and songs == [m_id, m_id_2])

    # Remove song from playlist
    trc = plserv.delete_song(p_id, m_id)
    assert trc == 200
    trc, playlistName, songs = plserv.read(p_id)
    assert (trc == 200 and playlistName == name and songs == [m_id_2])

    # Delete objects
    plserv.delete(p_id)
    mserv.delete(m_id)
    mserv.delete(m_id_2)
