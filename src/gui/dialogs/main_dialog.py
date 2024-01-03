from PyQt6.QtWidgets import QLabel, QDialog, QPushButton, QVBoxLayout, QHBoxLayout
import qdarktheme


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        qdarktheme.setup_theme('auto')

        self.parent_window = parent
        self.initUI()

        self.new_analysis = False
        self.open_analysis = False

    def initUI(self):
        self.setWindowTitle('VISREX')

        new_analysis_layout = QHBoxLayout()

        new_analysis_label = QLabel("Start a new analysis")
        new_analysis_button = QPushButton('New', self)
        new_analysis_button.setFixedSize(100, 30)
        new_analysis_button.clicked.connect(self.new_analysis_clicked)

        new_analysis_layout.addWidget(new_analysis_button)
        new_analysis_layout.addWidget(new_analysis_label)

        open_analysis_layout = QHBoxLayout()

        open_analysis_label = QLabel("Open a previous analysis")
        open_analysis_button = QPushButton('Open', self)
        open_analysis_button.setFixedSize(100, 30)
        open_analysis_button.clicked.connect(self.open_analysis_clicked)

        open_analysis_layout.addWidget(open_analysis_button)
        open_analysis_layout.addWidget(open_analysis_label)

        layout = QVBoxLayout()
        layout.addLayout(new_analysis_layout)
        layout.addLayout(open_analysis_layout)

        self.setLayout(layout)


    def new_analysis_clicked(self):
        self.new_analysis = True
        self.accept()

    def open_analysis_clicked(self):
        self.open_analysis = True
        self.accept()
        
    def closeEvent(self, event) -> None:
        self.accept()
        self.setResult(QDialog.Rejected)

    def exec_(self) -> int:
        self.new_analysis = False
        self.open_analysis = False
        
        return super().exec() 


