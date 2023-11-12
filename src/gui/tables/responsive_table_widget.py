from PyQt6.QtWidgets import QTableWidget, QSizePolicy
from PyQt6.QtGui import QPainter, QPen, QPainterPath
from PyQt6.QtCore import Qt, QPointF

class ResponsiveTableWidget(QTableWidget):
	def __init__(self, rows, headers: list[str], parent=None):
		super(ResponsiveTableWidget, self).__init__(rows, len(headers), parent)
		self.setHorizontalHeaderLabels(headers)
		self.setEditTriggers(QTableWidget.NoEditTriggers)
		self.setSizeAdjustPolicy(QTableWidget.AdjustToContents)
		self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
		self.horizontalHeader().setStretchLastSection(True)

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