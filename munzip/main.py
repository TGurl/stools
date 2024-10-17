#!/usr/bin/env python3
from zipfile import ZipFile, BadZipfile
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
        self.skip_test = False
        self.cls = False

    def show_help(self, error=''):
        fmt = "    {:<4} {}"
        self.header(self.title, clear=self.cls, nl=True)
        if error:
            self.printf(f"ERROR:")
            self.printf(f'    {error}', nl=True)
        self.printf('Usage:')
        self.printf(f'    {self.app_name} [options] <zip-file>', nl=True)
        self.printf('Options:')

        options = [
            {'opt': '-s', 'ex': 'Skip test zip-file before unzipping'},
            {'opt': '-k', 'ex': 'Keep zip-file when done'},
            {'opt': '-c', 'ex': 'Clear the screen before starting'},
            {'opt': '-h', 'ex': 'Show this help screen'},
        ]

        for option in options:
            self.fprint(option['opt'], option['ex'], fmt=fmt)
        
        sys.exit()

    def remove_options(self, args, remove):
        for r in remove:
            if r in args:
                idx = args.index(r)
                args.pop(idx)
        return args

    def is_valid_zip(self, archive):
        if not os.path.isfile(archive):
            self.show_help(error=f"Unable to open {archive}")

        if not archive.lower().endswith('.zip'):
            self.show_help(error=f"{archive} doesn't look like a valid zip archive")

        try:
            with ZipFile(archive, 'r') as zf:
                result = False
                if not self.skip_test:
                    self.printf(' > Checking archive...')
                    result = zf.testzip()
                return result
        except BadZipfile:
            self.show_help(error=f"{archive} is not a valid zip archive")
        except Exception as e:
            self.show_help(error=f"Ooops! {e}")

    def jack_the_unzipper(self, archive, dest_dir='.'):
        ret_code = self.is_valid_zip(archive) 
        self.clearlines()

        if not ret_code:
            archive_bytes = os.stat(archive).st_size
            archive_size = self.bytes_to_human_readable(archive_bytes)
            fmt = " > {:<12}: {}"
            self.header(self.title, clear=self.cls)
            self.fprint("Unzipping", archive, fmt=fmt)
            self.fprint("Size", archive_size, fmt=fmt)

            with ZipFile(archive, 'r') as zf:
                filelist = zf.infolist()
                total = len(filelist)

                for i, item in enumerate(filelist, start=1):
                    p = i * 100 // total
                    fname = item.filename
                    if len(fname) > 40:
                        fname = '..' + fname[-38:]
                    info = f"[{p:>3}%] {fname}"
                    self.fprint('Extracting', info, fmt=fmt)

                    extracted_path = zf.extract(item, dest_dir)
                    if item.create_system == 3:
                        unix_attr = item.external_attr >> 16
                        if unix_attr:
                            os.chmod(extracted_path, unix_attr)
                    self.clearlines()
            self.fprint('Extracting', 'Done', fmt=fmt)

            if not self.keep_archive:
                os.remove(archive)
                self.fprint('Remove zip', 'Done', fmt=fmt)


    def main(self, args):
        self.app_name = args[0]
        args.pop(0)

        # ---- parse the argumetns
        if '-c' in args or '-C' in args:
            self.cls = True
            args = self.remove_options(args, ['-c', '-C'])
        
        if '-h' in args or '-H' in args:
            self.show_help()

        if '-k' in args or '-K' in args:
            self.keep_archive = True
            args = self.remove_options(args, ['-k', '-K'])

        if '-s' in args or '-S' in args:
            self.skip_test = True
            args = self.remove_options(args, ['-s', '-S'])

        # ---- remove all the unknown options
        for i in args:
            if i.startswith('-'):
                self.show_help(error=f'Encountered an unknown option: {i}')

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
