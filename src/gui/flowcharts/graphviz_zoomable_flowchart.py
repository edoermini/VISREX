
import xml.etree.ElementTree as ET
from graphviz import Digraph
import io
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QApplication, QGraphicsPathItem
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

        self.edges_color = edges_color

        self.draw_scene()
    
    def draw_scene(self):
        self.setScene(self.gscene)

        # Parse SVG content
        root = ET.fromstring(self.svg)

        # [min_x, min_y, width, height]
        viewbox = [float(element) for element in root.get('viewBox').split(' ')]

        graph_element = root.find('.//{http://www.w3.org/2000/svg}g[@id="graph0"]')

        # Iterate through <g> elements and add them as separate items
        for g_element in graph_element.findall('.//{http://www.w3.org/2000/svg}g'):
            
            text = g_element.find(".//{http://www.w3.org/2000/svg}text")
            
            text_x = 0
            text_y = 0

            if text is not None:
                text_x = float(text.get('x'))
                text_y = float(text.get('y')) + viewbox[3]
                node_label = QGraphicsTextItem(text.text)
                node_label.setZValue(1)
                node_label.setFont(QFont('Arial'))
                self.gscene.addItem(node_label)

            ellipse = g_element.find('.//{http://www.w3.org/2000/svg}ellipse')
            polygon = g_element.find('.//{http://www.w3.org/2000/svg}polygon')

            if ellipse is not None:
                x = (float(ellipse.get('cx')) - float(ellipse.get('rx')))
                y = (float(ellipse.get('cy')) + viewbox[3]) - float(ellipse.get('ry'))
                width = float(ellipse.get('rx'))*2
                height = float(ellipse.get('ry'))*2

                ellipse_item = FlowchartEllipse(x, y, width, height, hex_color=ellipse.get('fill'))  # (x, y, width, height)
                ellipse_item.setZValue(0)
                self.gscene.addItem(ellipse_item)

                text_x = (ellipse_item.boundingRect().center().x() - node_label.boundingRect().width() / 2)
                text_y = (ellipse_item.boundingRect().center().y() - node_label.boundingRect().height() / 2)

            elif polygon is not None:
                points = polygon.get('points').split(' ')
            
                # (bottom, left, top, right)
                polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1]) + viewbox[3]) for point in points ]

                path = g_element.find('.//{http://www.w3.org/2000/svg}path')

                if path is not None:
                    print(path)
                    
                    painter_path = QPainterPath()

                    path_str = path.get('d')
                    commands = re.findall(r'([MC])([^MC]*)', path_str)

                    for command, args_str in commands:
                        args = [float(arg) if i%2 == 0 else float(arg) + viewbox[3] for i, arg in enumerate(args_str.replace(',', ' ').split())]
                        
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

                    center_point = painter_path.pointAtPercent(0.5)
                    
                    text_x = (center_point.x() - node_label.boundingRect().width() / 2)
                    text_y = (center_point.y() - node_label.boundingRect().height() / 2)
                
                else:
                    polygon_figure = QPolygonF([QPointF(x, y) for x, y in polygon_points])
                    polygon_item = FlowchartPolygon(polygon_figure, hex_color=polygon.get('fill'))
                    polygon_item.setZValue(0)
                    self.gscene.addItem(polygon_item)

                    text_x = (polygon_item.boundingRect().center().x() - node_label.boundingRect().width() / 2)
                    text_y = (polygon_item.boundingRect().center().y() - node_label.boundingRect().height() / 2)

            if text is not None:
                node_label.setPos(text_x, text_y)  # Adjust position based on the ellipse
    
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            factor = 1.2
            if event.angleDelta().y() < 0:
                factor = 1.0 / factor
            self.scale(factor, factor)
        else:
            super().wheelEvent(event)
    
    def set_edges_color(self, color):
        self.edges_color = color
        self.draw_scene()