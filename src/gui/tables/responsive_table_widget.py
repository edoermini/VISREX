from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QSizePolicy
import json

class ResponsiveTableWidget(QTableWidget):
    def __init__(self, rows, headers: list[str]):
        super(ResponsiveTableWidget, self).__init__(rows, len(headers))
        self.setHorizontalHeaderLabels(headers)
        self.setEditTriggers(QTableWidget.NoEditTriggers)
        self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def resizeEvent(self, event):
        super(ResponsiveTableWidget, self).resizeEvent(event)
        self.updateColumnWidths()

    def updateColumnWidths(self):
        if self.isCollapsed():
            return

        table_width = self.viewport().width()
        total_column_width = sum(self.columnWidth(col) for col in range(self.columnCount()))

        if total_column_width == 0:
            return  # Avoid division by zero

        for col in range(self.columnCount()):
            column_width = self.columnWidth(col)
            new_width = int(column_width / total_column_width * table_width)
            self.setColumnWidth(col, new_width)

    def isCollapsed(self):
        return self.width() == 0

class JSONResponsiveTableWidget(ResponsiveTableWidget):
    
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
        
        nodes = data['workflow']['nodes']

        super().__init__(len(nodes), headers)

        # Popolare la tabella con i dati dal JSON
        for node_id, (_, node_data) in enumerate(nodes.items()):
            row_position = node_id  # Ottenere la posizione della riga dall'ID del nodo
            for i, column in enumerate(columns):
                cell = node_data[column]

                if isinstance(node_data[column], list):
                    cell = ", ".join(node_data[column])

                self.setItem(row_position, i, QTableWidgetItem(cell))