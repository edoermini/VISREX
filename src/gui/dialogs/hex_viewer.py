from PyQt5.QtWidgets import QWidget, QTextEdit, QDialog, QVBoxLayout, QSplitter, QAction, QFileDialog, QHBoxLayout, QLabel, QComboBox, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextOption, QFont
import binascii

class HexViewer(QDialog):
    def __init__(self, title, byte_data, parent=None):
        super(HexViewer, self).__init__(parent)
        self.title = title
        self.byte_data = byte_data
        self.bytes_per_row = 16
        self.parent_window = parent
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()

        splitter = QSplitter(Qt.Horizontal)

        self.hex_view = QTextEdit()
        self.hex_view.setReadOnly(True)
        self.hex_view.setWordWrapMode(QTextOption.NoWrap)
        self.hex_view.setFont(QFont('Courier'))

        
        self.ascii_view = QTextEdit()
        self.ascii_view.setReadOnly(True)
        self.ascii_view.setWordWrapMode(QTextOption.NoWrap)
        self.ascii_view.setFont(QFont('Courier'))

        self.hex_view_scroll_bar = self.hex_view.verticalScrollBar()
        self.ascii_view_scroll_bar = self.ascii_view.verticalScrollBar()

        self.hex_view_scroll_bar.valueChanged.connect(self.sync_scroll)
        self.ascii_view_scroll_bar.valueChanged.connect(self.sync_scroll)

        splitter.addWidget(self.hex_view)
        splitter.addWidget(self.ascii_view)

        layout.addWidget(splitter)

        bottom_menu_widget = QWidget()
        bottom_menu_widget.setFixedHeight(100)
        bottom_menu_layout = QHBoxLayout(bottom_menu_widget)

        self.bytes_per_row_combo = QComboBox(self)
        self.bytes_per_row_combo.addItem("4 bytes per row")
        self.bytes_per_row_combo.addItem("8 bytes per row")
        self.bytes_per_row_combo.addItem("16 bytes per row")
        self.bytes_per_row_combo.addItem("32 bytes per row")
        self.bytes_per_row_combo.addItem("64 bytes per row")
        self.bytes_per_row_combo.addItem("128 bytes per row")
        self.bytes_per_row_combo.addItem("256 bytes per row")

        self.bytes_per_row_combo.setCurrentIndex(2)
        self.bytes_per_row_combo.currentIndexChanged.connect(self.change_bytes_per_row)
        
        bottom_menu_layout.addWidget(self.bytes_per_row_combo)

        self.save_button = QPushButton()
        self.save_button.setText('Save')
        self.save_button.clicked.connect(lambda x : self.save_file())

        bottom_menu_layout.addWidget(self.save_button)

        layout.addWidget(bottom_menu_widget)

        self.setLayout(layout)

        self.fill_views()

    def _divide_chunks(self, l, n):
      
        # looping till length l
        for i in range(0, len(l), n):
            yield l[i:i + n]

    def change_bytes_per_row(self, index):
        self.bytes_per_row = 2**index * 4
        self.fill_views()

    def fill_views(self):
        self.hex_view.clear()
        self.ascii_view.clear()

        for chunk in self._divide_chunks(self.byte_data, self.bytes_per_row):
            self.hex_view.append(' '.join(list(self._divide_chunks(binascii.hexlify(chunk).decode('utf-8'), 2))))
            self.ascii_view.append(''.join(chr(b) if 32 <= b <= 127 else '.' for b in chunk))
    
    def sync_scroll(self):
        value = self.sender().value()

        if self.sender() == self.hex_view_scroll_bar:
            self.ascii_view_scroll_bar.setValue(value)
        else:
            self.hex_view_scroll_bar.setValue(value)

    def save_file(self):
        options = QFileDialog.Options()
        file_types = "Binary Files (*.bin);;Executable Files (*.exe);;Text Files (*.txt);;All Files (*)"

        file_name, _ = QFileDialog.getSaveFileName(self, "Save File", "", file_types, options=options)
        if file_name:
            with open(file_name, 'wb') as file:
                file.write(self.byte_data)