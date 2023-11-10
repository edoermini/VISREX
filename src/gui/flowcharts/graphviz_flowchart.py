
import xml.etree.ElementTree as ET
from graphviz import Digraph
import io
from PyQt6.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsTextItem, QMenu
from PyQt6.QtCore import Qt, QObject, pyqtSignal, QPoint
from PyQt6.QtGui import QColor
import xml.etree.ElementTree as ET
import re


from .graphviz_flowchart_items import GraphvizFlowchartEdge, GraphvizFlowchartDecision, GraphvizFlowchartProcess

class GraphzivFlowchartSignals(QObject):
	rightClick = pyqtSignal(str, QPoint)

class GraphvizFlowchart(QGraphicsView):
	def __init__(self, dot:Digraph, edges_color:QColor = QColor("#00000"), parent = None):
		super().__init__(parent=parent)

		self.signals = GraphzivFlowchartSignals()

		svg_file = dot.pipe(format='svg')
		svg_stream = io.BytesIO(svg_file)

		tree = ET.parse(svg_stream)
		root = tree.getroot()
		for elem in root.iter():
			if 'fill' in elem.attrib and elem.attrib['fill'] == 'white':
				elem.attrib['fill'] = 'none'

		new_svg = io.BytesIO()
		tree.write(new_svg)
		new_svg.seek(0)

		self.svg = new_svg.read().decode('utf-8')

		self.gscene = QGraphicsScene()

		self.font_size = 6
		self.edges_color = edges_color

		self.edges : list[GraphvizFlowchartEdge] = [] # edges are made by a line and an arrow
		self.nodes : dict[str,GraphvizFlowchartProcess | GraphvizFlowchartDecision] = {}
		self.edges_labels : list[QGraphicsTextItem] = []

		self.viewbox : list[float] = [] # [min_x, min_y, width, height]

		self._draw_flowchart()
	
	def wheelEvent(self, event):
		factor = 1.1
		if event.modifiers() == Qt.ControlModifier:
			if event.angleDelta().y() < 0:
				factor = 1.0 / factor
			self.scale(factor, factor)
		elif event.modifiers() == Qt.ShiftModifier:
			delta = event.angleDelta().y()
			self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() + int(delta))
		else:
			super().wheelEvent(event)
	
	def setEdgesColor(self, color:QColor):

		self.edges_color = color
		
		for edge in self.edges:
			edge.setColor(self.edges_color)
	
	def _draw_flowchart(self):
		self.setScene(self.gscene)

		# Parse SVG content
		root = ET.fromstring(self.svg)

		self.viewbox = [float(element) for element in root.get('viewBox').split(' ')]

		graph_element = root.find('.//{http://www.w3.org/2000/svg}g[@id="graph0"]')

		g_elements = graph_element.findall('.//{http://www.w3.org/2000/svg}g')

		edges = filter(lambda x: x.find('.//{http://www.w3.org/2000/svg}path') is not None, g_elements)
		decision_nodes = filter(lambda x: x.find('.//{http://www.w3.org/2000/svg}path') is None and x.find('.//{http://www.w3.org/2000/svg}polygon') is not None, g_elements)
		nodes = filter(lambda x: x.find('.//{http://www.w3.org/2000/svg}ellipse') is not None, g_elements)

		self._draw_nodes(nodes)
		self._draw_edges(edges)
		self._draw_decision_nodes(decision_nodes)
		
	def _draw_edges(self, edges : list[ET.Element]):
		
		for edge in edges:

			path = edge.find('.//{http://www.w3.org/2000/svg}path')
			polygon = edge.find('.//{http://www.w3.org/2000/svg}polygon')
			text = edge.find('.//{http://www.w3.org/2000/svg}text')

			xml_path_str = ""
			xml_polygon_str = ""
			xml_text_str = ""

			if path is not None:
				xml_path_str = ET.tostring(path, encoding='unicode')
			
			if polygon is not None:
				xml_polygon_str = ET.tostring(polygon, encoding='unicode')
			
			if text is not None:
				xml_text_str = ET.tostring(text, encoding='unicode')
			
			flowchart_edge = GraphvizFlowchartEdge(self.viewbox[3], xml_path_str, xml_polygon_str, self.edges_color, xml_text_str)
			
			self.gscene.addItem(flowchart_edge)
			self.edges.append(flowchart_edge)
	
	def _draw_decision_nodes(self, decision_nodes : list[ET.Element]):

		for decision_node in decision_nodes:
			
			polygon = decision_node.find('.//{http://www.w3.org/2000/svg}polygon')
			text = decision_node.find('.//{http://www.w3.org/2000/svg}text')
			title = decision_node.find('.//{http://www.w3.org/2000/svg}title')

			if polygon is not None:
				xml_polygon_str = ET.tostring(polygon, encoding='unicode')
			
			if text is not None:
				xml_text_str = ET.tostring(text, encoding='unicode')
			
			flowchart_node = GraphvizFlowchartDecision(title.text, self.viewbox[3], xml_polygon_str, xml_text_str)
			flowchart_node.signals.rightClick.connect(self.nodeRightClick)

			self.gscene.addItem(flowchart_node)

			self.nodes[title.text] = flowchart_node

	def _draw_nodes(self, nodes : list[ET.Element]):

		for node in nodes:

			ellipse = node.find('.//{http://www.w3.org/2000/svg}ellipse')
			text = node.find('.//{http://www.w3.org/2000/svg}text')
			title = node.find('.//{http://www.w3.org/2000/svg}title')

			xml_ellipse_str = ""
			xml_text_str = ""

			if ellipse is not None:
				xml_ellipse_str = ET.tostring(ellipse, encoding='unicode')
			
			if text is not None:
				xml_text_str = ET.tostring(text, encoding='unicode')
			
			flowchart_node = GraphvizFlowchartProcess(title.text, self.viewbox[3], xml_ellipse_str, xml_text_str)
			flowchart_node.signals.rightClick.connect(self.nodeRightClick)
			self.gscene.addItem(flowchart_node)

			self.nodes[title.text] = flowchart_node

	def setOpacity(self, opacity: float, node_id : str = None):
		if not node_id:
			for _, flowchart_item in self.nodes.items():
				flowchart_item.setOpacity(opacity)
		
		else:
			self.nodes[node_id].setOpacity(opacity)
	
	def nodeRightClick(self, node_id, mouse_pos):
		self.signals.rightClick.emit(node_id, mouse_pos)
