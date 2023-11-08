import typing
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem
from PyQt5.QtGui import QColor, QBrush, QPolygonF, QPen
from PyQt5.QtCore import Qt

class FlowchartEllipse(QGraphicsEllipseItem):
    def __init__(self, x: float, y: float, w:float, h:float, parent: QGraphicsItem | None = None, hex_color:str = "#00000"):
        super().__init__(x, y, w, h, parent)
        self.setAcceptHoverEvents(True)

        self.color = QColor(hex_color)

        self.set_color(self.color)
    
    def set_color(self, color :QColor):
        self.color = color
    
        self.setBrush(QBrush(color))
        self.setPen(QPen(QBrush(color), 1, Qt.SolidLine))
    
    def hoverEnterEvent(self, event):
        # Change the appearance when the mouse enters the ellipse
        self.setPen(QPen(QBrush(self.color), 4, Qt.SolidLine))

    def hoverLeaveEvent(self, event):
        # Change the appearance back when the mouse leaves the ellipse
        self.setPen(QPen(QBrush(self.color), 1, Qt.SolidLine))

class FlowchartPolygon(QGraphicsPolygonItem):
    def __init__(self, polygon:QPolygonF, parent: QGraphicsItem | None = None, hex_color:str = "#00000"):
        super().__init__(polygon, parent)
        self.setAcceptHoverEvents(True)

        self.color = QColor(hex_color)

        self.set_color(self.color)
    
    def set_color(self, color :QColor):
        self.color = color
    
        self.setBrush(QBrush(color))
        self.setPen(QPen(QBrush(color), 1, Qt.SolidLine))
    
    def hoverEnterEvent(self, event):
        # Change the appearance when the mouse enters the ellipse
        self.setPen(QPen(QBrush(self.color), 4, Qt.SolidLine))

    def hoverLeaveEvent(self, event):
        # Change the appearance back when the mouse leaves the ellipse
        self.setPen(QPen(QBrush(self.color), 1, Qt.SolidLine))

class LabelTextItem(QGraphicsTextItem):
    def __init__(self, text, flowchart_item):
        super(LabelTextItem, self).__init__(text)

        self.flowchart_item = flowchart_item
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, event):
        # Change the appearance when the mouse enters the text item
        self.flowchart_item.hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        # Change the appearance back when the mouse leaves the text item
        self.flowchart_item.hoverLeaveEvent(event)