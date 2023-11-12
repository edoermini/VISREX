from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout


class OpenToolDialog(QDialog):
    def __init__(self, tools:list[str]):
        super().__init__()

        self.tools = tools
        self.initUI()

    def initUI(self):
        # Set up the layout
        layout = QVBoxLayout()

        # Add a label
        label = QLabel('Select an option:')
        layout.addWidget(label)

        # Add a dropdown menu
        self.combo_box = QComboBox()

        for tool in self.tools:
            self.combo_box.addItem(tool)
        
        layout.addWidget(self.combo_box)

        buttons_layout = QHBoxLayout()
        # Add a button to close the dialog
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.closeClicked)

        open_button = QPushButton('Open')
        open_button.clicked.connect(self.openClicked)

        buttons_layout.addWidget(close_button)
        buttons_layout.addWidget(open_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the dialog
        self.setLayout(layout)
    
    def closeClicked(self):
        self.accept()
        self.setResult(QDialog.Rejected)
    
    def openClicked(self):
        self.accept()
    
    def getSelected(self):
        return self.combo_box.currentText()
