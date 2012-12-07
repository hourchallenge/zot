zot is a command line interface to Zotero.

    Usage: zot (command) args

    Commands:
        search [keywords]: return keys of all matching items
        best [keywords]: return key of best search match
        bib [keys]: view bibliography for one or more items
        cit [keys]: view citations for one or more items
        files [keys]: view all attached files for one or more items
        read [keys]: view text content of attached PDFs for one or more items
        notes [keys]: view all notes for one or more items
        path (zotero_dir): set the path to your Zotero directory
        help


Before using, you'll need to set your Zotero path, like this:
    
    zot path /path/to/Zotero/directory/

Searches will return a list of keys which can be piped back to zot to do things with the results.
For example, 

    zot search --collection "home range"

will return the keys of items which are in a collection
whose name contains the words "home range." 

    zot search --collection "home range" | zot bib

will display the full bibliography for each of these items,

    zot search --collection "home range" | zot files

will display a list of all files attached to these items, etc.