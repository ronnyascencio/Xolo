import sys
from PySide2 import QtWidgets, QtGui

class SequenceShotCreator(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Sequence and Shot Creator')
        layout = QtWidgets.QVBoxLayout()

        # File import section
        self.file_label = QtWidgets.QLabel('Drop EDL/XML file here or click to select:')
        self.file_display = QtWidgets.QLabel()
        self.file_display.setFixedHeight(100)
        self.file_display.setFrameStyle(QtWidgets.QFrame.Box)
        self.file_display.setAcceptDrops(True)
        self.file_display.dragEnterEvent = self.drag_enter_event
        self.file_display.dropEvent = self.drop_event

        self.btn_select_file = QtWidgets.QPushButton('Select File')
        self.btn_select_file.clicked.connect(self.select_file)

        self.btn_process_file = QtWidgets.QPushButton('Process File')
        self.btn_process_file.clicked.connect(self.process_file)

        layout.addWidget(self.file_label)
        layout.addWidget(self.file_display)
        layout.addWidget(self.btn_select_file)
        layout.addWidget(self.btn_process_file)

        self.setLayout(layout)

    def drag_enter_event(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def drop_event(self, event):
        file_path = event.mimeData().urls()[0].toLocalFile()
        self.file_display.setText(file_path)
        self.file_path = file_path

    def select_file(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Select EDL/XML file", "", "EDL/XML Files (*.edl *.xml)")
        if file_path:
            self.file_display.setText(file_path)
            self.file_path = file_path

    def process_file(self):
        if hasattr(self, 'file_path'):
            self.parse_file(self.file_path)
        else:
            QtWidgets.QMessageBox.warning(self, "No file selected", "Please select an EDL/XML file to process.")

    def parse_file(self, file_path):
        # Implement parsing logic here
        # For now, just a placeholder
        QtWidgets.QMessageBox.information(self, "File Processed", f"File '{file_path}' processed successfully.")

def main():
    app = QtWidgets.QApplication(sys.argv)
    main_widget = SequenceShotCreator()
    main_widget.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
