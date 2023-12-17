from PyQt6.QtWidgets import QMenu, QStatusBar, QToolBar, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QTableWidgetItem, QFileDialog, QDialog, QLabel, QSplitter, QTableWidget, QMessageBox
from PyQt6.QtCore import Qt, QSize, QTimer, QThread
from PyQt6.QtGui import QMovie, QAction, QActionGroup, QColor
import qtawesome as qta
import qdarktheme
import os
import pickle
from time import time
from functools import partial
import subprocess
import platform
from pathlib import Path

from gui.updaters import ActivityUpdater, ExecutablesUpdater
from gui.dialogs import ReadProcessMemoryDialog, ComboBoxDialog, ToolsCoverageDialog, IATReconstructionDialog, TextBoxDialog
from gui.flowcharts import GraphvizFlowchart
from gui.tables import ResponsiveTableWidget
from gui.shared import StatusMessagesQueue
from gui.widgets import MardownEdit
from gui.utils import is_dark_theme_active

from analysis import Analysis, AnalysisLogEntry
from integrations.importer import get_tool
from integrations.generics import DesktopTool

class MainWindow(QMainWindow):
	def __init__(self, malware_sample=None, analysis_file=None):
		super(MainWindow, self).__init__()

		self.analysis_file = analysis_file
		self.messages = StatusMessagesQueue()
		self.replay_started = False
		self.replay_index = 0
		self.analysis = None

		if malware_sample is not None:
			self.analysis = Analysis(malware_sample)

			self.analysis.update_activity_log(
				AnalysisLogEntry(
					"",
					"Set malware sample",
					"",
					[self.analysis.malware_sample,],
					"",
					time()
				)
			)
		
		else:
			self.analysis = Analysis.import_analysis(self.analysis_file)
		
		self.initUI()
		self.setTheme('auto')

	def initUI(self):
		self.setWindowTitle("MASup (Malware Analysis Supporter)")

		# Creare un widget a pila per le diverse viste
		stacked_widget = QStackedWidget()

		# flowchart page
		self.flowchart = GraphvizFlowchart(self.analysis.workflow.dot_code(), QColor(Qt.white) if is_dark_theme_active(self) else QColor(Qt.black), 0.3)
		self.flowchart.signals.rightClick.connect(self.openFlowchartNodeContextMenu)
		self.flowchart.setProgressPercentage(0)

		flowchart_page = QWidget()
		flowchart_page_layout = QVBoxLayout(flowchart_page)
		flowchart_page_layout.addWidget(self.flowchart)

		# activity log page

		self.activity_log_page = QWidget()
		activity_log_page_layout = QVBoxLayout(self.activity_log_page)

		activity_log_toolbar = QToolBar(self)
		
		self.play_action = QAction(qta.icon("fa5s.play", color="white" if is_dark_theme_active(self) else "black"), "Play", self)
		self.play_action.setDisabled(True if self.analysis.get_activity_log_len() == 0 else False)
		self.play_action.triggered.connect(self.play_clicked)
		activity_log_toolbar.addAction(self.play_action)

		self.stop_action = QAction(qta.icon("fa5s.stop", color="white" if is_dark_theme_active(self) else "black"), "Stop", self)
		self.stop_action.setDisabled(True)
		self.stop_action.triggered.connect(self.stop_clicked)
		activity_log_toolbar.addAction(self.stop_action)
		
		activity_log_toolbar.addSeparator()

		self.step_forward_action = QAction(qta.icon("fa5s.step-forward", color="white" if is_dark_theme_active(self) else "black"), "Step forward", self)
		self.step_forward_action.setDisabled(True)
		self.step_forward_action.triggered.connect(self.execute_activity)
		activity_log_toolbar.addAction(self.step_forward_action)

		self.skip_action = QAction(qta.icon('fa5s.redo-alt', color="white" if is_dark_theme_active(self) else "black"), "Skip", self)
		self.skip_action.setDisabled(True)
		self.skip_action.triggered.connect(self.skip_activity)
		activity_log_toolbar.addAction(self.skip_action)

		activity_log_page_layout.addWidget(activity_log_toolbar)

		self.activity_log_page_splitter = QSplitter(Qt.Vertical)

		self.activity_log_table = ResponsiveTableWidget(self.analysis.get_activity_log_len(), AnalysisLogEntry.get_keys())
		self.activity_log_table.setSelectionMode(QTableWidget.SingleSelection)
		self.activity_log_table.cellClicked.connect(self.cell_selected)
		self.activity_log_table.currentCellChanged.connect(self.cell_selected)
		
		self.activity_log_page_splitter.addWidget(self.activity_log_table)

		self.notes_stacked_widget = QStackedWidget()

		for row, log_entry in enumerate(self.analysis.get_activity_log()):

			notes_edit_view = MardownEdit(is_dark_theme_active(self))
			notes_edit_view.setText(log_entry.notes)
			notes_edit_view.textUpdated.connect(self.updateLogEntryNotes)
			self.notes_stacked_widget.addWidget(notes_edit_view)

			columns = log_entry.to_json(string_values=True)

			for col, (_, value) in enumerate(columns.items()):
				item = QTableWidgetItem(value)
				self.activity_log_table.setItem(row, col, item)

		self.notes_stacked_widget.hide()

		self.activity_log_page_splitter.addWidget(self.notes_stacked_widget)

		activity_log_page_layout.addWidget(self.activity_log_page_splitter)

		stacked_widget.addWidget(flowchart_page)
		stacked_widget.addWidget(self.activity_log_page)

		self.setCentralWidget(stacked_widget)

		# toolbar

		self.toolbar = QToolBar("Toolbar", self)
		self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
		
		self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

		toolbar_actions = QActionGroup(self)
		toolbar_actions.setExclusive(True)

		self.progress_page_button = QAction(qta.icon("fa5s.project-diagram", color="white" if is_dark_theme_active(self) else "black"), "Progress", self)
		self.progress_page_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(0))
		self.progress_page_button.setCheckable(True)
		self.progress_page_button.setChecked(True)
		toolbar_actions.addAction(self.progress_page_button)
		self.toolbar.addAction(self.progress_page_button)

		self.activity_log_page_button = QAction(qta.icon("fa5s.history", color="white" if is_dark_theme_active(self) else "black"), "Activity log", self)
		self.activity_log_page_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(1))
		self.activity_log_page_button.setCheckable(True)
		self.activity_log_page_button.setChecked(False)
		toolbar_actions.addAction(self.activity_log_page_button)
		self.toolbar.addAction(self.activity_log_page_button)

		self.toolbar.addSeparator()

		self.read_process_memory_button = QAction(qta.icon("fa5s.syringe", color="white" if is_dark_theme_active(self) else "black"), "Read process memory", self)
		self.read_process_memory_button.triggered.connect(self.readProcessMemory)
		self.read_process_memory_button.setCheckable(False)
		self.toolbar.addAction(self.read_process_memory_button)

		self.iat_reconstruction_button = QAction(qta.icon("fa5s.tools", color="white" if is_dark_theme_active(self) else "black"), "Reconstruct IAT", self)
		self.iat_reconstruction_button.triggered.connect(self.iatReconstruct)
		self.iat_reconstruction_button.setCheckable(False)
		self.toolbar.addAction(self.iat_reconstruction_button)

		# top menu

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

		export_flowchat_png_action = QAction('Export Flowchart PNG', self)
		export_flowchat_png_action.triggered.connect(self.exportPNG)
		file_menu.addAction(export_flowchat_png_action)

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

		main_widget = QWidget()
		main_widget.setLayout(layout)

		self.setCentralWidget(main_widget)

		# status bar

		self.setStatusBar(QStatusBar(self))

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
			self.flowchart.exportPNG(file_path)

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

		last_row = self.activity_log_table.rowCount()

		for node_id in self.analysis.activities:
			if not self.flowchart.isActive(node_id):
				self.flowchart.setActive(True, node_id)

		for i, log_entry in enumerate(self.analysis.get_activity_log(last_row)):
			
			if not self.play_action.isEnabled():
				self.play_action.setDisabled(False)

			row = last_row + i
			columns = log_entry.to_json(string_values=True)
			column_count = len(columns)

			if row == self.activity_log_table.rowCount():
				self.activity_log_table.insertRow(row)

			notes_edit_view = MardownEdit(is_dark_theme_active(self))
			notes_edit_view.textUpdated.connect(self.updateLogEntryNotes)
			self.notes_stacked_widget.addWidget(notes_edit_view)
			
			if column_count > self.activity_log_table.columnCount():
				self.activity_log_table.setColumnCount(column_count)
				self.activity_log_table.setHorizontalHeaderLabels(columns.keys())

			for col, (_, value) in enumerate(columns.items()):
				item = QTableWidgetItem(value)
				self.activity_log_table.setItem(row, col, item)

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
		file_path, _ = QFileDialog.getSaveFileName(self, "Save Object", "", "JSON Files (*.json)")
		if file_path:
			self.analysis_file = file_path
			self.analysis.export_analysis(self.analysis_file)

	def openFile(self):
		file_path, _ = QFileDialog.getOpenFileName(self, "Load Object", "", "JSON Files (*.json)")
		if file_path:
			self.analysis_file = file_path
			self.analysis = Analysis.import_analysis(self.analysis_file)
			self.flowchart.redraw(self.analysis.workflow.dot_code())
	
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
	
	def iatReconstruct(self):
		tools = self.analysis.get_installed_tools('impt_2')
		
		iat_reconstruction_dialog = IATReconstructionDialog(tools, self)
		iat_reconstruction_dialog.setMinimumWidth(300)
		iat_reconstruction_dialog_result = QDialog.Accepted
		executable_dialog_result = QDialog.Rejected

		while iat_reconstruction_dialog_result == QDialog.Accepted and executable_dialog_result == QDialog.Rejected:
			iat_reconstruction_dialog_result = iat_reconstruction_dialog.exec_()

			if iat_reconstruction_dialog_result == QDialog.Accepted:
				tool_name = iat_reconstruction_dialog.getTool()
				oep = iat_reconstruction_dialog.getOEP()

				executable_dialog = ComboBoxDialog('Chose executable', self.analysis.get_executable(tool_name))
				executable_dialog_result = executable_dialog.exec_()

				if executable_dialog_result == QDialog.Accepted:
					tool_module = get_tool(tool_name)

					if not tool_module:
						error_dialog = QMessageBox(self)
						error_dialog.setIcon(QMessageBox.Warning)
						error_dialog.setWindowTitle("Error")
						error_dialog.setText(f"Automations for tool {tool_name} are not available yet\nChose another tool")
						error_dialog.exec_()
					else:
						tool = tool_module.Tool(executable_dialog.getSelected())
						tool.execute(malware=os.path.basename(self.analysis.malware_sample), oep=oep)

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

		dark_mode = is_dark_theme_active(self)

		self.flowchart.setEdgesColor(QColor(Qt.white) if dark_mode else QColor(Qt.black))
		self.progress_page_button.setIcon(qta.icon("fa5s.project-diagram", color="white" if dark_mode else "black"))
		self.iat_reconstruction_button.setIcon(qta.icon("fa5s.tools", color="white" if dark_mode else "black"))
		self.activity_log_page_button.setIcon(qta.icon("fa5s.history", color="white" if dark_mode else "black"))
		self.read_process_memory_button.setIcon(qta.icon("fa5s.syringe", color="white" if dark_mode else "black"))
		self.play_action.setIcon(qta.icon("fa5s.play", color="white" if dark_mode else "black"))
		self.stop_action.setIcon(qta.icon("fa5s.stop", color="white" if dark_mode else "black"))
		self.step_forward_action.setIcon(qta.icon("fa5s.step-forward", color="white" if dark_mode else "black"))

		for index in range(self.notes_stacked_widget.count()):
			self.notes_stacked_widget.widget(index).setDarkMode(dark_mode)

	def openFlowchartNodeContextMenu(self, node_id, mouse_pos):
		context_menu = QMenu(self)
		
		launch_tool_action = context_menu.addAction("Launch tool")
		launch_tool_action.triggered.connect(partial(self.openTool, node_id))
		
		show_tools_coverage_action = context_menu.addAction("Show tools coverage")
		show_tools_coverage_action.triggered.connect(partial(self.showToolsCoverage, node_id))

		automatize_menu = QMenu("Automatize")

		if node_id == 'start':
			change_sample_action = QAction('Change malware sample')
			change_sample_action.triggered.connect(self.changeMalwareSample)
			context_menu.addAction(change_sample_action)

		if node_id == 'impt_2':
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

		tools_coverage_dialog = ToolsCoverageDialog(coverage, is_dark_theme_active(self))
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
	
	def cell_selected(self, row, col):
		# notes
		self.notes_stacked_widget.show()
		self.notes_stacked_widget.setCurrentIndex(row)

	def updateLogEntryNotes(self, note):
		log_row = self.notes_stacked_widget.currentIndex()
		self.analysis.update_log_entry_notes(log_row, note)
	
	def play_clicked(self):
		
		self.activity_updater.stop()
		self.play_action.setDisabled(True)
		self.stop_action.setDisabled(False)
		self.step_forward_action.setDisabled(False)
		self.skip_action.setDisabled(False)
		self.replay_started = True

		self.execute_activity()
	
	def stop_clicked(self):
		for col in range(self.activity_log_table.columnCount()):
			item = self.activity_log_table.item(self.replay_index-1, col)
			item.setBackground(Qt.transparent)

		self.activity_updater.start()

		self.play_action.setDisabled(False)
		self.stop_action.setDisabled(True)
		self.step_forward_action.setDisabled(True)
		self.skip_action.setDisabled(True)
		self.replay_index = 0
		self.replay_started = False
	
	def execute_activity(self):

		self.highlight_activity()

		log_entry = self.analysis.get_activity_log_entry(self.replay_index)

		if log_entry.tool != '':
			tool_module = get_tool(log_entry.tool)

			if not tool_module:
				error_dialog = QMessageBox(self)
				error_dialog.setIcon(QMessageBox.Warning)
				error_dialog.setWindowTitle("Error")
				error_dialog.setText(f"Automations for tool {log_entry.tool} are not available yet\nFollow the notes written by the author")
				error_dialog.exec_()
				
			else:
				tool = tool_module.Tool(log_entry.executable)

				if log_entry.activity == 'Open tool':
					tool.execute(arguments=log_entry.arguments, malware=str(self.analysis.malware_sample))

				elif log_entry.activity == 'Close tool':
					if isinstance(tool, DesktopTool):
						tool.attach()
						tool.close()
		else:
			if log_entry.activity == "Set malware sample":
				if self.analysis.malware_sample != log_entry.arguments[0]:
					self.analysis.change_malware_sample(log_entry.arguments[0])
					self.flowchart.redraw(self.analysis.workflow.dot_code())


		self.replay_index += 1

		if self.replay_index == self.activity_log_table.rowCount():
			self.stop_clicked()
			
			return
	
	def skip_activity(self):
		self.highlight_activity()

		self.replay_index += 1

		if self.replay_index == self.activity_log_table.rowCount():
			self.stop_clicked()
			
			return
	
	def highlight_activity(self):
		if self.replay_index > 0:
			for col in range(self.activity_log_table.columnCount()):
				item = self.activity_log_table.item(self.replay_index-1, col)
				item.setBackground(Qt.transparent)
		
		for col in range(self.activity_log_table.columnCount()):
			item = self.activity_log_table.item(self.replay_index, col)
			item.setBackground(QColor('red'))

		self.activity_log_table.setCurrentCell(self.replay_index, self.activity_log_table.currentColumn())
	
	def changeMalwareSample(self):
		options = QFileDialog.Options()
		options |= QFileDialog.ReadOnly
		
		file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "", "Binary Files (*.bin);;Executable Files (*.exe);;Text Files (*.txt);;All Files (*)", options=options)

		if file_name:
			self.analysis.change_malware_sample(file_name)
			
			self.analysis.update_activity_log(
				AnalysisLogEntry(
					"",
					"Set malware sample",
					"",
					[file_name,],
					"",
					time()
				)	
			)

			self.flowchart.redraw(self.analysis.workflow.dot_code())

	def close(self) -> bool:
		return super().close()