import os
import sys
import sqlalchemy as sql
from settings import zotero_dir


class Zotero:
    def __init__(self, zotero_dir):
        self.zotero_dir = zotero_dir
        self.zotero_db_path = os.path.abspath(os.path.join(zotero_dir, 'zotero.sqlite'))
        self.zotero_storage_path = os.path.join(zotero_dir, 'storage/')
        if not os.path.exists(self.zotero_db_path):
            raise Exception('Zotero db not found at %s.' % self.zotero_db_path)
        self.db = sql.create_engine('sqlite:///' + self.zotero_db_path)
        self.db.echo = False
        self.metadata = sql.MetaData(self.db)

        # tables
        self.items = sql.Table('items', self.metadata, autoload=True)
        self.fields = sql.Table('fields', self.metadata, autoload=True)
        self.item_data = sql.Table('itemData', self.metadata, autoload=True)
        

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
