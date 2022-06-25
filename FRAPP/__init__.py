import os

__version__ = '1.1.1'

# set Python env variable to keep track of example data dir
frapp_dir = os.path.dirname(__file__)
DATADIR = os.path.join(frapp_dir, 'Examples/')
