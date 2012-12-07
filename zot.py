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
        self.item_creators = sql.Table('itemCreators', self.metadata, autoload=True)
        self.creators = sql.Table('creators', self.metadata, autoload=True)
        self.creator_data = sql.Table('creatorData', self.metadata, autoload=True)
        self.item_notes = sql.Table('itemNotes', self.metadata, autoload=True)
        
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
            if field_name == 'date':
                items[key]['year'] = value[:4]
            else: items[key][field_name] = value
            
        # get authors for these items
        query = sql.select([self.items.c.key, self.creator_data.c.lastName, self.creator_data.c.firstName],
                           (self.items.c.itemID == self.item_creators.c.itemID) &
                           (self.creators.c.creatorID == self.item_creators.c.creatorID) &
                           (self.creators.c.creatorDataID == self.creator_data.c.creatorDataID)
                           )
        result = query.execute()
        for key, last, first in result:
            if not key in items: items[key] = {'key': key}
            if not 'authors' in items[key]: items[key]['authors'] = []
            items[key]['authors'].append((last, first))
            
        # get all PDF attachments for these items
        query = sql.select([self.items.c.key, self.item_attachments.c.path],
                           (self.items.c.itemID == self.item_attachments.c.itemID) &
                           (self.item_attachments.c.mimeType == 'application/pdf')
                           )
        result = query.execute()
        for key, path in result:
            if not key in items: items[key] = {'key': key}
            if not 'attachments' in items[key]: items[key]['attachments'] = []
            items[key]['attachments'].append(path)
            
        # get all notes for these items
        query = sql.select([self.items.c.key, self.item_notes.c.note],
                           (self.items.c.itemID == self.item_notes.c.itemID)
                           )
        result = query.execute()
        for key, note in result:
            if not key in items: items[key] = {'key': key}
            if not 'notes' in items[key]: items[key]['notes'] = []
            items[key]['notes'].append(note)

        # get all collections
        query = sql.select([self.collections.c.collectionName, self.items.c.key],
                           (self.collections.c.collectionID == self.collection_items.c.collectionID) &
                           (self.collection_items.c.itemID == self.items.c.itemID)
                           )
        result = query.execute()
        collections = {}
        for collection, key in result:
            if not collection in collections: collections[collection] = set()
            collections[collection].add(key)
            if not key in items: items[key] = {'key': key}
            if not 'collections' in items[key]: items[key]['collections'] = set()
            items[key]['collections'].add(collection)
            
        self.all_items = {k: Item(v) for k, v in items.items()}

        
    def search(self, best=False, **kwargs):
        matches = [(item, item.match(**kwargs)) for item in self.all_items.values()]
        
        if not matches: return []
        if best: return [sorted(matches, key = lambda m: m[1], reverse=True)[0][0]]
        return [m[0] for m in filter(lambda m: m[1] > 0, matches)]
        
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
    search [keywords]: return keys of all matching items
    best [keywords]: return key of best search match
    bib [keys]: view bibliography for one or more items
    cit [keys]: view citations for one or more items
    files [keys]: view all attached files for one or more items
    read [keys]: view text content of attached PDFs for one or more items
    notes [keys]: view all notes for one or more items
    path (zotero_dir): set the path to your Zotero directory
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
    
    if len(sys.argv) > 2: args = sys.argv[2:]
    else:
        args = []
        for line in sys.__stdin__:
            args.append(line.strip())
    
    
    if command in ('search', 'best'):
        search_args = {}
        n = 0
        set_arg = 'keywords'
        while n < len(args):
            if not set_arg in search_args: search_args[set_arg] = []
            arg = args[n]
            if arg.startswith('--'): set_arg = arg[2:]
            else: search_args[set_arg].append(arg)
            n += 1
            
        result = z.search(best=command=='best', **search_args)
        for i in result:
            print getattr(i, 'key')
    elif command in ('bib', 'bibliography'):
        for result in [z.all_items[key].bibliography() for key in args]:
            print result
    elif command in ('cit', 'cite', 'citation'):
        for result in [z.all_items[key].citation() for key in args]:
            print result
    elif command == 'files':
        for result in [z.all_items[key] for key in args]:
            if hasattr(result, 'attachments'):
                for attachment in result.attachments:
                    print result.format_filename(attachment, z.zotero_storage_path)
    elif command == 'read':
        for key in args:
            z.all_items[key].get_full_text(z.zotero_storage_path)
    elif command == 'notes':
        for result in [z.all_items[key] for key in args]:
            if hasattr(result, 'notes'):
                for note in result.notes: print note
    elif command == 'debug':
        for i in [item.__dict__ for item in z.all_items.values()]: print i
    else:
        help_msg()
        return


if __name__ == '__main__':
    main()
