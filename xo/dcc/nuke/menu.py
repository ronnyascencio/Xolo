import importlib
import sys
import os
import nuke

root_dir = os.path.dirname(__file__).replace('dcc', 'core').replace('nuke', 'gui')
sys.path.append(root_dir)

import coreBrowser
import importlib

importlib.reload(coreBrowser)
# Debug print to verify path and imports
print('loaded: xolo')

# Nuke menu
xolo_menu = nuke.menu('Nuke').addMenu('xolo')
xolo_menu.addCommand('Project Browser', "coreBrowser.start('nuke')")
print('Nuke menu created')
