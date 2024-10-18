#!/usr/bin/env python3
import os
import sys
import glob
import shutil
import argparse
import subprocess

from utils import TGUtils
from pyfzf.pyfzf import FzfPrompt
from time import sleep


class Puta(TGUtils):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.app_title = 'Puta'
        self.app_slogan = 'Manage my pr0n games with ease'
        self.colors = False
        self.female_only = False
        self.male_only = False

        self.lore_path = os.path.join('/', 'lore', 'female')
        self.usb_path = os.path.join('/', 'USB', 'male')
        self.play_path = os.path.join('/', 'lore', 'playing')

    def system_check(self):
        all_ok = True
        required = ['fzf', 'mkzip', 'munzip']
        missing = []
        for app in required:
            if shutil.which(app) == None:
                all_ok = False
                missing.append(app)

        if not all_ok:
            self.app_header(clear_screen=False, colors=self.colors)
            string = ', '.join(missing)
            self.error(f"Unable to locate {string}...")
            sys.exit(1)

    def collect_all_games(self):
        if self.female_only:
            paths = [self.lore_path]
        elif self.male_only:
            paths = [self.usb_path]
        else:
            paths = [self.lore_path, self.usb_path]

        games = []
        for path in paths:
            content = glob.glob(os.path.join(path, '**', '**.zip'), recursive=True)
            games.extend(content)
        games.sort()
        return games

    def fuzzy_finder(self):
        game_list = self.collect_all_games()
        result = FzfPrompt().prompt(game_list, '--reverse --exact --multi')

        if not result:
            self.app_header(colors=self.colors)
            self.warning('No games selected...')
            sys.exit()

        return result

    def extract_games(self):
        games = " ".join(self.fuzzy_finder())
        cmd = f"munzip {games} -o {self.play_path} -c"
        subprocess.call(cmd.split())

    def main(self, args):
        self.colors = args.colors
        self.female_only = args.female
        self.male_only = args.male
        self.system_check()
        self.extract_games()



if __name__ == '__main__':
    app = Puta()

    parser = argparse.ArgumentParser(prog='puta',
                                     epilog='Released into the public domain in 2024',
                                     description='manage my pr0n games with ease')

    gender = parser.add_mutually_exclusive_group(required=False)

    gender.add_argument('-f', '--female',
                        action='store_true',
                        required=False,
                        help='Only female protagonist')

    gender.add_argument('-m', '--male',
                        action='store_true',
                        required=False,
                        help='Only male protagonist')
    
    parser.add_argument('-c', '--colors',
                        action='store_true',
                        required=False,
                        help='Colorize output')

    app.main(parser.parse_args())
