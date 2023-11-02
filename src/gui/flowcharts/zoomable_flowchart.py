import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter  

class ZoomableFlowchart(QGraphicsView):
    def __init__(self, svg_file):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.svg_item = QGraphicsSvgItem(svg_file)
        self.scene.addItem(self.svg_item)

        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)

        self.setDragMode(QGraphicsView.ScrollHandDrag)

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)