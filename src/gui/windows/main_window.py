from PyQt5.QtWidgets import QMenu, QActionGroup, QStatusBar, QToolBar, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QAction, QTableWidgetItem, QSizePolicy
from PyQt5.QtCore import Qt
import qtawesome as qta
import qdarktheme
import os
from datetime import datetime

from gui.updaters import ActivityUpdater
from gui.dialogs import ReadProcessMemoryDialog
from gui.flowcharts import GraphvizZoomableFlowchart
from gui.tables import ResponsiveTableWidget

from analysis import Analysis
from analysis import Workflow

class MainWindow(QMainWindow):
    def __init__(self, malware_sample=None, old_analysis=None, dark_mode=False):
        super(MainWindow, self).__init__()

        self.malware_sample = malware_sample
        self.old_analysis = old_analysis

        self.workflow = Workflow(os.path.basename(self.malware_sample))
        self.analysis = Analysis(self.workflow)
        
        self.initUI()
        self.dark_mode(dark_mode)

    def initUI(self):
        self.setWindowTitle("MASup (Malware Analysis Supporter)")

        # Creare un widget a pila per le diverse viste
        stacked_widget = QStackedWidget()

        self.progress_view = GraphvizZoomableFlowchart(self.workflow.dot_code(), "#00000")
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

    def closeEvent(self, event):
        event.accept()
    
    def dark_mode(self, active):

        qdarktheme.setup_theme('dark' if active else 'light')
        self.progress_view.dark_mode(active)
        self.progress_page_button.setIcon(qta.icon("fa5s.tasks", color="white" if active else "black"))
        self.activity_log_page_button.setIcon(qta.icon("fa5s.history", color="white" if active else "black"))
        self.process_injection_button.setIcon(qta.icon("fa5s.syringe", color="white" if active else "black"))

    def close(self) -> bool:
        return super().close()