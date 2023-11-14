from PyQt6.QtWidgets import QComboBox, QDialog, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QLineEdit

class IATReconstructionDialog(QDialog):
    def __init__(self, tools:list, parent=None):
        super(IATReconstructionDialog, self).__init__(parent)

        self.parent_window = parent
        self.tools = tools
        self.initUI()

    def initUI(self):
        self.setWindowTitle("IAT reconstruct")


        self.oep = QLineEdit(self)
        formLayout = QFormLayout()

        formLayout.addRow('OEP:', self.oep)

        # Add a dropdown menu
        self.combo_box = QComboBox()

        for tool in self.tools:
            self.combo_box.addItem(tool)
        
        formLayout.addRow('Tool:', self.combo_box)
        
        cancelButton = QPushButton('Cancel', self)
        cancelButton.clicked.connect(self.close)

        goButton = QPushButton('Go', self)
        goButton.clicked.connect(self.go)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(cancelButton)
        buttonLayout.addWidget(goButton)

        mainLayout = QVBoxLayout(self)
        mainLayout.addLayout(formLayout)
        mainLayout.addLayout(buttonLayout)
    
    def go(self):
        self.accept()
    
    def closeEvent(self, event) -> None:
        self.accept()
        self.setResult(QDialog.Rejected)
    
    def getOEP(self):
        return self.oep.text()

    def getTool(self):
        return self.combo_box.currentText()
