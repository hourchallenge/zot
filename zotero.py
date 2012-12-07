import os
import sys
import sqlalchemy as sql


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
        # get all items and associated field names, and store in items dictionary
        query = sql.select([self.items.c.key, self.fields.c.fieldName, self.item_data_values.c.value], 
                           (self.items.c.itemID == self.item_data.c.itemID) &
                           (self.item_data.c.fieldID == self.fields.c.fieldID) &
                           (self.item_data.c.valueID == self.item_data_values.c.valueID)
                           )
        result = query.execute()
        items = {}
        for key, field_name, value in result:
            if not key in items: items[key] = {}
            items[key][field_name] = value
            
        self.items = items

        
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


def help_msg():
    print '''Usage: zot (command) (args)
    
Commands:
    search
    best
    read
    notes
    bib
    path
    help'''
        
def main():
    if len(sys.argv) < 2:
        help_msg()
        return
        
    command = sys.argv[1]
    if command == 'help':
        help_msg()
        return
    elif command == 'path':
        arg = sys.argv[2]
        from settings import write_zotero_dir
        write_zotero_dir(arg)
        sys.exit()
        
    from settings import get_zotero_dir
    zotero_dir = get_zotero_dir()
    z = Zotero(zotero_dir)


if __name__ == '__main__':
    main()
