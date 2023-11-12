from PyQt6.QtWidgets import QLabel, QDialog, QPushButton, QVBoxLayout, QFileDialog, QHBoxLayout, QLineEdit
import qdarktheme


class ChoseFileDialog(QDialog):
    def __init__(self, title, file_types, parent=None):
        super(ChoseFileDialog, self).__init__(parent)

        qdarktheme.setup_theme('auto')
        
        self.title = title
        self.file_types = file_types
        self.parent_window = parent
        self.initUI()

        self.file_name = ""

    def initUI(self):
        self.setWindowTitle(self.title)

        self.open_file_layout = QHBoxLayout()

        malware_sample_label = QLabel("File:")
        self.file_path_label = QLineEdit(self)

        open_button = QPushButton('...', self)
        open_button.clicked.connect(self.openFile)

        self.open_file_layout.addWidget(malware_sample_label)
        self.open_file_layout.addWidget(self.file_path_label)
        self.open_file_layout.addWidget(open_button)

        self.go_button = QPushButton('Go', self)
        self.go_button.setDisabled(True)
        self.go_button.clicked.connect(self.goClicked)

        close_button = QPushButton('Close', self)
        close_button.clicked.connect(self.closeClicked)

        # Create a QHBoxLayout for the buttons
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(close_button)
        buttons_layout.addWidget(self.go_button)

        layout = QVBoxLayout()
        layout.addLayout(self.open_file_layout)
        layout.addLayout(buttons_layout)

        self.setLayout(layout)

    def openFile(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly

        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", self.file_types, options=options)

        if file_name:
            self.file_name = file_name
            self.file_path_label.setText(file_name)

            self.go_button.setDisabled(False)

    def goClicked(self):
        # Open the main window with the selected file
        self.accept()  # Close the dialog
    
    def closeClicked(self):
        self.accept()
        self.setResult(QDialog.Rejected)

    def closeEvent(self, event) -> None:
        self.accept()
        self.setResult(QDialog.Rejected)
