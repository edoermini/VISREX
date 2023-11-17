from PyQt6.QtWidgets import QWidget, QToolBar, QVBoxLayout, QSplitter, QTextEdit
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal
import qtawesome as qta
import markdown
from gui.utils import isDarkThemeActive

class MardownEdit(QWidget):
    textUpdated = pyqtSignal(str)

    def __init__(self, dark_mode:bool):
        super().__init__()

        self.dark_mode = dark_mode
    
        toolbar = QToolBar(self)
        self.edit_action = QAction(qta.icon("fa5s.edit", color="white" if self.dark_mode else "black"), "Edit", self, checkable=True)
        self.edit_action.triggered.connect(self.show_markdown_edit)
        toolbar.addAction(self.edit_action)

        splitter = QSplitter(Qt.Horizontal)

        self.markdown_edit = QTextEdit(self)
        self.markdown_edit.setPlaceholderText('Write your markdown notes here')
        self.markdown_edit.hide()
        self.markdown_edit.textChanged.connect(self.text_changed)
        splitter.addWidget(self.markdown_edit)

        self.markdown_view = QTextEdit(self)
        self.markdown_view.setPlaceholderText('Your notes will be shown here')
        self.markdown_view.setReadOnly(True)
        splitter.addWidget(self.markdown_view)

        layout = QVBoxLayout()
        layout.addWidget(toolbar)
        layout.addWidget(splitter)
        
        self.setLayout(layout)
    
    def show_markdown_edit(self, active):

        if active:
            self.markdown_edit.show()
        else:
            self.markdown_edit.hide()

    def text_changed(self):
        self.textUpdated.emit(self.markdown_edit.toPlainText())
        self._update_preview()

    def _update_preview(self):
        markdown_text = self.markdown_edit.toPlainText()
        html = markdown.markdown(markdown_text)
        self.markdown_view.setHtml(html)
    
    def setText(self, text:str):
        self.markdown_edit.setText = text
    
    def setDarkMode(self, dark_mode):
        self.dark_mode = dark_mode
        self.edit_action.setIcon(qta.icon("fa5s.edit", color="white" if dark_mode else "black"))