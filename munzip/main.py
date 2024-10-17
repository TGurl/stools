#!/usr/bin/env python3
from utils import TGutils
import sys
import os


class MUnzip(TGutils):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.app_name = 'munzip'
        self.title = '%yMUnzip v0.01a%R%F - %gTransgirl 2024%R'
        self.keep_archive = False

    def show_help(self, error=''):
        fmt = "    {:<12} {}"
        self.header(self.title, clear=True, nl=True)
        if error:
            self.printf(f"ERROR:")
            self.printf(f'    {error}', nl=True)
        self.printf('Usage:')
        self.printf(f'    {self.app_name} [options] <zip-file>', nl=True)
        self.printf('Options:')

        options = [
            {'opt': '-k', 'ex': 'Keep zip-file when done'},
        ]

        for option in options:
            self.fprint(option['opt'], option['ex'], fmt=fmt)
        

    def remove_options(self, args, remove):
        for r in remove:
            if r in args:
                idx = args.index(r)
                args.pop(idx)
        return args

    def jack_the_unzipper(self, archive):
        self.header(self.title)
        self.printf(f"> Unzipping {archive}")

    def main(self, args):
        self.app_name = args[0]
        args.pop(0)

        # ---- parse the argumetns
        if '-k' in args or '-K' in args:
            self.keep_archive = True
            args = self.remove_options(args, ['-k', '-K'])

        # ---- remove all the unknown options
        for i in args:
            if i.startswith('-'):
                self.show_help(error=f'Encountered an unknown option: {i}')
                sys.exit()

        if not args:
            self.show_help(error='You did not provide me with an archive to unzip')
        else:
            archive = args[0]

            if not archive.endswith('.zip'):
                archive += '.zip'
            if not os.path.exists(archive):
                err = f"ERROR: {archive} not found"
                self.header(err)
                sys.exit()

            self.jack_the_unzipper(archive)


if __name__ == '__main__':
    app = MUnzip()
    args = sys.argv
    if len(args) == 1:
        app.show_help()

    app.main(args)
