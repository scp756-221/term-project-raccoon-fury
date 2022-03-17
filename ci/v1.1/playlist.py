"""
Python  API for the music service.
"""

# Standard library modules

# Installed packages
import requests


class Playlist():
    """Python API for the playlist service.

    Handles the details of formatting HTTP requests and decoding
    the results.

    Parameters
    ----------
    url: string
        The URL for accessing the music service. Often
        'http://cmpt756s3:30003/'. Note the trailing slash.
    auth: string
        Authorization code to pass to the music service. For many
        implementations, the code is required but its content is
        ignored.
    """

    def __init__(self, url, auth):
        self._url = url
        self._auth = auth

    def health(self):
        """Perform simple health check for testing CI workflow.

        Returns
        -------
        status

        status: number
            The HTTP status code returned by Playlist.
        """
        r = requests.get(
            self._url + 'health',
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def create(self, playlist_name, songs):
        """Create a playlist with a list of m_id."""
        payload = {'PlaylistName': playlist_name,
                   'Songs': songs}
        if type(songs) == list:
            payload['Songs'] = ",".join(songs)
        r = requests.post(
            self._url,
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code, r.json()['playlist_id']

    def read(self, playlist_id):
        """Read a playlist."""
        r = requests.get(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )
        if r.status_code != 200:
            return r.status_code, None, None

        item = r.json()['Items'][0]
        return r.status_code, item['PlaylistName'], item['Songs']

    def add_song(self, playlist_id, music_id):
        """Add a song to playlist."""
        payload = {'music_id': music_id}
        r = requests.post(
            f"{self._url}{playlist_id}/add",
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete_song(self, playlist_id, music_id):
        """Delete a song in playlist."""
        payload = {'music_id': music_id}
        r = requests.post(
            f"{self._url}{playlist_id}/delete",
            json=payload,
            headers={'Authorization': self._auth}
        )
        return r.status_code

    def delete(self, playlist_id):
        """Delete a playlist."""
        requests.delete(
            self._url + playlist_id,
            headers={'Authorization': self._auth}
        )
