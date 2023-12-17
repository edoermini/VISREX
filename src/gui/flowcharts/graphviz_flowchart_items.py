from PyQt6.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsSceneContextMenuEvent, QGraphicsSceneHoverEvent, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsPathItem
from PyQt6.QtGui import QColor, QBrush, QPolygonF, QPen, QPainterPath, QFont, QPainter
from PyQt6.QtCore import Qt, QPointF, QRectF

import xml.etree.ElementTree as ET
import re

from .signals import GraphvizFlowchartNodeSignals

from gui.utils import make_color_darker, is_light_color

class ProgressBarItem(QGraphicsRectItem):
	def __init__(self, x, y, width, max_height, color:QColor, border_color:QColor, progress_percentage:float=1, parent=None):
		super().__init__(x, y, width, 0, parent)

		self.coord_y = y
		self.coord_x = x
		self.progress_percentage = progress_percentage  # Default progress percentage
		self.color = color
		self.border_color = border_color
		self.max_height = max_height
		self.width= width
		self.setBrush(QBrush(self.color, Qt.SolidPattern))
		self.setPen(QPen(Qt.NoPen))

		self.setZValue(2)

	def paint(self, painter: QPainter, option, widget=None):
		painter.setRenderHint(painter.Antialiasing)  # Optional, for smoother drawing

		new_height = self.max_height * self.progress_percentage

		# Draw the progress bar
		progress_rect = self.rect()
		progress_rect.setY(self.coord_y + (self.max_height - new_height))
		progress_rect.setHeight(new_height)

		# border rect
		border_rect = QRectF(self.coord_x, self.coord_y, self.width, self.max_height)

		painter.setPen(QPen(self.border_color, 0.5, Qt.SolidLine))
		painter.drawRect(border_rect)

		painter.setPen(QPen(Qt.NoPen))
		painter.setBrush(QBrush(self.color, Qt.SolidPattern))  # Green color for the progress bar
		painter.drawRect(progress_rect)
	
	def setProgressPercentage(self, percentage):
		if 0 <= percentage <= 1:
			#new_height = self.max_height * percentage
			#self.updateHeight(new_height)
			self.progress_percentage = percentage
			self.update()

class GraphvizFlowchartItem(QGraphicsItemGroup):
	def __init__(self,flowchart_height:float, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(parent)

		self.flowchart_height = flowchart_height
		self.xml_text = xml_text
		self.label = QGraphicsTextItem()
	
	def set_label(self, flowchart_item:QGraphicsItem, center:QPointF, color:QColor=None):
		if self.xml_text:

			text = ET.fromstring(self.xml_text)
			font_size = text.get('font-size')

			if font_size is None:
				raise ValueError(f"xml_text has no attribute 'font-size': {self.xml_text}")

			self.label = QGraphicsTextItem(text.text)
			self.label.setFont(QFont('Arial', pointSize=int(float(font_size))-5))
			self.label.setAcceptHoverEvents(True)

			if color is not None:
				self.label.setDefaultTextColor(color)
			else:
				self.label.setDefaultTextColor(QColor(Qt.black) if is_light_color(flowchart_item.brush().color()) else QColor(Qt.white))

			text_x = (center.x() - self.label.boundingRect().width() / 2)
			text_y = (center.y() - self.label.boundingRect().height() / 2)

			self.label.setPos(text_x, text_y)
			self.label.setAcceptHoverEvents(False)

			self.addToGroup(self.label)

class GraphvizFlowchartEdge(GraphvizFlowchartItem):
	def __init__(self, flowchart_height:float, xml_path: str, xml_polygon: str, color:QColor, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(flowchart_height, xml_text, parent)

		self.color = color

		path = ET.fromstring(xml_path)
		polygon = ET.fromstring(xml_polygon)

		points_str = polygon.get('points')

		if points_str is None:
			raise ValueError(f"xml_polygon has no attribute 'points': {xml_polygon}")
		
		points = points_str.split(' ')
		polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1]) + flowchart_height) for point in points ]

		painter_path = QPainterPath()

		path_str = path.get('d')

		if path_str is None:
			raise ValueError(f"xml_path has no attribute 'd': {xml_path}")
		
		commands = re.findall(r'([MC])([^MC]*)', path_str)

		for command, args_str in commands:
			args = [float(arg) if i%2 == 0 else float(arg) + flowchart_height for i, arg in enumerate(args_str.replace(',', ' ').split())]

			if command == 'M':
				painter_path.moveTo(*args)
			elif command == 'C':
				for i in range(0, len(args), 6):
					painter_path.cubicTo(*args[i:i+6])

		self.line = QGraphicsPathItem(painter_path)
		self.line.setAcceptHoverEvents(False)
		self.addToGroup(self.line)
		
		self.line.setPen(QPen(self.color, 1, Qt.SolidLine))

		arrow_figure = QPolygonF([QPointF(x, y) for x, y in polygon_points])
		self.arrow = QGraphicsPolygonItem(arrow_figure, self)
		self.arrow.setAcceptHoverEvents(False)
		self.arrow.setBrush(self.color)
		self.arrow.setPen(QPen(QBrush(self.color), 1, Qt.SolidLine))

		self.item = QGraphicsItemGroup()
		self.item.setAcceptHoverEvents(False)
		self.item.addToGroup(self.arrow)
		self.item.addToGroup(self.line)

		self.addToGroup(self.item)

		self.setZValue(0)

		self.set_label(self.item, painter_path.pointAtPercent(0.5), self.color)
	
	def setColor(self, color:QColor):
		self.arrow.setBrush(color)
		self.arrow.setPen(QPen(QBrush(color), 1, Qt.SolidLine))
		self.line.setPen(QPen(color, 1, Qt.SolidLine))
		self.label.setDefaultTextColor(color)

