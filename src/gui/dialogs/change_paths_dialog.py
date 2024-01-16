from PyQt6.QtWidgets import QLineEdit, QDialog, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QFileDialog, QMessageBox
import qtawesome as qta
import os
import pathlib


class ChangePathsDialog(QDialog):
    def __init__(self, paths:list[str], dark_mode, parent=None):
        super(ChangePathsDialog, self).__init__(parent)
        self.paths = paths
        self.dark_mode = dark_mode
        self.path_labels : list[QLabel]= []
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Check malware paths")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Change to the directory that should contain at least the first malware samples loaded"))

        for path in self.paths:
            path_label = QLineEdit(os.path.basename(str(pathlib.Path(path))))
            path_label.setReadOnly(True)
            layout.addWidget(path_label)
            self.path_labels.append(path_label)
        
        buttons_layout = QHBoxLayout()

        choose_button = QPushButton(qta.icon('fa.folder-open', color="white" if self.dark_mode else "black"), "Change directory")
        choose_button.clicked.connect(self.chooseDirectory)

        ok_button = QPushButton('Ok', self)
        ok_button.clicked.connect(self.okClicked)

        buttons_layout.addWidget(choose_button)
        buttons_layout.addWidget(ok_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)
    
    def chooseDirectory(self):
        # Implement your logic for choosing a directory here
        directory = QFileDialog.getExistingDirectory(self, "Choose Directory")
        if directory:
            if any([os.path.exists(os.path.join(directory, os.path.basename(path))) for path in self.paths]):
                for i, path in enumerate(self.paths):
                    new_path = str(pathlib.Path(os.path.join(directory, os.path.basename(path))))
                    self.paths[i] = new_path
                    self.path_labels[i].setText(new_path)
            
            else:
                error_dialog = QMessageBox(self)
                error_dialog.setIcon(QMessageBox.Critical)
                error_dialog.setWindowTitle("Error")
                error_dialog.setText(f"Chose the directory containing at least the initial malware sample")
                error_dialog.exec_()

    def okClicked(self):
        if any([os.path.exists(path) for path in self.paths]):
            self.accept()
        else:
            error_dialog = QMessageBox(self)
            error_dialog.setIcon(QMessageBox.Critical)
            error_dialog.setWindowTitle("Error")
            error_dialog.setText(f"Chose the directory containing at least the initial malware sample")
            error_dialog.exec_()
    
    def getPaths(self) -> list[str]:
        return self.paths
    
