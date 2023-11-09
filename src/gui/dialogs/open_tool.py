from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton


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
        combo_box = QComboBox()

        for tool in self.tools:
            combo_box.addItem(tool)
        
        layout.addWidget(combo_box)

        # Add a button to close the dialog
        close_button = QPushButton('Close Dialog')
        close_button.clicked.connect(self.accept)
        layout.addWidget(close_button)

        # Set the layout for the dialog
        self.setLayout(layout)
