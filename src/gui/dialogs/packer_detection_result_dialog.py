from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout


class PackerDetectionResultDialog(QDialog):
    def __init__(self, found, packer:str= ""):
        super().__init__()

        self.found = found
        self.packer = packer
        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()
        self.setWindowTitle("Packer Detection Result")

        # Add a label
        if self.found:
            label = QLabel('Packer found:')
            packer_label = QLabel(self.packer)
            layout.addWidget(label)
            layout.addWidget(packer_label)
        else:
            label = QLabel('Packer not found!')
            layout.addWidget(label)

        buttons_layout = QHBoxLayout()
        # Add a button to close the dialog

        ok_button = QPushButton('Ok')
        ok_button.clicked.connect(self.okClicked)

        unpack_button = QPushButton('Unpack')
        unpack_button.clicked.connect(self.unpackClicked)

        if not self.found:
            unpack_button.setDisabled(True)

        buttons_layout.addWidget(ok_button)
        buttons_layout.addWidget(unpack_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the dialog
        self.setLayout(layout)
    
    def okClicked(self):
        self.accept()
        self.setResult(QDialog.Rejected)
    
    def unpackClicked(self):
        self.accept()