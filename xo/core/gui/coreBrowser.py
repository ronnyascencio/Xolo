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

    def connect_signals(self):
        self.save_button.clicked.connect(self.save_project)
        self.save_new_version_button.clicked.connect(self.save_new_version)
        self.open_button.clicked.connect(self.open_project)
        self.project_combobox.currentIndexChanged.connect(self.update_sequences)
        self.sequence_combobox.currentIndexChanged.connect(self.update_shots)

        type_list = ['', 'character', 'environment', 'prop']
        self.type_combobox.addItems(type_list)

        # Corrected this line
        self.type_combobox.currentIndexChanged.connect(self.update_assets)

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
            print(f"Contents of {sequences_path}: {sequence_list}")
            self.sequence_combobox.clear()
            self.sequence_combobox.addItems(sequence_list)
        else:
            print(f"Path {sequences_path} does not exist.")

    def clear_asset_combobox(self):
        self.asset_combobox.clear()

    def update_assets(self):
        global selected_project
        selected_project = self.project_combobox.currentText()

        # Load the JSON config
        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        asset_type = self.type_combobox.currentText()

        # Construct the path to the assets
        assets_path = os.path.join(root_path, selected_project, 'Production', 'Assets', asset_type)

        if asset_type:  # If an asset type is selected
            if os.path.exists(assets_path):
                assets_list = os.listdir(assets_path)
                print(f"Contents of {assets_path}: {assets_list}")
                self.asset_combobox.clear()
                self.asset_combobox.addItems(assets_list)

                if assets_list:  # Enable asset combobox if there are assets
                    self.asset_combobox.setEnabled(True)
                else:  # Disable asset combobox if there are no assets
                    self.asset_combobox.setEnabled(False)
                    self.clear_asset_combobox()  # Clear asset combobox
            else:
                print(f"Path {assets_path} does not exist.")
                self.asset_combobox.setEnabled(False)  # Disable asset if path does not exist
                self.clear_asset_combobox()  # Clear asset combobox
        else:
            self.asset_combobox.setEnabled(False)  # Disable asset if no type is selected
            self.clear_asset_combobox()  # Clear asset combobox

    def update_shots(self):
        self.selected_sequence = self.sequence_combobox.currentText()
        if not self.selected_sequence:
            return

        config = self.load_config(CONFIG_FILE)
        root_path = config.get('root_path', '')
        shots_path = os.path.join(root_path, self.selected_project, 'Production', 'shots', self.selected_sequence)

        if os.path.exists(shots_path):
            shot_list = os.listdir(shots_path)
            print(f"Contents of {shots_path}: {shot_list}")
            if self.shot_combobox is not None:
                self.shot_combobox.clear()
                self.shot_combobox.addItems(shot_list)
            else:
                print("Error: shot_combobox not found. Check the object name in the UI file.")
        else:
            print(f"Path {shots_path} does not exist.")

    def select_project(self):
        try:
            config = self.load_config(CONFIG_FILE)
            root_path = config.get('root_path', '')

            if os.path.exists(root_path):
                project_list = os.listdir(root_path)
                print(f"Contents of {root_path}: {project_list}")
                self.project_combobox.clear()
                self.project_combobox.addItems(project_list)
            else:
                print(f"Path {root_path} does not exist.")
        except Exception as e:
            print(f"Error loading project list: {e}")

    # DCC SELECTOR
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

    # Nuke functions
    def save_project_nuke(self):
        import nuke
        nuke.message("Saving project in Nuke")
        print("Saving project in Nuke")

    def save_new_version_nuke(self):
        print("Saving new version in Nuke")

    def open_project_nuke(self):
        print("Opening project in Nuke")

    # Houdini functions
    def save_project_houdini(self):
        print("Saving project in Houdini")

    def save_new_version_houdini(self):
        print("Saving new version in Houdini")

    def open_project_houdini(self):
        print("Opening project in Houdini")


def start(dcc):
    global main_widget
    main_widget = ProjectBrowser(dcc)
    print(f"Started ProjectBrowser for {dcc}")

# Example of how to start the ProjectBrowser for Nuke or Houdini
# start("nuke")  # Uncomment to start for Nuke
# start("houdini")  # Uncomment to start for Houdini