class GraphvizFlowchartDecision(GraphvizFlowchartItem):

	def __init__(self, node_id:str, flowchart_height:float, xml_polygon: str, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(flowchart_height, xml_text, parent)

		self.signals = GraphvizFlowchartNodeSignals()
		self.setAcceptHoverEvents(True)
		
		self.active = False
		self.node_id = node_id

		polygon = ET.fromstring(xml_polygon)

		fill_color = polygon.get('fill')

		if fill_color is None:
			raise ValueError(f"xml_polygon has no attribute 'fill': {xml_polygon}")
		
		self.color = QColor(fill_color)

		points_str = polygon.get('points')

		if points_str is None:
			raise ValueError(f"xml_polygon has no attribute 'points': {xml_polygon}")
		
		points = points_str.split(' ')
		polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1]) + flowchart_height) for point in points ]

		polygon_figure = QPolygonF([QPointF(x, y) for x, y in polygon_points])
		self.item = QGraphicsPolygonItem(polygon_figure, self)
		self.item.setAcceptHoverEvents(False)
		self.setActive(False)

		self.addToGroup(self.item)

		self.set_label(self.item, self.item.boundingRect().center())
	
	def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
		pen = self.item.pen()
		pen.setWidth(4)
		self.item.setPen(pen)
	
	def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
		pen = self.item.pen()
		pen.setWidth(0)
		self.item.setPen(pen)
	
	def setActive(self, active: bool) -> None:
		self.active = active

		if active:
			self.item.setBrush(self.color)
			self.item.setPen(QPen(QBrush(self.color), 0, Qt.SolidLine))

		else:
			darker_color = make_color_darker(self.color, 0.5)

			self.item.setBrush(darker_color)
			self.item.setPen(QPen(QBrush(darker_color), 0, Qt.SolidLine))

		self.label.setDefaultTextColor(QColor(Qt.black) if is_light_color(self.item.brush().color()) else QColor(Qt.white))	
	
	def isActive(self):
		return self.active
	
	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent | None) -> None:
		mouse_pos = event.screenPos()
		self.signals.rightClick.emit(self.node_id, mouse_pos)

class GraphvizFlowchartProcess(GraphvizFlowchartItem):

	def __init__(self, node_id:str, flowchart_height:float, xml_ellipse: str, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(flowchart_height, xml_text, parent)

		self.signals = GraphvizFlowchartNodeSignals()
		self.setAcceptHoverEvents(True)

		self.active = False
		self.node_id = node_id

		ellipse = ET.fromstring(xml_ellipse)

		fill_color = ellipse.get('fill')

		if fill_color is None:
			raise ValueError(f"xml_ellipse has no attribute 'fill': {xml_ellipse}")

		self.color = QColor(fill_color)

		cx = ellipse.get('cx')
		cy = ellipse.get('cy')
		rx = ellipse.get('rx')
		ry = ellipse.get('ry')

		if cx is None:
			raise ValueError(f"xml_text has no attribute 'cx': {xml_ellipse}")
		if cy is None:
			raise ValueError(f"xml_text has no attribute 'cy': {xml_ellipse}")
		if rx is None:
			raise ValueError(f"xml_text has no attribute 'rx': {xml_ellipse}")
		if ry is None:
			raise ValueError(f"xml_text has no attribute 'ry': {xml_ellipse}")
	
		x = (float(cx) - float(rx))
		y = (float(cy) + flowchart_height) - float(ry)
		width = float(rx)*2
		height = float(ry)*2

		self.item = QGraphicsEllipseItem(x, y, width, height, self)
		self.item.setAcceptHoverEvents(False)
		self.setActive(False)

		self.set_label(self.item, self.item.boundingRect().center())

		self.addToGroup(self.item)

		self.progress_bar = ProgressBarItem(x + width+5, y, 3, height, self.color, self.color)
		self.addToGroup(self.progress_bar)
		self.setZValue(1)
	
	def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
		pen = self.item.pen()
		pen.setWidth(4)
		self.item.setPen(pen)
	
	def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent | None) -> None:
		pen = self.item.pen()
		pen.setWidth(0)
		self.item.setPen(pen)
	
	def setActive(self, active: bool) -> None:
		self.active = active

		if active:
			self.item.setBrush(self.color)
			self.item.setPen(QPen(QBrush(self.color), 0, Qt.SolidLine))

		else:
			darker_color = make_color_darker(self.color, 0.5)

			self.item.setBrush(darker_color)
			self.item.setPen(QPen(QBrush(darker_color), 0, Qt.SolidLine))

		self.label.setDefaultTextColor(QColor(Qt.black) if is_light_color(self.item.brush().color()) else QColor(Qt.white))
	
	def isActive(self):
		return self.active
	
	def contextMenuEvent(self, event: QGraphicsSceneContextMenuEvent | None) -> None:
		mouse_pos = event.screenPos()
		self.signals.rightClick.emit(self.node_id, mouse_pos)
	
	def setProgressPercentage(self, percentage:float):
		self.progress_bar.setProgressPercentage(percentage)