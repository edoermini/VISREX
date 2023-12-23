from PyQt6.QtWidgets import QTableWidget, QSizePolicy, QMenu
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, pyqtSignal

class ResponsiveTableWidget(QTableWidget):
	deletedRow = pyqtSignal(int)
	
	def __init__(self, rows, headers: list[str], parent=None):
		super(ResponsiveTableWidget, self).__init__(rows, len(headers), parent)
		self.setHorizontalHeaderLabels(headers)
		self.setEditTriggers(QTableWidget.NoEditTriggers)
		self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.horizontalHeader().setStretchLastSection(True)
		self.sorting_enabled = False

		self.sorting_order : list[Qt.SortOrder] = [Qt.SortOrder.AscendingOrder for header in headers]


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

	def setDefaultSortingEnabled(self, a0:bool):
		if a0:
			self.horizontalHeader().sectionClicked.connect(self.sort_rows)
		else:
			self.horizontalHeader().sectionClicked.disconnect(self.sort_rows)
		
		self.sorting_enabled = a0
	
	def defaultSortingEnabled(self):
		return self.sorting_enabled

	def contextMenuEvent(self, event):
		context_menu = QMenu(self)

		# Get the selected row
		selected_row = self.currentRow()

		# Create actions for the context menu
		delete_row_action = QAction("Delete Row", self)
		delete_row_action.triggered.connect(lambda: self.deleteRow(selected_row))

		# Add actions to the context menu
		context_menu.addAction(delete_row_action)

		# Show the context menu at the cursor position
		context_menu.exec_(event.globalPos())

	def deleteRow(self, row):
		self.removeRow(row)
		self.deletedRow.emit(row)

	def sort_rows(self, logical_index):
		
		if self.sorting_enabled:

			# Get the column values for the clicked header
			column_values = [self.item(row, logical_index).text() for row in range(self.rowCount())]

			self.sorting_order[logical_index] = Qt.SortOrder.AscendingOrder if self.sorting_order[logical_index] == Qt.SortOrder.DescendingOrder else Qt.SortOrder.DescendingOrder

			# Sort the rows based on the column values
			sorted_rows = sorted(range(len(column_values)), key=lambda k: column_values[k], reverse=self.sorting_order[logical_index] == Qt.SortOrder.DescendingOrder)
			new_table = []

			# Rearrange the rows in the table based on the sorted order
			for new_row, old_row in enumerate(sorted_rows):
				new_table.append([])

				for col in range(self.columnCount()):
					item = self.takeItem(old_row, col)
					new_table[new_row].append(item)
			
			for row, columns in enumerate(new_table):
				for col, item in enumerate(columns):
					self.setItem(row, col, item)
