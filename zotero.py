import os
import sys
import sqlalchemy as sql
from item import Item


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
        self.item_data_values = sql.Table('itemDataValues', self.metadata, autoload=True)
        self.item_attachments = sql.Table('itemAttachments', self.metadata, autoload=True)
        self.collections = sql.Table('collections', self.metadata, autoload=True)
        self.collection_items = sql.Table('collectionItems', self.metadata, autoload=True)
        
        self.get_items()
        

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
            if not key in items: items[key] = {'key': key}
            items[key][field_name] = value
            
        self.all_items = {k: Item(v) for k, v in items.items()}

        
    def search(self, best=False, **kwargs):
        matches = [(item, item.match(**kwargs)) for item in self.all_items.values()]
        
        # TODO: return only best
        return filter(lambda m: m[1] > 0, matches)
        
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
        
    command = sys.argv[1].lower()
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
    
    if command in ('search', 'best'):
        args = {}
        n = 2
        set_arg = 'keywords'
        while n < len(sys.argv):
            if not set_arg in args: args[set_arg] = []
            arg = sys.argv[n]
            if arg.startswith('--'): set_arg = arg[2:]
            else: args[set_arg].append(arg)
            n += 1
            
        result = z.search(best=command=='best', **args)
        for i in result:
            print i
    elif command == 'debug':
        for i in [item.__dict__ for item in z.all_items.values()]: print i
    else:
        help_msg()
        return


if __name__ == '__main__':
    main()
