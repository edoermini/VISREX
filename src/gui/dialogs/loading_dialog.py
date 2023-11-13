from PyQt6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton, QHBoxLayout
from PyQt6.QtGui import QMovie
from PyQt6.QtCore import Qt, QSize
import os


class LoadingDialog(QDialog):
	def __init__(self, title:str=None, message:str=None):
		super().__init__()

		self.title = title
		self.message_label = QLabel(message)
		self.initUI()

	def initUI(self):
		# Set up the layout
		
		layout = QVBoxLayout()
		
		if self.title:
			self.setWindowTitle(self.title)

		self.spinner_label = QLabel(self)
		self.spinner_label.setFixedSize(100, 100)
		self.spinner_movie = QMovie(os.path.abspath("gui/assets/loading.gif"))
		self.spinner_movie.setScaledSize(QSize(95, 95))
		self.spinner_label.setMovie(self.spinner_movie)
		self.spinner_movie.start()
		self.spinner_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		layout.addWidget(self.spinner_label)

		self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

		layout.addWidget(self.message_label)

		layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

		# Set the layout for the dialog
		self.setLayout(layout)
	
	def setMessage(self, message):
		self.message_label.setText(message)