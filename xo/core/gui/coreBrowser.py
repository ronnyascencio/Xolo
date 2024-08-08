import os
import json
from PySide2 import QtCore, QtWidgets, QtUiTools


DIR_PATH = os.path.dirname(__file__).replace('\\', '/')
ROOT_PATH = DIR_PATH.replace('/core/gui', '/')
UI_PATH = os.path.join(ROOT_PATH, "ui/pbrowser.ui")
CONFIG_FILE = os.path.join(ROOT_PATH, 'config.json')  # Adjust this path accordingly


class ProjectBrowser(QtWidgets.QWidget):
    def __init__(self, dcc):
        super(ProjectBrowser, self).__init__()
        self.dcc = dcc
        self.wg_browser = QtUiTools.QUiLoader().load(UI_PATH)
        self.setup_ui()
        self.connect_signals()

        # Show the widget
        self.wg_browser.show()

        # Load projects based on DCC
        self.select_project()

        # Initialize selected project and sequence
        self.selected_project = ""
        self.selected_sequence = ""

        # Show or hide type and asset fields based on DCC
        self.show_hide_type_asset_fields()

    def setup_ui(self):
        self.project_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_project")
        self.sequence_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_sequence")
        self.shot_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_shots")
        self.type_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_type")
        self.asset_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_asset")
        self.department_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_departments")
        self.task_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_tasks")
        self.script_version_combobox = self.wg_browser.findChild(QtWidgets.QComboBox, "cbb_script")
        self.save_button = self.wg_browser.findChild(QtWidgets.QPushButton, "btn_save")
        self.save_new_version_button = self.wg_browser.findChild(QtWidgets.QPushButton, "btn_new_version")
        self.open_button = self.wg_browser.findChild(QtWidgets.QPushButton, "btn_open")

        # Labels
        self.lbl_type = self.wg_browser.findChild(QtWidgets.QLabel, "lbl_type")
        self.lbl_asset = self.wg_browser.findChild(QtWidgets.QLabel, "lbl_asset")
        self.lbl_path_info = self.wg_browser.findChild(QtWidgets.QLabel, "lbl_path_info")

    def connect_signals(self):
        self.save_button.clicked.connect(self.save_project)
        self.save_new_version_button.clicked.connect(self.save_new_version)
        self.open_button.clicked.connect(self.open_project)
        self.project_combobox.currentIndexChanged.connect(self.update_sequences)
        self.sequence_combobox.currentIndexChanged.connect(self.update_shots)
        self.shot_combobox.currentIndexChanged.connect(self.set_path)
        self.type_combobox.currentIndexChanged.connect(self.update_assets)
        self.type_combobox.currentIndexChanged.connect(self.update_departments)
        self.department_combobox.currentIndexChanged.connect(self.update_tasks)
        self.script_version_combobox.currentIndexChanged.connect(self.set_path)

        type_list = ['', 'character', 'environment', 'props']
        self.type_combobox.addItems(type_list)

        # Initial setup for departments and tasks
        self.update_departments()
        self.update_tasks()


    def load_config(self, config_file):
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        with open(config_file, 'r') as file:
            config = json.load(file)

        if 'root_path' not in config:
            raise KeyError("The config file does not contain 'root_path' key")

        return config

    def update_sequences(self):
        self.selected_project = self.project_combobox.currentText()
        if not self.selected_project:
            return

        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        sequences_path = os.path.join(root_path, self.selected_project, 'Production', 'Shots')

        if os.path.exists(sequences_path):
            sequence_list = os.listdir(sequences_path)
            self.sequence_combobox.clear()
            self.sequence_combobox.addItems(sequence_list)
        else:
            self.sequence_combobox.clear()

        self.set_path()

    def clear_asset_combobox(self):
        self.asset_combobox.clear()

    def update_assets(self):
        self.selected_project = self.project_combobox.currentText()
        asset_type = self.type_combobox.currentText()

        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        assets_path = os.path.join(root_path, self.selected_project, 'Production', 'Assets', asset_type)

        if asset_type and os.path.exists(assets_path):
            assets_list = os.listdir(assets_path)
            self.asset_combobox.clear()
            self.asset_combobox.addItems(assets_list)
            self.asset_combobox.setEnabled(bool(assets_list))
        else:
            self.asset_combobox.clear()
            self.asset_combobox.setEnabled(False)

        self.set_path()

    def update_shots(self):
        self.selected_sequence = self.sequence_combobox.currentText()
        if not self.selected_sequence:
            return

        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        shots_path = os.path.join(root_path, self.selected_project, 'Production', 'Shots', self.selected_sequence)

        if os.path.exists(shots_path):
            shot_list = os.listdir(shots_path)
            self.shot_combobox.clear()
            self.shot_combobox.addItems(shot_list)
        else:
            self.shot_combobox.clear()

        self.set_path()

    def select_project(self):
        try:
            config = self.load_config(CONFIG_FILE)
            root_path = config.get('root_path', '')

            if os.path.exists(root_path):
                project_list = os.listdir(root_path)
                #print(f"Contents of {root_path}: {project_list}")
                self.project_combobox.clear()
                self.project_combobox.addItems(project_list)
            else:
                print(f"Path {root_path} does not exist.")
        except Exception as e:
            print(f"Error loading project list: {e}")




    # DCC SELECTOR

    def show_hide_type_asset_fields(self):
        if self.dcc == "nuke":
            self.lbl_type.hide()
            self.lbl_asset.hide()
            self.type_combobox.hide()
            self.asset_combobox.hide()
        else:
            self.lbl_type.show()
            self.lbl_asset.show()
            self.type_combobox.show()
            self.asset_combobox.show()
    def save_project(self):
        if self.dcc == "nuke":
            self.save_project_nuke()
        elif self.dcc == "houdini":
            self.save_project_houdini()

    def save_new_version(self):
        if self.dcc == "nuke":
            self.save_new_version_nuke()
        elif self.dcc == "houdini":
            self.save_new_version_houdini()

    def open_project(self):
        if self.dcc == "nuke":
            self.open_project_nuke()
        elif self.dcc == "houdini":
            self.open_project_houdini()

    def update_departments(self):
        departments = []
        if self.dcc == "nuke":
            departments = ['cmp', 'prep', 'lgt']
        elif self.dcc == "houdini":
            departments_assets = ['mod', 'rig', 'lkd']
            departments_shot = ['lay', 'anim', 'fx', 'lgt']
            type_selected = self.type_combobox.currentText()
            if type_selected in ['character', 'props', 'environment']:
                departments = departments_assets
            else:
                departments = departments_shot

        self.department_combobox.clear()
        self.department_combobox.addItems(departments)
        self.set_path()

    def update_tasks(self):
        tasks = []
        if self.dcc == "nuke":
            department_selected = self.department_combobox.currentText()
            if department_selected == 'cmp':
                tasks = ['Compositing']
            elif department_selected == 'prep':
                tasks = ['Prep']
            elif department_selected == 'lgt':
                tasks = ['Lighting']
        elif self.dcc == "houdini":

            department_selected = self.department_combobox.currentText()
            if department_selected in ['mod', 'rig', 'lkd']:
                if department_selected == 'mod':
                    tasks = ['Modeling']
                elif department_selected == 'rig':
                    tasks = ['Rigging']
                elif department_selected == 'lkd':
                    tasks = ['LookDev']

            else:
                if department_selected == 'lay':
                    tasks = ['Layout']
                elif department_selected == 'anim':
                    tasks = ['Animation']
                elif department_selected == 'fx':
                    tasks = ['Fx']
                elif department_selected == 'lgt':
                    tasks = ['Lighting']



        self.task_combobox.clear()
        self.task_combobox.addItems(tasks)
        self.set_path()

    def set_path(self):
        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        project = self.project_combobox.currentText()
        sequence = self.sequence_combobox.currentText()
        shot = self.shot_combobox.currentText()
        type_ = self.type_combobox.currentText()
        asset = self.asset_combobox.currentText()
        department = self.department_combobox.currentText()
        task = self.task_combobox.currentText()
        script_version = self.script_version_combobox.currentText()

        path = ""
        if self.dcc == "nuke":
            path = os.path.join(root_path, project, 'Production', 'Shots', sequence, shot, 'Scenefiles', department, task)
            self.update_script_combobox(path, '.nk')
        elif self.dcc == "houdini":
            if type_:
                path = os.path.join(root_path, project, 'Production', 'Assets', type_, asset, 'Scenefiles', department, task)
            else:
                path = os.path.join(root_path, project, 'Production', 'Shots', sequence, shot, 'Scenefiles', department, task)
            self.update_script_combobox(path, '.hiplc')

        if script_version:
            path = os.path.join(path, script_version)

        self.lbl_path_info.setText(path)
        print(f"Path updated to: {path}")  # Add logging to verify path updates

    def update_script_combobox(self, path, extension):
        self.script_version_combobox.blockSignals(True)
        self.script_version_combobox.clear()
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.endswith(extension)]
            self.script_version_combobox.addItems(files)
        self.script_version_combobox.blockSignals(False)






    # Nuke functions
    def save_project_nuke(self):
        import nuke
        script_path = self.lbl_path_info.text()
        shot = self.shot_combobox.currentText()
        task = self.task_combobox.currentText()
        file_name = script_path + '/' + shot + '_' + task + '_v001.nk'
        script_name = shot + '_' + task + '_v001.nk'
        if nuke.ask(f'is this the correct shot?: {script_name}'):
            if not os.path.exists(script_path):
                os.makedirs(script_path)
                nuke.scriptSaveAs(file_name)
                if os.path.exists(file_name):
                    nuke.message(f'script saved:{file_name}')
        else:
            nuke.message('Script not saved')


    def save_new_version_nuke(self):
        import nuke
        import nukescripts
        nukescripts.script.script_version_up()

    def open_project_nuke(self):
        import nuke

        script_path = self.lbl_path_info.text()

        nuke.scriptOpen(script_path)



    # Houdini functions
    def save_project_houdini(self):
        import hou
        import os

        script_path = self.lbl_path_info.text()
        shot = self.shot_combobox.currentText()
        task = self.task_combobox.currentText()
        type_ = self.type_combobox.currentText()
        asset = self.asset_combobox.currentText()

        # Determine if it's an asset or shot work
        if any(keyword in script_path for keyword in ['character', 'props', 'environment']):
            file_name = os.path.join(script_path, f'{asset}_{task}_v001.hiplc')
            script_name = f'{asset}_{task}_v001.hiplc'
            if hou.ui.displayMessage(f'Is this the correct shot?: {script_name}', buttons=('Yes', 'No')) == 0:
                if not os.path.exists(script_path):
                    os.makedirs(script_path)
                hou.hipFile.save(file_name)
                if os.path.exists(file_name):
                    hou.ui.displayMessage(f'Script saved: {file_name}')
            else:
                hou.ui.displayMessage('Script not saved')
        else:
            file_name = os.path.join(script_path, f'{shot}_{task}_v001.hiplc')
            script_name = f'{shot}_{task}_v001.hiplc'
            if hou.ui.displayMessage(f'Is this the correct shot?: {script_name}', buttons=('Yes', 'No')) == 0:
                if not os.path.exists(script_path):
                    os.makedirs(script_path)
                hou.hipFile.save(file_name)
                if os.path.exists(file_name):
                    hou.ui.displayMessage(f'Script saved: {file_name}')
            else:
                hou.ui.displayMessage('Script not saved')

    def save_new_version_houdini(self):
        import hou
        import os
        import re

        script_path = self.lbl_path_info.text()
        shot = self.shot_combobox.currentText()
        task = self.task_combobox.currentText()
        type_ = self.type_combobox.currentText()
        asset = self.asset_combobox.currentText()

        # Determine if it's an asset or shot work
        if any(keyword in script_path for keyword in ['character', 'prop', 'environment']):
            file_base = f'{asset}_{task}_v'
        else:
            file_base = f'{shot}_{task}_v'

        # Extract the directory path and ensure it exists
        directory_path = os.path.dirname(script_path)
        if not os.path.isdir(directory_path):
            hou.ui.displayMessage(f'Directory does not exist: {directory_path}')
            return

        # Find existing versions
        existing_versions = [int(re.search(rf'{file_base}(\d{{3}}).hiplc$', f).group(1)) for f in
                             os.listdir(directory_path) if re.search(rf'{file_base}(\d{{3}}).hiplc$', f)]
        if existing_versions:
            next_version = max(existing_versions) + 1
        else:
            next_version = 1

        file_name = os.path.join(directory_path, f'{file_base}{next_version:03d}.hiplc')
        script_name = f'{file_base}{next_version:03d}.hiplc'

        if hou.ui.displayMessage(f'Save as new version?: {script_name}', buttons=('Yes', 'No')) == 0:
            hou.hipFile.save(file_name)
            if os.path.exists(file_name):
                hou.ui.displayMessage(f'New version saved: {file_name}')
        else:
            hou.ui.displayMessage('Save new version canceled')

    def open_project_houdini(self):
        import hou

        script_path = self.lbl_path_info.text()

        if os.path.exists(script_path):
            hou.hipFile.load(script_path)
            hou.ui.displayMessage(f'Project opened: {script_path}')
        else:
            hou.ui.displayMessage(f'File does not exist: {script_path}')


def start(dcc):
    global main_widget
    main_widget = ProjectBrowser(dcc)
    print(f"Started ProjectBrowser for {dcc}")


