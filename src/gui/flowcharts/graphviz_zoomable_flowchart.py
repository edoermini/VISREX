
import xml.etree.ElementTree as ET
from graphviz import Digraph
import io
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsItem, QGraphicsTextItem, QGraphicsPathItem
from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPolygonF, QPainterPath, QFont, QColor, QPen
import xml.etree.ElementTree as ET
import re


from .flowchart_items import FlowchartEllipse, FlowchartPolygon

class GraphvizZoomableFlowchart(QGraphicsView):
    def __init__(self, dot:Digraph, edges_color:str = None):
        super().__init__()

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

        self.edges : list[tuple[QGraphicsPathItem, FlowchartPolygon]] = [] # edges are made by a line and an arrow
        self.nodes : dict[str,FlowchartEllipse | FlowchartPolygon] = {}
        self.edges_labels : list[QGraphicsTextItem] = []

        self.viewbox : list[float] = [] # [min_x, min_y, width, height]

        self.draw_flowchart()
    
    def draw_flowchart(self):
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
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)
    
    def set_edges_color(self, color:str):
        self.edges_color = color
        
        for edge in self.edges:
            line = edge[0]
            arrow = edge[1]
            
            arrow.set_color(QColor(color))

            pen_color = QColor(self.edges_color)  # Red color
            line.setPen(QPen(pen_color, 1, Qt.SolidLine))
        
        for edge_label in self.edges_labels:
            edge_label.setDefaultTextColor(QColor(color))


    def _draw_edges(self, edges : list[ET.Element]):
        
        for edge in edges:

            path = edge.find('.//{http://www.w3.org/2000/svg}path')
            polygon = edge.find('.//{http://www.w3.org/2000/svg}polygon')
            text = edge.find('.//{http://www.w3.org/2000/svg}text')
            
            points = polygon.get('points').split(' ')
            polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1]) + self.viewbox[3]) for point in points ]

            painter_path = QPainterPath()

            path_str = path.get('d')
            commands = re.findall(r'([MC])([^MC]*)', path_str)

            for command, args_str in commands:
                args = [float(arg) if i%2 == 0 else float(arg) + self.viewbox[3] for i, arg in enumerate(args_str.replace(',', ' ').split())]
                
                print(args)

                if command == 'M':
                    painter_path.moveTo(*args)
                elif command == 'C':
                    for i in range(0, len(args), 6):
                        painter_path.cubicTo(*args[i:i+6])

            path_item = QGraphicsPathItem(painter_path)
            path_item.setZValue(0)
            self.gscene.addItem(path_item)
            
            pen_color = QColor(self.edges_color)  # Red color
            path_item.setPen(QPen(pen_color, 1, Qt.SolidLine))

            polygon_figure = QPolygonF([QPointF(x, y) for x, y in polygon_points])
            polygon_item = FlowchartPolygon(polygon_figure, hex_color=self.edges_color)
            polygon_item.setZValue(0)
            self.gscene.addItem(polygon_item)

            self.edges.append((path_item, polygon_item))

            center_point = painter_path.pointAtPercent(0.5)

            if text is not None:
                node_label = QGraphicsTextItem(text.text)
                node_label.setZValue(1)
                node_label.setFont(QFont('Arial', pointSize=self.font_size))
                node_label.setDefaultTextColor(QColor(self.edges_color))

                self.gscene.addItem(node_label)
            
                text_x = (center_point.x() - node_label.boundingRect().width() / 2)
                text_y = (center_point.y() - node_label.boundingRect().height() / 2)

                node_label.setPos(text_x, text_y)

                self.edges_labels.append(node_label)
    
    def _draw_decision_nodes(self, decision_nodes : list[ET.Element]):

        for decision_node in decision_nodes:
            
            polygon = decision_node.find('.//{http://www.w3.org/2000/svg}polygon')
            text = decision_node.find('.//{http://www.w3.org/2000/svg}text')
            title = decision_node.find('.//{http://www.w3.org/2000/svg}title')

            background_color = polygon.get('fill')

            points = polygon.get('points').split(' ')
            polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1]) + self.viewbox[3]) for point in points ]

            polygon_figure = QPolygonF([QPointF(x, y) for x, y in polygon_points])
            polygon_item = FlowchartPolygon(polygon_figure, hex_color=background_color)

            polygon_item.setZValue(0)
            self.gscene.addItem(polygon_item)

            self.nodes[title.text] = polygon_item

            if text is not None:
                node_label = QGraphicsTextItem(text.text)
                node_label.setZValue(1)

                node_label.setFont(QFont('Arial', pointSize=self.font_size))
                
                node_label.setDefaultTextColor(self._get_node_text_color(background_color))

                self.gscene.addItem(node_label)
                
                text_x = (polygon_item.boundingRect().center().x() - node_label.boundingRect().width() / 2)
                text_y = (polygon_item.boundingRect().center().y() - node_label.boundingRect().height() / 2)

                node_label.setPos(text_x, text_y)

    def _draw_nodes(self, nodes : list[ET.Element]):

        for node in nodes:

            ellipse = node.find('.//{http://www.w3.org/2000/svg}ellipse')
            text = node.find('.//{http://www.w3.org/2000/svg}text')
            title = node.find('.//{http://www.w3.org/2000/svg}title')

            background_color = ellipse.get('fill')

            x = (float(ellipse.get('cx')) - float(ellipse.get('rx')))
            y = (float(ellipse.get('cy')) + self.viewbox[3]) - float(ellipse.get('ry'))
            width = float(ellipse.get('rx'))*2
            height = float(ellipse.get('ry'))*2

            ellipse_item = FlowchartEllipse(x, y, width, height, hex_color=background_color)  # (x, y, width, height)
            ellipse_item.setZValue(0)
            self.gscene.addItem(ellipse_item)

            self.nodes[title.text] = ellipse_item

            if text is not None:
                node_label = QGraphicsTextItem(text.text)
                node_label.setZValue(1)
                
                node_label.setFont(QFont('Arial', pointSize=self.font_size))

                node_label.setDefaultTextColor(self._get_node_text_color(background_color))
                self.gscene.addItem(node_label)
                
                text_x = (ellipse_item.boundingRect().center().x() - node_label.boundingRect().width() / 2)
                text_y = (ellipse_item.boundingRect().center().y() - node_label.boundingRect().height() / 2)

                node_label.setPos(text_x, text_y)

    def _get_node_text_color(self, hex_bg_color : str):

        background_color = QColor(hex_bg_color)

        # Calculate the luminance using the formula: Y = 0.299*R + 0.587*G + 0.114*B
        luminance = 0.299 * background_color.red() + 0.587 * background_color.green() + 0.114 * background_color.blue()

        # Choose the text color based on the luminance
        if luminance > 128:
            return QColor(Qt.black)
        else:
            return QColor(Qt.white)
    
    def set_opacity(self, opacity: float, node_id : str = None):
        if not node_id:
            for _, node in self.nodes.items():
                node.setOpacity(opacity)
        
        else:
            self.nodes[node_id].setOpacity(opacity)
