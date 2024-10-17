#!/usr/bin/env python3
from utils import TGutils


class MUnzip(TGutils):
    def __init__(self):
        super().__init__()
        self.initialize()

    def initialize(self):
        self.title = '%yMUnzip v0.01a%R%F - %gTransgirl 2024%R'

    def main(self):
        self.header(self.title, ascii=True)


if __name__ == '__main__':
    app = MUnzip()
    app.main()
