from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout


class ComboBoxDialog(QDialog):
    def __init__(self, title:str, items:list[str]):
        super().__init__()

        self.title = title
        self.items = items
        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()
        self.setWindowTitle(self.title)

        # Add a label
        label = QLabel('Select an option:')
        layout.addWidget(label)

        # Add a dropdown menu
        self.combo_box = QComboBox()

        for tool in self.items:
            self.combo_box.addItem(tool)
        
        layout.addWidget(self.combo_box)

        buttons_layout = QHBoxLayout()
        # Add a button to close the dialog
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.closeClicked)

        open_button = QPushButton('Ok')
        open_button.clicked.connect(self.okClicked)

        if len(self.items) == 0:
            open_button.setDisabled(True)

        buttons_layout.addWidget(close_button)
        buttons_layout.addWidget(open_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the dialog
        self.setLayout(layout)
    
    def closeClicked(self):
        self.accept()
        self.setResult(QDialog.Rejected)
    
    def okClicked(self):
        self.accept()
    
    def getSelected(self):
        return self.combo_box.currentText()
