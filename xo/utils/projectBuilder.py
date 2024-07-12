import sys
import os
import yaml
from utils import onProjectCreate
from PySide2 import QtCore, QtWidgets, QtGui, QtUiTools

# main variables

DIR_PATH = os.path.dirname(__file__).replace('\\utils', '')
IMG_PATH = DIR_PATH + '/ui/icons/xproject.png'
UI_PATH = DIR_PATH + "/ui/pcreator.ui"
MAIN_STRUCTURE = os.path.dirname(__file__)


class ProjectCreator:
    def __init__(self):
        # LOAD Ui
        self.wg_creator = QtUiTools.QUiLoader().load(UI_PATH)

        # Connect button with functions
        self.wg_creator.btn_search.clicked.connect(self.press_search)
        self.wg_creator.btn_create.clicked.connect(self.press_create)
        # set image
        pixmap = QtGui.QPixmap(IMG_PATH)
        self.wg_creator.lbl_image.setPixmap(pixmap)

        # show
        self.wg_creator.show()

    def press_search(self):
        options = QtWidgets.QFileDialog.Options()
        directory = QtWidgets.QFileDialog.getExistingDirectory(
            None, "Select Directory", QtCore.QDir.homePath(), options=options)
        if directory:
            self.wg_creator.edt_directory.setText(directory)
        else:
            print('no directory selected ')

    def press_create(self):

        # project settings variables
        project_name = self.wg_creator.edt_project.text()
        project_dir = self.wg_creator.edt_directory.text()
        selected_type = self.wg_creator.cbb_type.currentText()
        selected_format = self.wg_creator.cbb_format.currentText()
        selected_fps = self.wg_creator.cbb_fps.currentText()
        project_root = project_dir + '/' + project_name
        # Debug
        print(project_root)
        # Check if project_root exists, create if not
        if not os.path.exists(project_root):
            os.makedirs(project_root)

        self.create_folders(project_root)

        # project data
        data = {
            'project name': project_name,
            'project type': selected_type,
            'resolution': selected_format,
            'fps': selected_fps
        }
        file_path = project_root + '/' + '.$PROJECT_info.yaml'

        with open(file_path, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)

        # folder structure creation

    def create_folders(self, base_path):
        if self.wg_creator.cbb_type.currentText() == 'Commercial':
            onProjectCreate.commercialstructure(base_path)
        elif self.wg_creator.cbb_type.currentText() == 'Animation':
            onProjectCreate.animationstructure(base_path)
        elif self.wg_creator.cbb_type.currentText() == 'VFX':
            onProjectCreate.vfxstructure(base_path)
        elif self.wg_creator.cbb_type.currentText() == 'Shot':
            onProjectCreate.shotstructure(base_path)
        else:
            print('no folder was created')


# Stand Alone
def create():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ProjectCreator()
    sys.exit(app.exec_())


# DCC start


def start():
    global main_widget
    main_widget = ProjectCreator()

