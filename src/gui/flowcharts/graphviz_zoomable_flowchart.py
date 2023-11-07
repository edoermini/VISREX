import subprocess
import tempfile
import xml.etree.ElementTree as ET
from graphviz import Digraph
import io

from .zoomable_flowchart import ZoomableFlowchart

class GraphvizZoomableFlowchart(ZoomableFlowchart):
    def __init__(self, dot:Digraph):

        svg_file = dot.pipe(format='svg')
        print(svg_file)
        svg_stream = io.BytesIO(svg_file)

        tree = ET.parse(svg_stream)
        root = tree.getroot()
        for elem in root.iter():
            if 'fill' in elem.attrib and elem.attrib['fill'] == 'white':
                elem.attrib['fill'] = 'none'

        new_svg = io.BytesIO()
        tree.write(new_svg)

        new_svg.seek(0)

        super().__init__(new_svg)