import importlib
import sys
import os
import nuke
# import hiero.ui
# import shotCreate

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
print('xolo: Nuke menu created')


# def export_shots():
#     shotCreate.export_shots()
#
# # Create a menu item in Nuke Studio
# menu = hiero.ui.menuBar().addMenu("xolo")
# action = hiero.ui.createMenuAction("Export Shots", export_shots)
# menu.addAction(action)
