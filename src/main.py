import sys
from PyQt5.QtWidgets import QMenu, QSplitter, QLabel, QActionGroup, QStatusBar, QToolBar, QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QAction, QTableWidgetItem
from PyQt5.QtCore import Qt
import qtawesome as qta
import qdarktheme

from gui.tables.responsive_table_widget import ResponsiveTableWidget
from gui.updaters import ProgressTableUpdater
from gui.dialogs import ReadProcessMemory
from gui.flowcharts import GraphvizZoomableFlowchart

from analysis import Analysis
from analysis import Workflow

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.workflow = Workflow()

        self.initUI()

    def initUI(self):
        self.setWindowTitle("MASup (Malware Analysis Supporter)")

        # Creare un widget a pila per le diverse viste
        stacked_widget = QStackedWidget()

        self.interactive_workflow_view = GraphvizZoomableFlowchart(self.workflow.dot_code(), "#00000")
        self.interactive_workflow_view.set_opacity(0.2)

        interactive_workflow_page = QWidget()
        workflow_page_layout = QVBoxLayout(interactive_workflow_page)
        workflow_page_layout.addWidget(self.interactive_workflow_view)
        stacked_widget.addWidget(interactive_workflow_page)

        self.setCentralWidget(stacked_widget)

        self.toolbar = QToolBar("Toolbar", self)
        self.toolbar.setContextMenuPolicy(Qt.PreventContextMenu)
        
        self.addToolBar(Qt.LeftToolBarArea, self.toolbar)

        toolbar_actions = QActionGroup(self)
        toolbar_actions.setExclusive(True)

        progress_button = QAction(qta.icon("fa5s.tasks"), "Progress", self)
        progress_button.setStatusTip("Analysis' progresses")
        progress_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(0))
        progress_button.setCheckable(True)
        progress_button.setChecked(True)
        toolbar_actions.addAction(progress_button)
        self.toolbar.addAction(progress_button)

        self.toolbar.addSeparator()

        self.setStatusBar(QStatusBar(self))

        # Aggiungere il menu "File" con un'opzione di uscita
        menubar = self.menuBar()
        file_menu = menubar.addMenu('File')

        exit_action = QAction('Quit', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Aggiungere un menu "View" con una checkbox
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

        analysis_menu = menubar.addMenu('Analysis')
        process_injection_menu = QMenu('Process injection', self)
        extract_injected_action = QAction('Read process memory', self, checkable=False)
        extract_injected_action.triggered.connect(lambda: ReadProcessMemory(self).exec_())
        process_injection_menu.addAction(extract_injected_action)

        analysis_menu.addMenu(process_injection_menu)

        layout = QVBoxLayout()
        layout.addWidget(stacked_widget)

        # Creare un widget principale e impostare il layout principale
        main_widget = QWidget()
        main_widget.setLayout(layout)

        # Impostare il widget principale come widget centrale della finestra principale
        self.setCentralWidget(main_widget)

        self.analysis = Analysis(self.workflow)

        self.process_table_updater = ProgressTableUpdater(self)
        self.process_table_updater.start()
    
    def update_progress(self):
        self.analysis.update_activities()

        for node_id in self.analysis.activities:
            self.interactive_workflow_view.set_opacity(1, node_id)

    def closeEvent(self, event):
        self.process_table_updater.stop()
        self.process_table_updater.join()
        event.accept()
    
    def dark_mode(self, active):
        if active:
            qdarktheme.setup_theme('dark')
            self.interactive_workflow_view.set_edges_color("#ffffff")
        else:
            qdarktheme.setup_theme('light')
            self.interactive_workflow_view.set_edges_color("#000000")

    def close(self) -> bool:
        self.tmp_dir.cleanup()
        return super().close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme('light')

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
