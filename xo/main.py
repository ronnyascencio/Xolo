import sys
from PySide2 import QtWidgets
from xo.core.gui.projectBuilder import ProjectCreator
from xo.core.gui.ssCreator import SequenceShotCreator

class MainApp(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('XOLO Main Menu')
        layout = QtWidgets.QVBoxLayout()

        # Buttons to launch different GUIs
        btn_project_creator = QtWidgets.QPushButton('Project Creator')
        btn_sequence_shot_creator = QtWidgets.QPushButton('Sequence and Shot Creator')

        btn_project_creator.clicked.connect(self.launch_project_creator)
        btn_sequence_shot_creator.clicked.connect(self.launch_sequence_shot_creator)

        layout.addWidget(btn_project_creator)
        layout.addWidget(btn_sequence_shot_creator)

        self.setLayout(layout)

    def launch_project_creator(self):
        self.project_creator = ProjectCreator()
        self.project_creator.wg_creator.show()

    def launch_sequence_shot_creator(self):
        self.sequence_shot_creator = SequenceShotCreator()
        self.sequence_shot_creator.show()

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = MainApp()
    main_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
