# import eel
# eel.init('web')
# eel.start(
#     'templates/progress.html',
#     jinja_templates='templates'
# )

import sys
from PyQt5.QtWidgets import QMenu, QSplitter, QTableWidget, QTableWidgetItem, QActionGroup, QStatusBar, QToolBar, QApplication, QMainWindow, QVBoxLayout, QWidget, QStackedWidget, QAction
from PyQt5.QtCore import Qt
import qtawesome as qta
import json
import qdarktheme

class ResponsiveTableWidget(QTableWidget):
    def __init__(self, rows, headers:list[str]):
        super(ResponsiveTableWidget, self).__init__(rows, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)

    def resizeEvent(self, event):
        super(ResponsiveTableWidget, self).resizeEvent(event)
        self.updateColumnWidths()

    def updateColumnWidths(self):
        table_width = self.viewport().width()
        total_column_width = 0

        for col in range(self.columnCount()):
            total_column_width += self.columnWidth(col)

        for col in range(self.columnCount()):
            column_width = self.columnWidth(col)
            new_width = int(column_width / total_column_width * table_width)
            self.setColumnWidth(col, new_width)
    
    def update_table(self, ):
        
        # Aggiornare i dati della tabella (ad esempio, dati dal database)
        # In questo esempio, inseriamo dati di esempio casuali
        stacked_widget = self.centralWidget().layout().itemAt(0).widget()
        table_widget = stacked_widget.currentWidget().layout().itemAt(0).widget()
        
        for row in range(1, table_widget.rowCount()):
            for col in range(table_widget.columnCount()):
                item = QTableWidgetItem(str(row * col))
                table_widget.setItem(row, col, item)

class JSONResposiveTableWidget(ResponsiveTableWidget):
    
    def __init__(self, json_file:str, columns:list[str], headers:list[str]):
        """A Qt Table widget created from a json file

        Keyword arguments:
        json_file (str): the path to json file
        columns (list[str]): for each element of the json 
        headers (OrderedDict[str, str]): a dict representing the columns of the table;
        """

        data = {}

        with open(json_file, 'r') as file:
            data = json.load(file)

        super().__init__(len(data['nodes']), headers)

        # Popolare la tabella con i dati dal JSON
        for node_id, (_, node_data) in enumerate(data["nodes"].items()):
            row_position = node_id  # Ottenere la posizione della riga dall'ID del nodo
            for i, column in enumerate(columns):
                cell = node_data[column]

                if isinstance(node_data[column], list):
                    cell = ", ".join(node_data[column])

                self.setItem(row_position, i, QTableWidgetItem(cell))

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.setWindowTitle("MASup (Malware Analysis Supporter)")

        # Creare un widget a pila per le diverse viste
        stacked_widget = QStackedWidget()

        splitter = QSplitter(Qt.Vertical)
        
        progress_page = QWidget()
        progress_page_layout = QVBoxLayout(progress_page)
        progress_page_layout.addWidget(ResponsiveTableWidget(1, ['Name', 'Phase', 'Tools', 'Status']))
        splitter.addWidget(progress_page)

        suggestions_page = QWidget()
        suggestions_page_layout = QVBoxLayout(suggestions_page)
        suggestions_page_layout.addWidget(ResponsiveTableWidget(1, ['Name', 'Phase', 'Tools', 'Suggestions']))
        splitter.addWidget(suggestions_page)

        stacked_widget.addWidget(splitter)

        workflow_page = QWidget()
        workflow_page_layout = QVBoxLayout(workflow_page)
        workflow_page_layout.addWidget(JSONResposiveTableWidget('workflow.json', ['name', 'phase', 'tools'], ['Name', 'Phase', 'Tools', 'Status']))
        stacked_widget.addWidget(workflow_page)

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

        suggestions_button = QAction(qta.icon('fa5s.stream'), "Flow", self)
        suggestions_button.setStatusTip("Analysis' suggestions")
        suggestions_button.triggered.connect(lambda: stacked_widget.setCurrentIndex(1))
        suggestions_button.setCheckable(True)
        toolbar_actions.addAction(suggestions_button)
        self.toolbar.addAction(suggestions_button)

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
        show_toolbar_action.triggered.connect(lambda checked: self.toolbar.setVisible(checked))
        view_menu.addAction(show_toolbar_action)

        appearance_submenu = QMenu('Appearance', self)
        dark_mode_action = QAction('Dark mode', self, checkable=True)
        dark_mode_action.setChecked(False)
        dark_mode_action.triggered.connect(lambda checked : qdarktheme.setup_theme('dark' if checked else 'light'))
        appearance_submenu.addAction(dark_mode_action)

        view_menu.addMenu(appearance_submenu)

        layout = QVBoxLayout()
        layout.addWidget(stacked_widget)

        # Creare un widget principale e impostare il layout principale
        main_widget = QWidget()
        main_widget.setLayout(layout)

        # Impostare il widget principale come widget centrale della finestra principale
        self.setCentralWidget(main_widget)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme('light')

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
