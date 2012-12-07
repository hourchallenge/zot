import argparse
import ConfigParser
import os
import sys


def make_dir_if_not_exists(path):
    if not os.path.exists(path): os.makedirs(path)

home_dir = os.path.expanduser('~/.zot/')
make_dir_if_not_exists(home_dir)
config_file_path = os.path.join(home_dir, 'settings')


config = ConfigParser.SafeConfigParser()
if not config.has_section('zot'): config.add_section('zot')
config.read(config_file_path)
try:
    zotero_dir = config.get('zot', 'zotero_dir')
except ConfigParser.NoOptionError:
    print '''No Zotero directory defined. Run 'zotero path [zotero_dir]' to set your Zotero directory.'''
    sys.exit()
