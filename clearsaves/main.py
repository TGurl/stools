#!/usr/bin/env python3
import os
import sys
import shutil


class ClearSaves():
    def __init__(self):
        self.proper_cleaned = "Ren'Py cache cleared"
        self.proper_notneeded = "Not needed"
        self.insult_cleaned = "I cleaned up the mess you left behind, you little slut!"
        self.insult_notneeded = "You haven't had any clients yet, you whore!"

    def remove_item(self, item):
        if os.path.isdir(item):
            shutil.rmtree(item)
        else:
            os.remove(item)

    def clean_system(self, insult=False):
        cleared_msg = self.insult_cleaned if insult else self.proper_cleaned
        notneeded_msg = self.insult_notneeded if insult else self.proper_notneeded

        items_to_clear = []
        # --- collect all the files in ~/.renpy
        home_cache = os.path.expanduser(os.path.join('~', '.renpy'))
        blacklist = ['launcher-4', 'persistent', 'tokens']
        for item in os.scandir(home_cache):
            if os.path.isdir(item.path) and item.name not in blacklist:
                items_to_clear.append(item.path)

        # -- collect the renpy SDK cache
        sdk_cache = os.path.expanduser(os.path.join('~', 'Downloads', 'Renpy'))
        for item in os.scandir(sdk_cache):
            path = os.path.join(item.path, 'tmp')
            if os.path.exists(path):
                items_to_clear.append(path)

        # -- collect the renpy DEV cache
        dev_cache = os.path.expanduser(os.path.join('~', 'Dev', 'renpy', 'my_games'))
        for item in os.scandir(dev_cache):
            if 'dists' in item.name:
                items_to_clear.append(item.path)

        # -- clean the sytem when needed
        if items_to_clear:
            for item in items_to_clear:
                self.remove_item(item)
            print(cleared_msg)
        else:
            print(notneeded_msg)

    def main(self, insult=False):
        self.clean_system(insult)



if __name__ == '__main__':
    args = []
    if len(sys.argv) > 1:
        args = sys.argv[1:]

    args = [i.lower() for i in args]
    insult = '-i' in args
   
    app = ClearSaves()
    app.main(insult)
