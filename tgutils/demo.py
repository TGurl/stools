#!/usr/bin/env python3
from utils import TGUtils

class Demo(TGUtils):
    def __init__(self):
        super().__init__()

    def run(self):
        self.app_title = 'Demo'
        self.app_slogan = 'Wanna fuck me?'
        self.app_header(clear_screen=True, nl=False)
        self.app_header(nl=False, colors=False)


if __name__ == '__main__':
    demo= Demo()
    demo.run()
