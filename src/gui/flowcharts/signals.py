from PyQt6.QtCore import pyqtSignal, QPoint, QObject

class GraphvizFlowchartNodeSignals(QObject):
	rightClick = pyqtSignal(str, QPoint)

class GraphzivFlowchartSignals(QObject):
	rightClick = pyqtSignal(str, QPoint)