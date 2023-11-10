from PyQt6.QtWidgets import QApplication, QMenu, QStatusBar, QToolBar, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QTableWidgetItem, QFileDialog, QDialog, QLabel, QSpacerItem, QSizePolicy, QHBoxLayout
from PyQt6.QtCore import Qt, QSize, QTimer, QThread
from PyQt6.QtGui import QColor, QMovie, QAction, QActionGroup, QPalette
import qtawesome as qta
import qdarktheme
import os
from datetime import datetime
import pickle
from time import time
from functools import partial

from gui.updaters import ActivityUpdater
from gui.dialogs import ReadProcessMemoryDialog, OpenToolDialog
from gui.flowcharts import GraphvizFlowchart
from gui.tables import ResponsiveTableWidget
from gui.threads import ExecutablesUpdaterThread
from gui.shared import StatusMessagesQueue

from analysis import Analysis

class MainWindow(QMainWindow):
	def __init__(self, malware_sample=None, analysis_file=None):
		super(MainWindow, self).__init__()

		self.malware_sample = malware_sample
		self.analysis_file = analysis_file
		self.messages = StatusMessagesQueue()
		self.analysis = None

		if self.malware_sample is not None:
			self.malware_sample = os.path.basename(self.malware_sample)
			self.analysis = Analysis(self.malware_sample)
		
		else:
			with open(self.analysis_file, "rb") as file:
				self.analysis = pickle.load(file)
		
		self.initUI()
		self.setTheme('auto')

	def initUI(self):
		self.setWindowTitle("MASup (Malware Analysis Supporter)")

		# Creare un widget a pila per le diverse viste
		stacked_widget = QStackedWidget()

		self.progress_view = GraphvizFlowchart(self.analysis.workflow.dot_code(), QColor('#fffff') if self.isDarkThemeActive() else QColor('#00000'))
		self.progress_view.signals.rightClick.connect(self.openFlowchartNodeContextMenu)
		self.progress_view.setOpacity(0.2)

		progress_page = QWidget()
		progress_page_layout = QVBoxLayout(progress_page)
		progress_page_layout.addWidget(self.progress_view)
		stacked_widget.addWidget(progress_page)

		self.activity_log_table = ResponsiveTableWidget(0, ['Time', 'Activity', 'Tool', 'Executable', 'Arguments'], self)
		activity_log_page = QWidget()
		activity_log_page_layout = QVBoxLayout(activity_log_page)
		activity_log_page_layout.addWidget(self.activity_log_table)
		stacked_widget.addWidget(activity_log_page)

		self.setCentralWidget(stacked_widget)

		self.toolbar = QToolBar("Toolbar", self)
		self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
		
		self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

		toolbar_actions = QActionGroup(self)
		toolbar_actions.setExclusive(True)

		self.progress_page_button = QAction(qta.icon("fa5s.tasks"), "Progress", self)
		self.progress_page_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(0))
		self.progress_page_button.setCheckable(True)
		self.progress_page_button.setChecked(True)
		toolbar_actions.addAction(self.progress_page_button)
		self.toolbar.addAction(self.progress_page_button)

		self.activity_log_page_button = QAction(qta.icon("fa5s.history"), "Activity log", self)
		self.activity_log_page_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(1))
		self.activity_log_page_button.setCheckable(True)
		self.activity_log_page_button.setChecked(False)
		toolbar_actions.addAction(self.activity_log_page_button)
		self.toolbar.addAction(self.activity_log_page_button)

		self.toolbar.addSeparator()

		self.read_process_memory_button = QAction(qta.icon("fa5s.syringe"), "Read process memory", self)
		self.read_process_memory_button.triggered.connect(self.readProcessMemory)
		self.read_process_memory_button.setCheckable(False)
		toolbar_actions.addAction(self.read_process_memory_button)
		self.toolbar.addAction(self.read_process_memory_button)

		self.setStatusBar(QStatusBar(self))

		menubar = self.menuBar()
		file_menu = menubar.addMenu('File')

		save_action = QAction('Save', self)
		save_action.triggered.connect(self.saveFile)
		file_menu.addAction(save_action)

		save_with_name_action = QAction('Save with name', self)
		save_with_name_action.triggered.connect(self.saveWithName)
		file_menu.addAction(save_with_name_action)

		load_action = QAction('Open analysis', self)
		load_action.triggered.connect(self.openFile)
		file_menu.addAction(load_action)

		exit_action = QAction('Quit', self)
		exit_action.triggered.connect(self.close)
		file_menu.addAction(exit_action)

		view_menu = menubar.addMenu('View')

		show_toolbar_action = QAction('Show toolbar', self, checkable=True)
		show_toolbar_action.setChecked(True)
		show_toolbar_action.triggered.connect(self.toolbar.setVisible)
		view_menu.addAction(show_toolbar_action)

		appearance_submenu = QMenu('Appearance', self)
		theme_menu = QMenu('Theme', self)

		appearance_submenu.addMenu(theme_menu)

		theme_action_group = QActionGroup(self)
		theme_action_group.setExclusive(True)

		self.dark_mode_action = QAction('Dark', self, checkable=True)
		self.dark_mode_action.triggered.connect(partial(self.setTheme, 'dark'))
		theme_action_group.addAction(self.dark_mode_action)
		theme_menu.addAction(self.dark_mode_action)

		self.light_mode_action = QAction('Light', self, checkable=True)
		self.light_mode_action.triggered.connect(partial(self.setTheme, 'light'))
		theme_action_group.addAction(self.light_mode_action)
		theme_menu.addAction(self.light_mode_action)

		self.system_mode_action = QAction('Auto', self, checkable=True)
		self.system_mode_action.triggered.connect(partial(self.setTheme, 'auto'))
		theme_action_group.addAction(self.system_mode_action)
		theme_menu.addAction(self.system_mode_action)

		view_menu.addMenu(appearance_submenu)

		options_menu = menubar.addMenu('Options')
		update_tools_exec_action = QAction('Update tools executables', self)
		update_tools_exec_action.triggered.connect(self.executablesFinderStart)
		options_menu.addAction(update_tools_exec_action)


		layout = QVBoxLayout()
		layout.addWidget(stacked_widget)

		# Creare un widget principale e impostare il layout principale
		main_widget = QWidget()
		main_widget.setLayout(layout)

		# Impostare il widget principale come widget centrale della finestra principale
		self.setCentralWidget(main_widget)

		self.spinner_label = QLabel(self)
		self.spinner_label.setFixedSize(25, 25)
		self.spinner_movie = QMovie(os.path.abspath("gui/assets/loading.gif"))
		self.spinner_movie.setScaledSize(QSize(20, 20))
		self.spinner_label.setMovie(self.spinner_movie)
		self.spinner_movie.start()
		self.spinner_label.hide()

		self.statusBar().addPermanentWidget(self.spinner_label)

		self.timer = QTimer(self)
		self.timer.timeout.connect(self.updateStatus)
		self.timer.start(2000)  # Switch messages every 2000 milliseconds

		self.activity_updater = ActivityUpdater(self.analysis, 500)
		self.activity_updater.dataUpdated.connect(self.updateProgress)

		self.executablesFinderStart()
	
	def updateStatus(self):
		# Display the next message in the list

		message = self.messages.get_message_rotation()

		if message is None:
			if not self.spinner_label.isHidden():
				self.spinner_label.hide()
				self.statusBar().clearMessage()
			
			return
		
		if self.spinner_label.isHidden():
			self.spinner_label.show()

		self.statusBar().showMessage(message)
		
	def updateProgress(self):
		self.analysis.update_activities()

		for node_id in self.analysis.activities:
			self.progress_view.setOpacity(1, node_id)
		
		for row, log in enumerate(self.analysis.activity_log):

			if row == self.activity_log_table.rowCount():
				self.activity_log_table.insertRow(row)
			
			columns = [datetime.fromtimestamp(log['time']).isoformat(), log['activity'], log['tool'], log['executable'], ' '.join(log['arguments'])]

			for col, value in enumerate(columns):
				item = QTableWidgetItem(value)
				self.activity_log_table.setItem(row, col, item)

	def executablesFinderStart(self):
		message_index = self.messages.add('Looking for executables')

		executables_finder_thread = ExecutablesUpdaterThread(self.analysis)
		executables_finder_thread.finished.connect(partial(self.executablesFinderFinish, message_index, executables_finder_thread))
		executables_finder_thread.start()

	def executablesFinderFinish(self, message_index:int, thread:QThread):
		self.messages.remove(message_index)
		thread.terminate()

	def saveFile(self):

		if not self.analysis_file:
			self.saveWithName()
			return
		
		self.analysis.export_analysis(self.analysis_file)

	def saveWithName(self):
		file_path, _ = QFileDialog.getSaveFileName(self, "Save Object", "", "Malware Analysis Supporter Files (*.masup)")
		if file_path:
			self.analysis_file = file_path
			self.analysis.export_analysis(self.analysis_file)

	def openFile(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Load Object", "", "Malware Analysis Supporter Files (*.masup)")
		if file_path:
			with open(file_path, "rb") as file:
				self.analysis = pickle.load(file)
	
	def readProcessMemory(self):
		read_process_memory = ReadProcessMemoryDialog(self)
		result = read_process_memory.exec_()

		if result == QDialog.Accepted:

			self.analysis.update_activity_log([{
				"time":time(), 
				"activity":"Read process memory", 
				"tool": "", 
				"executable":"", 
				"arguments":[f"{read_process_memory.getProcessName()}, {read_process_memory.getStartAddress()}, {read_process_memory.getBytesLength()}",]
			}])

	def closeEvent(self, event):
		self.activity_updater.stop()
		event.accept()
	
	def setTheme(self, theme:str):
		
		if theme == 'auto':
			self.system_mode_action.setChecked(True)
		elif theme == 'dark':
			self.dark_mode_action.setChecked(True)
		else: # theme == 'light'
			self.light_mode_action.setChecked(True)

		qdarktheme.setup_theme(theme)
		self.progress_view.setEdgesColor(QColor('#ffffff') if self.isDarkThemeActive() else QColor('#000000'))
		self.progress_page_button.setIcon(qta.icon("fa5s.tasks", color="white" if self.isDarkThemeActive() else "black"))
		self.activity_log_page_button.setIcon(qta.icon("fa5s.history", color="white" if self.isDarkThemeActive() else "black"))
		self.read_process_memory_button.setIcon(qta.icon("fa5s.syringe", color="white" if self.isDarkThemeActive() else "black"))

	def openFlowchartNodeContextMenu(self, node_id, mouse_pos):
		context_menu = QMenu(self)
		action = context_menu.addAction("Launch tool")
		action.triggered.connect(partial(self.openTool, node_id))
		context_menu.exec_(mouse_pos)
	
	def openTool(self, node_id):
		tools = [tool for tool in self.analysis.workflow['workflow']['nodes'][node_id]['tools'] if tool in self.analysis.executables]
		dialog = OpenToolDialog(tools)
		dialog.setMinimumWidth(200)
		dialog.exec_()
	
	def isDarkThemeActive(self):

		# Check the color role for the WindowText color
		background_color = self.palette().color(self.backgroundRole())

		# Calculate the overall brightness of the color
		brightness = (background_color.red() * 299 + background_color.green() * 587 + background_color.blue() * 114) / 1000

		# If the brightness is less than a threshold, consider it a dark theme
		return brightness < 128

	def close(self) -> bool:
		return super().close()