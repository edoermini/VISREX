from PyQt5.QtWidgets import QGraphicsItem, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsSceneHoverEvent, QGraphicsTextItem, QGraphicsItemGroup, QGraphicsPathItem
from PyQt5.QtGui import QColor, QBrush, QPolygonF, QPen, QPainterPath, QFont
from PyQt5.QtCore import Qt, QPointF

import xml.etree.ElementTree as ET
import re

class GraphvizFlowchartItem(QGraphicsItemGroup):
	def __init__(self, flowchart_height:float, xml_text:str = "", parent: QGraphicsItem = None):
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

			if color is not None:
				self.label.setDefaultTextColor(color)
			else:
				self.label.setDefaultTextColor(self._get_node_text_color(flowchart_item))

			text_x = (center.x() - self.label.boundingRect().width() / 2)
			text_y = (center.y() - self.label.boundingRect().height() / 2)

			self.label.setPos(text_x, text_y)
			self.label.setAcceptHoverEvents(False)

			self.addToGroup(self.label)
	
	def _get_node_text_color(self, flowchart_item:QGraphicsItem):

		background_color = flowchart_item.brush().color()

		# Calculate the luminance using the formula: Y = 0.299*R + 0.587*G + 0.114*B
		luminance = 0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()

		# Choose the text color based on the luminance
		if luminance > 128:
			return QColor(Qt.black)
		else:
			return QColor(Qt.white)
		
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

		self.set_label(self.item, painter_path.pointAtPercent(0.5), self.color)
	
	def set_color(self, color:QColor):
		self.arrow.setBrush(color)
		self.arrow.setPen(QPen(QBrush(color), 1, Qt.SolidLine))
		self.line.setPen(QPen(color, 1, Qt.SolidLine))
		self.label.setDefaultTextColor(color)


class GraphvizFlowchartDecision(GraphvizFlowchartItem):
	def __init__(self, flowchart_height:float, xml_polygon: str, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(flowchart_height, xml_text, parent)

		self.setAcceptHoverEvents(True)

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
		self.item.setBrush(self.color)
		self.item.setPen(QPen(QBrush(self.color), 0, Qt.SolidLine))
		self.item.setAcceptHoverEvents(False)

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

class GraphvizFlowchartProcess(GraphvizFlowchartItem):
	def __init__(self, flowchart_height:float, xml_ellipse: str, xml_text:str = "", parent: QGraphicsItem = None):
		super().__init__(flowchart_height, xml_text, parent)

		self.setAcceptHoverEvents(True)

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
		self.item.setBrush(self.color)
		self.item.setPen(QPen(QBrush(self.color), 0, Qt.SolidLine))
		self.item.setAcceptHoverEvents(False)

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