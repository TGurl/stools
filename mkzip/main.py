#!/usr/bin/env python3
import os
import glob
import shutil
import argparse
import subprocess

from utils import TGutils
from zipfile import ZipFile, ZIP_LZMA, ZIP_BZIP2, ZIP_DEFLATED, BadZipfile

class Mkzip(TGutils):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.folder = ''
        self.output = '.'
        self.keepsource = False
        self.clearscreen = False
        self.do_test = False
        self.remove = False
        self.compression = ZIP_DEFLATED
    
    def header(self):
        if self.clearscreen:
            subprocess.call('clear')
        self.printf("Mkzip v0.01a - part of Transgirl's Simple Tools", nl=True)
  
    def collect_files_in_folder(self):
        pattern = os.path.join(self.folder, '**')
        files = glob.glob(pattern, recursive=True)
        return files

    def check_archive(self):
        try:
            with ZipFile(self.output, 'r') as zf:
                result = zf.testzip()
                if result is not None:
                    return False
                else:
                    return True
        except BadZipfile:
            self.err(f"{self.output} is not a valid ZIP file", exit_app=True)
        except Exception as e:
            self.err(f"An error occurred: {e}", exit_app=True)

    def jack_the_zipper(self):
        self.header()

        if not os.path.exists(self.folder):
            self.err(f"Cannot open {self.folder}, does it exist?", exit_app=True)

        if os.path.exists(self.output) and not self.remove:
            self.err(f"An archive by that name already exists!")
            self.err(f"Delete it manually or use -r to do it automatically", exit_app=True)
        elif os.path.exists(self.output):
            os.remove(self.output)
        else:
            pass

        filelist = self.collect_files_in_folder()
        total_files = len(filelist)
        fmt = "{:<16}: {}"
        action = 'Deflating' if self.compression == ZIP_DEFLATED else 'Compressing'

        self.fprint('Creating', self.output, fmt=fmt)
        if self.compression != ZIP_DEFLATED:
            method = 'LZMA' if self.compression == ZIP_LZMA else 'Bzip2'
            self.fprint('Method', method, fmt=fmt)

        if self.compresslevel != 7:
            self.fprint('Compress Level', self.compresslevel, fmt=fmt)

        self.fprint('Total files', total_files, fmt=fmt)
        
        with ZipFile(self.output, 'w', compresslevel=self.compresslevel, compression=self.compression) as zf:
            for i, item in enumerate(filelist, start=1):
                p = i * 100 // total_files
                filename = item
                if len(filename) > 40:
                    filename = '..' + filename[-38:]
                line = f"[{p:>3}%] {filename}"
                self.fprint(action, line, fmt=fmt)
                zf.write(item)
                self.clearlines()

        asize = self.bytes_to_human_readable(os.stat(self.output).st_size)
        self.fprint(action, "[100%] Done", fmt=fmt)
        self.fprint('Size', asize, fmt=fmt)

        if self.do_test:
            self.fprint('Testing archive', '', fmt=fmt)
            
            check = self.check_archive()
            result = 'OK' if check else '%rFAULTY%R'
            
            self.clearlines()
            self.fprint('Testing archive', result, fmt=fmt)
            
        if not self.keepsource:
            shutil.rmtree(self.folder)
            self.fprint('Removed source', 'Done', fmt=fmt)

    def main(self, args):
        self.folder = args.folder
        self.keepsource = args.keep
        self.compresslevel = args.compress
        self.clearscreen = args.noclear
        self.do_test = args.test
        self.remove = args.remove
        self.do_test = args.test

        if args.lzma:
            self.compression = ZIP_LZMA
        elif args.bzip2:
            self.compression = ZIP_BZIP2
        else:
            self.compression = ZIP_DEFLATED

        if args.output == 'folder':
            self.output = self.folder + '.zip'
        else:
            if '.zip' not in args.output:
                self.output = args.output + '.zip'
        
        try:
            self.jack_the_zipper()
        except KeyboardInterrupt:
            self.printf('\n\nProgram interrupted by user. Exiting gracefully...')
            os.remove(self.output)


if __name__ == '__main__':
    app = Mkzip()

    parser = argparse.ArgumentParser(prog='mkzip')

    parser.add_argument('folder',
                        type=str,
                        help='Folder to zip')

    parser.add_argument('-o', '--output',
                        type=str,
                        default='folder',
                        required=False,
                        help='Set output file')


    parser.add_argument('-c', '--compress',
                        type=int,
                        metavar='x',
                        default=7,
                        required=False,
                        help='Compression level (default=7)')

    compress  = parser.add_mutually_exclusive_group(required=False)

    compress.add_argument('-l', '--lzma',
                          action='store_true',
                          required=False,
                          help='Use lzma compression')

    compress.add_argument('-b', '--bzip2',
                          action='store_true',
                          required=False,
                          help='Use lzma compression')
    
    parser.add_argument('-r', '--remove',
                       action='store_true',
                       required=False,
                       help='Remove existing archive')
    
    parser.add_argument('-t', '--test',
                       action='store_true',
                       required=False,
                       help='Test the created archive')

    parser.add_argument('-k', '--keep',
                       action='store_true',
                       required=False,
                       help='Keep the source once done')
    
    parser.add_argument('-n', '--noclear',
                       action='store_true',
                       required=False,
                       help='Clear the screen')
    
    
    app.main(parser.parse_args())
