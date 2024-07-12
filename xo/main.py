import sys
from PySide2 import QtWidgets
from utils.projectBuilder import ProjectCreator


def main():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = ProjectCreator()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
