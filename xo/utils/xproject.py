import sys
import os
import yaml
import onProjectCreate
from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools

# main variables

ROOT_PATH = os.path.dirname(__file__).replace('\\utils', '')
IMG_PATH = ROOT_PATH + '/ui/icons/xproject.png'
UI_PATH = ROOT_PATH + "/ui/pcreator.ui"
FILE_PATH = os.path.dirname(__file__)


class Saver:
    def __init__(self):


 # Stand Alone
def create():

    app = QtWidgets.QApplication(sys.argv)
    main_widget = ProjectCreator()
    sys.exit(app.exec_())

# DCC start

def start():

    global main_widget
    main_widget = ProjectCreator()

create()