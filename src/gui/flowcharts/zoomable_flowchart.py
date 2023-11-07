import sys
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter  
import io

class ZoomableFlowchart(QGraphicsView):
    def __init__(self, svg_file):
        super().__init__()

        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        svg_renderer = QSvgRenderer(svg_file.read())

        self.svg_item = QGraphicsSvgItem()
        self.svg_item.setSharedRenderer(svg_renderer)
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