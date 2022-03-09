"""
Simple command-line interface to all services
"""

# Submodules
from mcli_base import *
from mcli_music import *


class Mcli(cmd.Cmd):
    def __init__(self, args):
        self.name = args.name
        self.port = args.port
        cmd.Cmd.__init__(self)
        self.prompt = 'mql: '
        self.intro = """
Command-line interface to music service.
Enter 'help' for command list.
'Tab' character autocompletes commands.
"""

    def dispatch(self, sub_cmd, arg):
        args = parse_quoted_strings(arg)
        if len(args) > 0:
            sub_cmd.onecmd(arg)
        else:
            sub_cmd.cmdloop()

    def do_music(self, arg):
        """
        Proceed with the music service.
        """
        self.svc = 'music'
        sub_cmd = MusicMcli(self)
        self.dispatch(sub_cmd, arg)
        return

    def do_user(self, arg):
        """
        Proceed with the user service.
        """
        self.svc = 'user'
        # TODO
        return

    def do_playlist(self, arg):
        """
        Proceed with the playlist service.
        """
        self.svc = 'playlist'
        # TODO
        return

    def do_quit(self, arg):
        """
        Quit the program.
        """
        return True


if __name__ == '__main__':
    args = parse_args()
    Mcli(args).cmdloop()
