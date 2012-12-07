import os
import sys
import sqlalchemy as sql
from settings import zotero_dir


class Zotero:
    def __init__(self, zotero_dir):
        pass
        

    def get_items(self):
        pass
        

    def search(self, **kwargs):
        pass
        
    def read(self, keys):
        pass
        
    def notes(self, keys):
        pass
        
    def add_note(self, key, note_txt):
        pass
        
    def bib(self, keys):
        pass
        
        
def main():
    z = Zotero(zotero_dir)


if __name__ == '__main__':
    main()
