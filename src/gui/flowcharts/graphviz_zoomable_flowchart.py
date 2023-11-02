import subprocess
import tempfile
import xml.etree.ElementTree as ET

from .zoomable_flowchart import ZoomableFlowchart 

class GraphvizZoomableFlowchart(ZoomableFlowchart):
    def __init__(self, dot_code):

        self.tmp_dir = tempfile.TemporaryDirectory()
        svg_file = f"{self.tmp_dir.name}/flowchart.svg"
        
        with open(f"{self.tmp_dir.name}/flowchart.dot", "w") as dot_file:
            dot_file.write(dot_code)

        # Use Graphviz to generate the SVG file
        subprocess.run(["dot", "-Tsvg", "-o", svg_file, f"{self.tmp_dir.name}/flowchart.dot"], check=True)

        tree = ET.parse(svg_file)
        root = tree.getroot()
        for elem in root.iter():
            if 'fill' in elem.attrib and elem.attrib['fill'] == 'white':
                elem.attrib['fill'] = 'none'

        tree.write(svg_file)

        super().__init__(svg_file)
        
        self.tmp_dir.cleanup()