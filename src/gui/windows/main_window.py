from PyQt5.QtWidgets import QMenu, QActionGroup, QStatusBar, QToolBar, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QAction, QTableWidgetItem, QFileDialog
from PyQt5.QtCore import Qt
import qtawesome as qta
import qdarktheme
import os
from datetime import datetime
import pickle

from gui.updaters import ActivityUpdater
from gui.dialogs import ReadProcessMemoryDialog
from gui.flowcharts import GraphvizZoomableFlowchart
from gui.tables import ResponsiveTableWidget

from analysis import Analysis

class MainWindow(QMainWindow):
    def __init__(self, malware_sample=None, analysis_file=None, dark_mode=False):
        super(MainWindow, self).__init__()

        self.malware_sample = malware_sample
        self.analysis_file = analysis_file
        self.analysis = None

        if self.malware_sample is not None:
            self.malware_sample = os.path.basename(self.malware_sample)
            self.analysis = Analysis(self.malware_sample)
        
        else:
            with open(self.analysis_file, "rb") as file:
                self.analysis = pickle.load(file)
        
        self.initUI()
        self.dark_mode(dark_mode)

    def initUI(self):
        self.setWindowTitle("MASup (Malware Analysis Supporter)")

        # Creare un widget a pila per le diverse viste
        stacked_widget = QStackedWidget()

        self.progress_view = GraphvizZoomableFlowchart(self.analysis.workflow.dot_code(), "#00000")
        self.progress_view.set_opacity(0.2)

        progress_page = QWidget()
        progress_page_layout = QVBoxLayout(progress_page)
        progress_page_layout.addWidget(self.progress_view)
        stacked_widget.addWidget(progress_page)

        self.activity_log_table = ResponsiveTableWidget(0, ['Time', 'Tool', 'Executable', 'Action'], self)
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

        self.process_injection_button = QAction(qta.icon("fa5s.syringe"), "Read process memory", self)
        self.process_injection_button.triggered.connect(lambda: ReadProcessMemoryDialog(self).exec_())
        self.process_injection_button.setCheckable(False)
        toolbar_actions.addAction(self.process_injection_button)
        self.toolbar.addAction(self.process_injection_button)

        self.setStatusBar(QStatusBar(self))

        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        save_action = QAction('Save', self)
        save_action.triggered.connect(self.save_file)
        file_menu.addAction(save_action)

        save_with_name_action = QAction('Save with name', self)
        save_with_name_action.triggered.connect(self.save_with_name)
        file_menu.addAction(save_with_name_action)

        load_action = QAction('Open analysis', self)
        load_action.triggered.connect(self.open_file)
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
        dark_mode_action = QAction('Dark mode', self, checkable=True)
        dark_mode_action.setChecked(False)
        dark_mode_action.triggered.connect(self.dark_mode)
        appearance_submenu.addAction(dark_mode_action)

        view_menu.addMenu(appearance_submenu)

        layout = QVBoxLayout()
        layout.addWidget(stacked_widget)

        # Creare un widget principale e impostare il layout principale
        main_widget = QWidget()
        main_widget.setLayout(layout)

        # Impostare il widget principale come widget centrale della finestra principale
        self.setCentralWidget(main_widget)

        self.activity_updater = ActivityUpdater(self.analysis, 500)
        self.activity_updater.dataUpdated.connect(self.update_progress)
    
    def update_progress(self):
        self.analysis.update_activities()

        for node_id in self.analysis.activities:
            self.progress_view.set_opacity(1, node_id)
        
        for row, log in enumerate(self.analysis.activity_log):

            if row == self.activity_log_table.rowCount():
                self.activity_log_table.insertRow(row)
            
            columns = [datetime.fromtimestamp(log['time']).isoformat(), log['tool'], log['executable'], "opened" if log['opened'] else "closed"]

            for col, value in enumerate(columns):
                item = QTableWidgetItem(value)
                self.activity_log_table.setItem(row, col, item)

    def save_file(self):

        if not self.analysis_file:
            self.save_with_name()
            return
        
        self.analysis.export_analysis(self.analysis_file)

    def save_with_name(self):
        file_path, _ = QFileDialog.getSaveFileName(self, "Save Object", "", "Malware Analysis Supporter Files (*.masup)")
        if file_path:
            self.analysis_file = file_path
            self.analysis.export_analysis(self.analysis_file)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Load Object", "", "Malware Analysis Supporter Files (*.masup)")
        if file_path:
            with open(file_path, "rb") as file:
                self.analysis = pickle.load(file)

    def closeEvent(self, event):
        self.activity_updater.stop()
        event.accept()
    
    def dark_mode(self, active):

        qdarktheme.setup_theme('dark' if active else 'light')
        self.progress_view.dark_mode(active)
        self.progress_page_button.setIcon(qta.icon("fa5s.tasks", color="white" if active else "black"))
        self.activity_log_page_button.setIcon(qta.icon("fa5s.history", color="white" if active else "black"))
        self.process_injection_button.setIcon(qta.icon("fa5s.syringe", color="white" if active else "black"))

    def close(self) -> bool:
        return super().close()