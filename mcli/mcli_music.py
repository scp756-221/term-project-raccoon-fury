"""
Simple command-line interface to music service
"""

from mcli_base import *


class MusicMcli(cmd.Cmd):
    def __init__(self, args):
        self.m_name = args.m_name
        self.m_port = args.m_port
        self.p_name = args.p_name
        self.p_port = args.p_port
        self.svc = args.svc
        cmd.Cmd.__init__(self)
        self.prompt = 'mql-music: '

    def do_read(self, arg):
        """
        Read a single song or list all songs.

        Parameters
        ----------
        song:  music_id (optional)
            The music_id of the song to read. If not specified,
            all songs are listed.

        Examples
        --------
        read 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Return "The Last Great American Dynasty".
        read
            Return all songs (if the server supports this).

        Notes
        -----
        Some versions of the server do not support listing
        all songs and will instead return an empty list if
        no parameter is provided.
        """

        url = get_url(self.m_name, self.m_port, self.svc)
        r = requests.get(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
        items = r.json()
        if 'Count' not in items:
            print("0 items returned")
            return
        print("{} items returned".format(items['Count']))
        for i in items['Items']:
            print("{}  {:20.20s} {}".format(
                i['music_id'],
                i['Artist'],
                i['SongTitle']))

    def do_create(self, arg):
        """
        Add a song to the database.

        Parameters
        ----------
        artist: string
        title: string

        Both parameters can be quoted by either single or double quotes.

        Examples
        --------
        create 'Steely Dan'  "Everyone's Gone to the Movies"
            Quote the apostrophe with double-quotes.

        create Chumbawamba Tubthumping
            No quotes needed for single-word artist or title name.
        """
        url = get_url(self.m_name, self.m_port, self.svc)
        args = parse_quoted_strings(arg)
        payload = {
            'Artist': args[0],
            'SongTitle': args[1]
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        print(r.json())

    def do_delete(self, arg):
        """
        Delete a song.

        Parameters
        ----------
        song: music_id
            The music_id of the song to delete.

        Examples
        --------
        delete 6ecfafd0-8a35-4af6-a9e2-cbd79b3abeea
            Delete "The Last Great American Dynasty".
        """
        url = get_url(self.m_name, self.m_port, self.svc)
        r = requests.delete(
            url+arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True

    def do_test(self, arg):
        """
        Run a test stub on the music server.
        """
        url = get_url(self.m_name, self.m_port, self.svc)
        r = requests.get(
            url+'test',
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_shutdown(self, arg):
        """
        Tell the music cerver to shut down.
        """
        url = get_url(self.m_name, self.m_port, self.svc)
        r = requests.get(
            url+'shutdown',
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
