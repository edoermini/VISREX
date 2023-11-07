import typing
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem
from PyQt5.QtGui import QColor, QBrush, QPolygonF, QPen
from PyQt5.QtCore import Qt

class FlowchartItem(QGraphicsItem):
    def __init__(self, parent: QGraphicsItem | None = ...) -> None:
        super().__init__(parent)

        self.fill_color = None

class FlowchartEllipse(QGraphicsEllipseItem):
    def __init__(self, x: float, y: float, w:float, h:float, parent: QGraphicsItem | None = None, hex_color:str = "#00000"):
        super().__init__(x, y, w, h, parent)


        color = QColor(hex_color)

        self.setBrush(QBrush(color))
        self.setPen(QPen(QBrush(color), 1, Qt.SolidLine))

class FlowchartPolygon(QGraphicsPolygonItem):
    def __init__(self, polygon:QPolygonF, parent: QGraphicsItem | None = None, hex_color:str = "#00000"):
        super().__init__(polygon, parent)

        color = QColor(hex_color)

        self.set_color(color)
    
    def set_color(self, color : QColor):
        self.setBrush(QBrush(color))
        self.setPen(QPen(QBrush(color), 1, Qt.SolidLine))


