from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QPushButton, QHBoxLayout, QSplitter, QToolBar
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QAction

import markdown
import qtawesome as qta

class TextBoxDialog(QDialog):
    def __init__(self, title:str, text:str, dark_mode:bool):
        super().__init__()

        self.title = title
        self.dark_mode = dark_mode
        self.text = text
        self.initUI()

    def initUI(self):
        
        self.setWindowTitle(self.title)
        
        layout = QVBoxLayout()


        toolbar = QToolBar(self)
        edit_action = QAction(qta.icon("fa5s.edit", color="white" if self.dark_mode else "black"), "Edit", self, checkable=True)
        edit_action.triggered.connect(self.show_markdown_edit)
        toolbar.addAction(edit_action)

        layout.addWidget(toolbar)

        splitter = QSplitter(Qt.Horizontal)

        self.markdown_edit = QTextEdit(self)
        self.markdown_edit.setText(self.text)
        self.markdown_edit.hide()
        splitter.addWidget(self.markdown_edit)

        self.markdown_view = QTextEdit(self)
        self.markdown_view.setReadOnly(True)
        splitter.addWidget(self.markdown_view)

        layout.addWidget(splitter)

        self.setLayout(layout)

        self.markdown_edit.textChanged.connect(self.update_preview)

        buttons_layout = QHBoxLayout()


        # Add a button to close the dialog
        close_button = QPushButton('Close')
        close_button.clicked.connect(self.closeClicked)

        open_button = QPushButton('Ok')
        open_button.clicked.connect(self.okClicked)

        buttons_layout.addWidget(close_button)
        buttons_layout.addWidget(open_button)

        layout.addLayout(buttons_layout)

        # Set the layout for the dialog
        self.setLayout(layout)

        self.update_preview()
    
    def show_markdown_edit(self, active):
        if active:
            self.markdown_edit.show()
        else:
            self.markdown_edit.hide()

    def update_preview(self):
        markdown_text = self.markdown_edit.toPlainText()
        html = markdown.markdown(markdown_text)
        self.markdown_view.setHtml(html)

    def closeClicked(self):
        self.accept()
        self.setResult(QDialog.Rejected)
    
    def okClicked(self):
        self.accept()
    
    def getText(self):
        return self.markdown_edit.toPlainText()
