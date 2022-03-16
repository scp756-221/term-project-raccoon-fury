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
