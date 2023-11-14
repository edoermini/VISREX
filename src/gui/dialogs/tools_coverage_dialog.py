from PyQt6.QtWidgets import QDialog, QVBoxLayout,QTableWidget, QTableWidgetItem, QHeaderView
from gui.tables import ResponsiveTableWidget
import qtawesome as qta

class ToolsCoverageDialog(QDialog):
	def __init__(self, tools:dict[str, bool], dark_mode:bool):
		super().__init__()
		self.tools = tools
		self.dark_mode = dark_mode
		self.initUI()

	def initUI(self):
		# Set up the layout
		layout = QVBoxLayout()
		self.setWindowTitle('Tools coverage')

		table = ResponsiveTableWidget(len(self.tools), ['tool', 'present'])
		#table.setHorizontalHeaderLabels(['tool', 'present'])

		header = table.horizontalHeader()
		header.setStretchLastSection(False)
		header.setSectionResizeMode(0, QHeaderView.Fixed)
		header.resizeSection(0, 200)
		header.setSectionResizeMode(1, QHeaderView.Fixed)
		header.resizeSection(1, 70)

		for row, (tool, present) in enumerate(self.tools.items()):
			item = QTableWidgetItem(tool)
			table.setItem(row, 0, item)

			item = QTableWidgetItem(qta.icon(
				"fa5s.check-circle" if present else "fa5s.times-circle", 
				color="green" if present else "red"
			), "")
			table.setItem(row, 1, item)
		
		width = sum(table.columnWidth(col) for col in range(table.columnCount())) + 50
		height = sum(table.rowHeight(row) for row in range(table.rowCount())) + 47

		self.setFixedSize(width, height)
		
		layout.addWidget(table)

		self.setLayout(layout)
