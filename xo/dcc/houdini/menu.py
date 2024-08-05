import hou

import os
import sys
root_dir = os.path.dirname(__file__).replace('dcc', 'core').replace('houdini', 'gui')
print('root dir ', root_dir)
sys.path.append(root_dir)

import importlib
import coreBrowser

importlib.reload(coreBrowser)
coreBrowser.start()