#!/usr/bin/env python3
import os
import argparse
import subprocess

from utils import TGutils
from zipfile import ZipFile


class MUnzip(TGutils):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.output = '.'
        self.keeparchive = False
        self.clearscreen = False

    def header(self):
        if self.clearscreen:
            subprocess.call('clear')
        self.printf("MUnzip v0.02a - part of Transgirl's Simple Tools", nl=True)

    def undress_archive(self, archive):
        fmt = "{:<14}: {}"

        try:
            with ZipFile(archive, 'r') as zf:
                filelist = zf.infolist()
                total = len(filelist)

                for i, item in enumerate(filelist, start=1):
                    p = i * 100 // total
                    filename = item.filename
                    if len(filename) > 40:
                        filename = '..' + filename[-38:]

                    line = f"[{p:>3}%] {filename}"
                    self.fprint('Extracting', line, fmt=fmt)

                    extracted_path = zf.extract(item, self.output)
                    if item.create_system == 3:
                        unix_attr = item.external_attr >> 16
                        if unix_attr:
                            os.chmod(extracted_path, unix_attr)
                    self.clearlines()
            
            arcsize = self.bytes_to_human_readable(os.stat(self.output).st_size)
            self.fprint('Extracting', '[100%] Done', fmt=fmt)
            self.fprint('Size', arcsize)

        except FileNotFoundError:
            self.err(f"Unable to open {archive}!", exit_app=True)
        except Exception as e:
            self.err(f"An unknown error occurred:\n\n{e}", exit_app=True)

    def main(self, args):
        if args.output:
            self.output = args.output

        self.keeparchive = args.keep
        self.clearscreen = args.clear 
       
        self.header()
        total_archives = len(args.archives)
        w = len(str(total_archives))
        fmt = "{:<14}: {}"

        for i, archive in enumerate(args.archives, start=1):
            arcsize = self.bytes_to_human_readable(os.stat(archive).st_size)
            self.fprint('Processing', f"{i:>{w}} of {total_archives}", fmt=fmt)
            self.fprint('Size', arcsize, fmt=fmt)
            self.fprint('Unzipping', archive, fmt=fmt)
            self.undress_archive(archive)
            if i < total_archives:
                self.clearlines(num=4)
        self.msg('All done...', colors=True)


if __name__ == '__main__':
    app = MUnzip()

    parser = argparse.ArgumentParser(prog='munzip')

    parser.add_argument('archives',
                        nargs='+',
                        help='<Required> Folder to archive')

    parser.add_argument('-o', '--output',
                        type=str,
                        required=False,
                        help='<optional> the final destination')

    parser.add_argument('-k', '--keep',
                        action='store_true',
                        required=False,
                        help='Keep archive once done')

    parser.add_argument('-c', '--clear',
                        action='store_true',
                        required=False,
                        help='Clear the screen')

    app.main(parser.parse_args())
