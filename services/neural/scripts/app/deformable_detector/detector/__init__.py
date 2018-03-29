import os
import sys


def add_path(path):
    if path not in sys.path:
        sys.path.insert(0, path)


this_dir = os.path.dirname(__file__)

lib_path = os.path.join(this_dir, '..', 'libs', 'lib')
add_path(lib_path)

lib_path = os.path.join(this_dir, '..', 'libs', 'src')
add_path(lib_path)