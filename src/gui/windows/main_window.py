from PyQt6.QtWidgets import QMenu, QStatusBar, QToolBar, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QTableWidgetItem, QFileDialog, QDialog, QLabel, QTextEdit
from PyQt6.QtCore import Qt, QSize, QTimer, QThread
from PyQt6.QtGui import QMovie, QAction, QActionGroup
import qtawesome as qta
import qdarktheme
import os
import pickle
from time import time
from functools import partial
import subprocess
import platform
import markdown

from gui.updaters import ActivityUpdater, ExecutablesUpdater
from gui.dialogs import ReadProcessMemoryDialog, ComboBoxDialog, ToolsCoverageDialog, IATReconstructionDialog, TextBoxDialog
from gui.flowcharts import GraphvizFlowchart
from gui.tables import ResponsiveTableWidget
from gui.shared import StatusMessagesQueue

from analysis import Analysis, AnalysisLogEntry


if platform.system() == "Windows":
	from masup.tools import Scylla


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

		# flowchart page
		self.flowchart = GraphvizFlowchart(self.analysis.workflow.dot_code(), Qt.white if self.isDarkThemeActive() else Qt.black)
		self.flowchart.signals.rightClick.connect(self.openFlowchartNodeContextMenu)
		self.flowchart.setOpacity(0.3)
		self.flowchart.setProgressPercentage(0)

		flowchart_page = QWidget()
		flowchart_page_layout = QVBoxLayout(flowchart_page)
		flowchart_page_layout.addWidget(self.flowchart)

		# activity log page
		self.activity_log_table = ResponsiveTableWidget(0, [], self)
		activity_log_page = QWidget()
		activity_log_page_layout = QVBoxLayout(activity_log_page)
		activity_log_page_layout.addWidget(self.activity_log_table)
		self.activity_log_table.doubleClicked.connect(self.activity_log_table_double_click)

		stacked_widget.addWidget(flowchart_page)
		stacked_widget.addWidget(activity_log_page)

		self.setCentralWidget(stacked_widget)

		# toolbar

		self.toolbar = QToolBar("Toolbar", self)
		self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
		
		self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

		toolbar_actions = QActionGroup(self)
		toolbar_actions.setExclusive(True)

		self.progress_page_button = QAction(qta.icon("fa5s.project-diagram"), "Progress", self)
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

		self.read_process_memory_button = QAction(qta.icon("fa5s.syringe", color="white" if self.isDarkThemeActive() else "black"), "Read process memory", self)
		self.read_process_memory_button.triggered.connect(self.readProcessMemory)
		self.read_process_memory_button.setCheckable(False)
		self.toolbar.addAction(self.read_process_memory_button)

		self.iat_reconstruction_button = QAction(qta.icon("fa5s.tools", color="white" if self.isDarkThemeActive() else "black"), "Unpack", self)
		self.iat_reconstruction_button.triggered.connect(self.iatReconstruct)
		self.iat_reconstruction_button.setCheckable(False)
		self.toolbar.addAction(self.iat_reconstruction_button)

		self.unpack_button = QAction(qta.icon("fa5s.box-open", color="white" if self.isDarkThemeActive() else "black"), "Unpack", self)
		self.unpack_button.triggered.connect(self.unpack)
		self.unpack_button.setCheckable(False)
		self.toolbar.addAction(self.unpack_button)

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

		file_menu.addSeparator()

		export_flowchat_svg_action = QAction('Export Flowchart SVG', self)
		export_flowchat_svg_action.triggered.connect(self.exportSVG)
		file_menu.addAction(export_flowchat_svg_action)

		export_flowchat_svg_action = QAction('Export Flowchart PNG', self)
		export_flowchat_svg_action.triggered.connect(self.exportPNG)
		file_menu.addAction(export_flowchat_svg_action)

		file_menu.addSeparator()

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

		# status bar 

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
		self.activity_updater.dataUpdated.connect(self.updateAnalysisProgress)
		self.activity_updater.start()
		
		self.executablesFinderStart()
	
	def exportSVG(self):
		file_path, _ = QFileDialog.getSaveFileName(self, "Save as SVG", "", "SVG Files (*.svg)")
		if file_path:
			self.flowchart.exportSVG(file_path)
	
	def exportPNG(self):
		file_path, _ = QFileDialog.getSaveFileName(self, "Save as PNG", "", "PNG Files (*.png)")
		if file_path:
			self.flowchart.exportSVG(file_path)

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
		
	def updateAnalysisProgress(self):
		
		last_row = 0#self.activity_log_table.rowCount()

		for node_id in self.analysis.activities:
			self.flowchart.setOpacity(1, node_id)

		for i, log_entry in enumerate(self.analysis.get_activity_log(last_row)):
			row = last_row + i
			columns = log_entry.to_json(string_values=True)
			column_count = len(columns)

			if row == self.activity_log_table.rowCount():
				self.activity_log_table.insertRow(row)
			
			if column_count > self.activity_log_table.columnCount():
				self.activity_log_table.setColumnCount(column_count)
				self.activity_log_table.setHorizontalHeaderLabels(columns.keys())

			for col, (_, value) in enumerate(columns.items()):

				if self.activity_log_table.horizontalHeaderItem(col).text() == 'notes':
					html_value = markdown.markdown(value)
					markdown_view = QTextEdit()
					markdown_view.setReadOnly(True)
					markdown_view.setHtml(html_value)

					self.activity_log_table.setCellWidget(row, col, markdown_view)
				else:
					self.activity_log_table.setItem(row, col, QTableWidgetItem(value))

	def executablesFinderStart(self):
		message_index = self.messages.add('Looking for executables')
		executables_finder_thread = ExecutablesUpdater(self.analysis)
		executables_finder_thread.executableFound.connect(self.updateToolsCoverage)
		executables_finder_thread.finished.connect(partial(self.executablesFinderFinish, message_index, executables_finder_thread))
		executables_finder_thread.start()

	def executablesFinderFinish(self, message_index:int, thread:QThread):
		self.messages.remove(message_index)
		thread.terminate()

	def updateToolsCoverage(self):
		nodes_ids = self.analysis.workflow.get_nodes_ids()

		for node_id in nodes_ids:

			tools = self.analysis.get_tools(node_id)
			installed_tools = self.analysis.get_installed_tools(node_id)
			
			if len(tools) > 0:
				self.flowchart.setProgressPercentage(len(installed_tools)/len(tools), node_id)

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

			self.analysis.update_activity_log(
				AnalysisLogEntry(
					"",
					"Read process memory",
					"",
					[f"{read_process_memory.getProcessName()}, {read_process_memory.getStartAddress()}, {read_process_memory.getBytesLength()}"],
					"",
					time()
				)
				
			)
		
	def unpack(self):
		print('unpacking...')
	
	def iatReconstruct(self):
		tools = self.analysis.get_installed_tools('impt_1')
		
		iat_reconstruction_dialog = IATReconstructionDialog(tools, self)
		iat_reconstruction_dialog.setMinimumWidth(300)
		iat_reconstruction_dialog_result = QDialog.Accepted
		executable_dialog_result = QDialog.Rejected

		while iat_reconstruction_dialog_result == QDialog.Accepted and executable_dialog_result == QDialog.Rejected:
			iat_reconstruction_dialog_result = iat_reconstruction_dialog.exec_()

			if iat_reconstruction_dialog_result == QDialog.Accepted:
				tool = iat_reconstruction_dialog.getTool()
				oep = iat_reconstruction_dialog.getOEP()

				executable_dialog = ComboBoxDialog('Chose executable', self.analysis.get_executable(tool))
				executable_dialog_result = executable_dialog.exec_()

				if executable_dialog_result == QDialog.Accepted:

					if tool == 'scylla':
						scylla = Scylla(executable_dialog.getSelected())
						scylla.run()
						scylla.attach_to_process(self.analysis.malware_sample)
						scylla.set_oep(oep)
						scylla.iat_autosearch()
						scylla.get_imports()
					
					else:
						break

				print(f"{iat_reconstruction_dialog.getOEP()}, {iat_reconstruction_dialog.getTool()}")

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
		self.flowchart.setEdgesColor(Qt.white if self.isDarkThemeActive() else Qt.black)
		self.progress_page_button.setIcon(qta.icon("fa5s.project-diagram", color="white" if self.isDarkThemeActive() else "black"))
		self.unpack_button.setIcon(qta.icon("fa5s.box-open", color="white" if self.isDarkThemeActive() else "black"))
		self.iat_reconstruction_button.setIcon(qta.icon("fa5s.tools", color="white" if self.isDarkThemeActive() else "black"))
		self.activity_log_page_button.setIcon(qta.icon("fa5s.history", color="white" if self.isDarkThemeActive() else "black"))
		self.read_process_memory_button.setIcon(qta.icon("fa5s.syringe", color="white" if self.isDarkThemeActive() else "black"))

	def openFlowchartNodeContextMenu(self, node_id, mouse_pos):
		context_menu = QMenu(self)
		
		launch_tool_action = context_menu.addAction("Launch tool")
		launch_tool_action.triggered.connect(partial(self.openTool, node_id))
		
		show_tools_coverage_action = context_menu.addAction("Show tools coverage")
		show_tools_coverage_action.triggered.connect(partial(self.showToolsCoverage, node_id))

		automatize_menu = QMenu("Automatize")

		if node_id == 'impt_1':
			context_menu.addMenu(automatize_menu)

			iat_reconstruct_action = QAction("IAT reconstruction")
			iat_reconstruct_action.triggered.connect(self.iatReconstruct)
			automatize_menu.addAction(iat_reconstruct_action)

			context_menu.addMenu(automatize_menu)
		
		if node_id == 'bhvr_3':
			context_menu.addMenu(automatize_menu)

			inspect_process_memory_action = QAction("Inspect process memory")
			inspect_process_memory_action.triggered.connect(self.readProcessMemory)
			automatize_menu.addAction(inspect_process_memory_action)

			context_menu.addMenu(automatize_menu)
		
		context_menu.exec_(mouse_pos)
	
	def showToolsCoverage(self, node_id):
		executables = self.analysis.get_executables()

		coverage = {}
		for tool in self.analysis.workflow['workflow']['nodes'][node_id]['tools']:
			coverage[tool] = tool in executables

		tools_coverage_dialog = ToolsCoverageDialog(coverage, self.isDarkThemeActive())
		tools_coverage_dialog.exec_()

	def openTool(self, node_id):
		executables = self.analysis.get_executables()

		tools = [tool for tool in self.analysis.workflow['workflow']['nodes'][node_id]['tools'] if tool in executables]
		select_tool_dialog = ComboBoxDialog("Select tool", tools)
		select_tool_dialog.setMinimumWidth(300)
		select_tool_dialog_result = QDialog.Accepted
		select_executable_dialog_result = QDialog.Rejected

		while select_tool_dialog_result == QDialog.Accepted and select_executable_dialog_result == QDialog.Rejected:

			select_tool_dialog_result = select_tool_dialog.exec_()

			if select_tool_dialog_result == QDialog.Accepted:
				tool = select_tool_dialog.getSelected()

				select_executable_dialog = ComboBoxDialog("Select executable", executables[tool])
				select_executable_dialog_result = select_executable_dialog.exec_()
				
				if select_executable_dialog_result == QDialog.Accepted:

					executable = select_executable_dialog.getSelected()

					if self.analysis.workflow['tools'][tool]['nature'] == 'GUI' or self.analysis.workflow['tools'][tool]['nature'] == 'CLI-GUI':
						
						subprocess.Popen(executable)
					else:
						if platform.system() == "Windows":
							subprocess.Popen(["start", "cmd", "/k", executable], shell=True, close_fds=True, start_new_session=True)
						elif platform.system() == "Linux":
							subprocess.Popen(["x-terminal-emulator", "-e", executable], shell=True, close_fds=True, start_new_session=True)
	
	def activity_log_table_double_click(self, item):
		row = item.row()
		col = item.column()
	
		col_header = self.activity_log_table.horizontalHeaderItem(col).text()

		if col_header == 'notes':
			log_entry = self.analysis.get_activity_log_entry(row)

			dialog = TextBoxDialog('Write your notes', log_entry.notes, self.isDarkThemeActive())
			result = dialog.exec_()

			if result == QDialog.Accepted:
				note = dialog.getText()
				self.analysis.update_log_entry_notes(row, note)
				
				html_value = markdown.markdown(note)
				markdown_view = QTextEdit()
				markdown_view.setReadOnly(True)
				markdown_view.setHtml(html_value)

				self.activity_log_table.setCellWidget(row, col, markdown_view)

	def isDarkThemeActive(self):

		# Check the color role for the WindowText color
		background_color = self.palette().color(self.backgroundRole())

		# Calculate the overall brightness of the color
		brightness = (background_color.red() * 299 + background_color.green() * 587 + background_color.blue() * 114) / 1000

		# If the brightness is less than a threshold, consider it a dark theme
		return brightness < 128

	def close(self) -> bool:
		return super().close()