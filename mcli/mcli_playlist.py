"""
Simple command-line interface to playlist service
"""

from mcli_base import *


class PlaylistMcli(cmd.Cmd):
    def __init__(self, args):
        self.m_name = args.m_name
        self.m_port = args.m_port
        self.p_name = args.p_name
        self.p_port = args.p_port
        self.svc = args.svc
        cmd.Cmd.__init__(self)
        self.prompt = 'mql-playlist: '

    def do_read(self, arg):
        """
        Read a playlist.

        Parameters
        ----------
        playlist:  playlist_id (optional)
            The playlist_id of the playlist to read. If not specified,
            all playlists are listed.

        Examples
        --------
        read 91246583-ced8-4d70-8f5e-ce81419bb63c
            Return content of the playlist.
        read
            Return all playlists (if the server supports this).

        Notes
        -----
        Some versions of the server do not support listing
        all playlists and will instead return an empty list if
        no parameter is provided.
        """

        url = get_url(self.p_name, self.p_port, self.svc)
        r = requests.get(
            url + arg.strip(),
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
                i['playlist_id'],
                i['PlaylistName'],
                i['Songs']))

    def do_create(self, arg):
        """
        Add a song to the database.

        Parameters
        ----------
        name: string
        songs: string

        Both parameters can be quoted by either single or double quotes.

        Examples
        --------
        create 'My Test Playlist'  "74561cb6-bfc5-431c-8357-8a5b15318f30,d4999ccb-f7f7-41e0-aef0-8f332fad9276"
            Quote the apostrophe with double-quotes.

        create Soundtracks 91246583-ced8-4d70-8f5e-ce81419bb63c
            No quotes needed for single-word artist or title name.
        """
        url = get_url(self.p_name, self.p_port, self.svc)
        args = parse_quoted_strings(arg)
        payload = {
            'PlaylistName': args[0],
            'Songs': ','.join(args[1:])
        }
        r = requests.post(
            url,
            json=payload,
            headers={'Authorization': DEFAULT_AUTH}
        )
        print(r.json())

    def do_delete(self, arg):
        """
        Delete a playlist.

        Parameters
        ----------
        playlist: playlist_id
            The playlist_id of the playlist to delete.

        Examples
        --------
        delete 91246583-ced8-4d70-8f5e-ce81419bb63c
            Delete "My New Playlist".
        """
        url = get_url(self.p_name, self.p_port, self.svc)
        r = requests.delete(
            url + arg.strip(),
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_append(self, arg):
        """
        Add a song to a playlist.

        Parameters
        ----------
        playlist: playlist_id
            The playlist_id of the playlist to update.
        song: music_id
            The song to be appended to the playlist.

        Examples
        --------
        append 91246583-ced8-4d70-8f5e-ce81419bb63c 862a897c-0fa9-4a18-9a5b-77661528dde8
            Add song "(Don’t Fear) The Reaper" to "My New Playlist".
        """
        url = get_url(self.p_name, self.p_port, self.svc)
        args = parse_quoted_strings(arg)
        r = requests.post(
            url + f'{args[0]}/add',
            json={'music_id': args[1]},
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)

    def do_remove(self, arg):
        """
        Remove a song from a playlist.

        Parameters
        ----------
        playlist: playlist_id
            The playlist_id of the playlist to update.
        song: music_id
            The song to be removed from the playlist.

        Examples
        --------
        append 91246583-ced8-4d70-8f5e-ce81419bb63c 862a897c-0fa9-4a18-9a5b-77661528dde8
            Remove song "(Don’t Fear) The Reaper" from "My New Playlist".
        """
        url = get_url(self.p_name, self.p_port, self.svc)
        args = parse_quoted_strings(arg)
        r = requests.post(
            url + f'{args[0]}/delete',
            json={'music_id': args[1]},
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
        Run a test stub on the playlist server.
        """
        url = get_url(self.p_name, self.p_port, self.svc)
        r = requests.get(
            url + 'test',
            headers={'Authorization': DEFAULT_AUTH}
        )
        if r.status_code != 200:
            print("Non-successful status code:", r.status_code)
