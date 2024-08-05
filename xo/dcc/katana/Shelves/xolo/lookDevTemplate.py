"""
NAME: lookdev_template
ICON: icon.pg
DROP_TYPES:

"""
from Katana import KatanaFile
import sys
import os
import inspect

# Get the directory of the current script
current_script_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

# Set the XOLO_ROOT environment variable relative to the current script directory
# Assuming the script is within the 'Shelves/xolo' directory
xolo_root = os.path.abspath(os.path.join(current_script_dir, '..', '..', '..', '..'))
os.environ['XOLO_ROOT'] = xolo_root

# Retrieve the XOLO_ROOT environment variable
xolo_root = os.getenv('XOLO_ROOT')
lookdev_template = os.path.join(xolo_root, 'dcc', 'katana', 'templates', 'lookdev_v001.katana')
print(lookdev_template)
def FloatNodes(nodeList):
    NodegraphPanel1 = UI4.App.Tabs.FindTopTab('Node Graph')
    if NodegraphPanel1:
        for n in NodegraphAPI.GetAllSelectedNodes():
            NodegraphAPI.SetNodeSelected(n, False)
        for n in nodeList:
            NodegraphAPI.SetNodeSelected(n, True)
        # NodegraphPanel1.prepareFloatingLayerWithPasteBound(modelList)
        NodegraphPanel1.enableFloatingLayer()


nodes = KatanaFile.Import(lookdev_template)
FloatNodes(nodes)