import sys
import nuke
import os
FILE_PATH = os.path.dirname(__file__).replace('\\dcc\\nuke', '')
MODULE_PATH = FILE_PATH.replace('\\', '/') + '/core/gui'

if MODULE_PATH not in sys.path:
    sys.path.append(MODULE_PATH)
