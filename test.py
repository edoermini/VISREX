import sys
import typing
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsSceneHoverEvent, QGraphicsSceneMouseEvent, QGraphicsView, QGraphicsEllipseItem, QGraphicsPolygonItem, QGraphicsTextItem, QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QPen, QBrush
from PyQt5.QtSvg import QGraphicsSvgItem, QSvgRenderer
import io
import xml.etree.ElementTree as ET
import re

class SVGItem(QGraphicsSvgItem):
    def __init__(self, svg, node_id, ax, ay):

        self.node_id = node_id

        svg_renderer = QSvgRenderer(io.BytesIO(svg.encode()).read())
        svg_item = QGraphicsSvgItem()
        svg_item.setSharedRenderer(svg_renderer)
        svg_item.setElementId(self.node_id)
        svg_item.setPos(ax, ay)
    
    def mouseDoubleClickEvent(self, event: QGraphicsSceneMouseEvent | None) -> None:
        print(f"clicked {self.node_id}")
        return super().mouseDoubleClickEvent(event)

class ClickableSVGViewer(QGraphicsView):
    def __init__(self, svg_path):
        super(ClickableSVGViewer, self).__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        svg_content = svg_path.read()

        # Parse SVG content
        root = ET.fromstring(svg_content)

        print(svg_content)

        # [min_x, min_y, width, height]
        self.viewbox = [float(element) for element in root.get('viewBox').split(' ')]

        graph_element = root.find('.//{http://www.w3.org/2000/svg}g[@id="graph0"]')

        last_2_nodes = []

        # Iterate through <g> elements and add them as separate items
        for g_element in graph_element.findall('.//{http://www.w3.org/2000/svg}g'):
            
            text = g_element.find(".//{http://www.w3.org/2000/svg}text")

            if text is not None:
                print(text.text)
            ax = 0
            ay = 0

            print(g_element.text)
            ellipse = g_element.find('.//{http://www.w3.org/2000/svg}ellipse')
            polygon = g_element.find('.//{http://www.w3.org/2000/svg}polygon')

            if ellipse is not None:
                ax = (float(ellipse.get('cx')) - float(ellipse.get('rx')))
                ay = (float(ellipse.get('cy')) + self.viewbox[3]) - float(ellipse.get('ry'))

                if len(last_2_nodes) == 2:
                    last_2_nodes.pop(0)


                last_2_nodes.append((ay, ay + 2*float(ellipse.get('ry'))))
                
            elif polygon is not None:
                points = polygon.get('points').split(' ')
            
                # (bottom, left, top, right)
                polygon_points = [ (float(point.split(',')[0]), float(point.split(',')[1])) for point in points ]

                path = g_element.find('.//{http://www.w3.org/2000/svg}path')

                if path is not None:
                    print(path)
                    print(last_2_nodes)

                    matched = re.match(r'M(-?\d+\.?\d{0,2}),(-?\d+\.?\d{0,2}).*\s(-?\d+\.?\d{0,2}),(-?\d+\.?\d{0,2})', path.get('d'))
                    print(path.get('d'))

                    start_x = float(matched.group(1))
                    start_y = float(matched.group(2))
                    end_x = float(matched.group(3))
                    end_y = float(matched.group(4))

                    ax = start_x if start_x < end_x else end_x

                    if start_y > end_y:
                        ay =  polygon_points[1][1] + self.viewbox[3]
                    else:
                        ay =  start_y + self.viewbox[3]

                else:
                    ax = polygon_points[1][0]
                    ay = polygon_points[2][1] + self.viewbox[3] - abs(polygon_points[2][1] - polygon_points[0][1])
                    
                    if len(last_2_nodes) == 2:
                        last_2_nodes.pop(0)

                    last_2_nodes.append((ay, ay + abs(polygon_points[2][1] - polygon_points[0][1])))

            print(ax, ay)

            svg_item_content = f"<svg>{ET.tostring(g_element, encoding='utf-8').decode('utf-8')}</svg>"
            svg_renderer = QSvgRenderer(io.BytesIO(svg_item_content.encode()).read())
            svg_item = QGraphicsSvgItem()
            svg_item.setSharedRenderer(svg_renderer)
            svg_item.setElementId(g_element.get('id', ''))

            svg_item.setPos(ax, ay)

            self.scene.addItem(svg_item)

        # Iterate through items in the SVG and make them clickable
        for item in self.scene.items():
            item.setAcceptHoverEvents(True)
            item.hoverEnterEvent = self.hoverEnterEvent
            item.hoverLeaveEvent = self.hoverLeaveEvent
            item.mousePressEvent = self.mousePressEvent

    def hoverEnterEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item:
            for child_item in item.childItems():
                child_item.setOpacity(0.5)

    def hoverLeaveEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item:
            for child_item in item.childItems():
                child_item.setOpacity(1.0)

    def mousePressEvent(self, event):
        item = self.scene.itemAt(event.pos(), self.transform())
        if item:
            print("Clicked on:", item.elementId())

if __name__ == '__main__':
    svg = b'''
<svg width="854pt" height="2287pt" viewBox="0.00 0.00 854.00 2287.00"
    xmlns="http://www.w3.org/2000/svg"
    xmlns:xlink="http://www.w3.org/1999/xlink">
    <g id="graph0" class="graph" transform="scale(1 1) rotate(0) translate(4 2283)">
        <title>%3</title>
        <polygon fill="white" stroke="transparent" points="-4,4 -4,-2283 850,-2283 850,4 -4,4"/>
        <!-- start -->
        <g id="node1" class="node">
            <title>start</title>
            <ellipse fill="#4051b5" stroke="black" cx="565.47" cy="-2261" rx="75.29" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-2257.3" font-family="Arial" font-size="14.00">Malware sample</text>
        </g>
        <!-- extr_0 -->
        <g id="node2" class="node">
            <title>extr_0</title>
            <polygon fill="#4051b5" stroke="black" points="565.47,-2206 436.6,-2188 565.47,-2170 694.33,-2188 565.47,-2206"/>
            <text text-anchor="middle" x="565.47" y="-2184.3" font-family="Arial" font-size="14.00">Hidden from WinAPI</text>
        </g>
        <!-- start&#45;&gt;extr_0 -->
        <g id="edge1" class="edge">
            <title>start&#45;&gt;extr_0</title>
            <path fill="none" stroke="black" d="M565.47,-2242.81C565.47,-2234.79 565.47,-2225.05 565.47,-2216.07"/>
            <polygon fill="black" stroke="black" points="568.97,-2216.03 565.47,-2206.03 561.97,-2216.03 568.97,-2216.03"/>
        </g>
        <!-- extr_1 -->
        <g id="node3" class="node">
            <title>extr_1</title>
            <ellipse fill="#4051b5" stroke="black" cx="470.47" cy="-2101" rx="91.78" ry="18"/>
            <text text-anchor="middle" x="470.47" y="-2097.3" font-family="Arial" font-size="14.00">Automatic Extraction</text>
        </g>
        <!-- extr_0&#45;&gt;extr_1 -->
        <g id="edge2" class="edge">
            <title>extr_0&#45;&gt;extr_1</title>
            <path fill="none" stroke="black" d="M548.92,-2172.19C534.57,-2159.36 513.56,-2140.56 496.89,-2125.64"/>
            <polygon fill="black" stroke="black" points="498.89,-2122.73 489.1,-2118.67 494.22,-2127.95 498.89,-2122.73"/>
            <text text-anchor="middle" x="535.97" y="-2140.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- extr_2 -->
        <g id="node4" class="node">
            <title>extr_2</title>
            <ellipse fill="#4051b5" stroke="black" cx="661.47" cy="-2101" rx="81.49" ry="18"/>
            <text text-anchor="middle" x="661.47" y="-2097.3" font-family="Arial" font-size="14.00">Manual Extraction</text>
        </g>
        <!-- extr_0&#45;&gt;extr_2 -->
        <g id="edge3" class="edge">
            <title>extr_0&#45;&gt;extr_2</title>
            <path fill="none" stroke="black" d="M582.19,-2172.19C596.68,-2159.36 617.92,-2140.56 634.77,-2125.64"/>
            <polygon fill="black" stroke="black" points="637.47,-2127.92 642.64,-2118.67 632.83,-2122.68 637.47,-2127.92"/>
            <text text-anchor="middle" x="627.47" y="-2140.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- extr_3 -->
        <g id="node5" class="node">
            <title>extr_3</title>
            <ellipse fill="#4051b5" stroke="black" cx="565.47" cy="-2028" rx="89.08" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-2024.3" font-family="Arial" font-size="14.00">Extract from archive</text>
        </g>
        <!-- extr_1&#45;&gt;extr_3 -->
        <g id="edge4" class="edge">
            <title>extr_1&#45;&gt;extr_3</title>
            <path fill="none" stroke="black" d="M492.98,-2083.17C505.61,-2073.73 521.54,-2061.83 535.24,-2051.59"/>
            <polygon fill="black" stroke="black" points="537.53,-2054.25 543.44,-2045.46 533.34,-2048.64 537.53,-2054.25"/>
        </g>
        <!-- extr_2&#45;&gt;extr_3 -->
        <g id="edge5" class="edge">
            <title>extr_2&#45;&gt;extr_3</title>
            <path fill="none" stroke="black" d="M639.2,-2083.53C626.45,-2074.1 610.26,-2062.13 596.3,-2051.8"/>
            <polygon fill="black" stroke="black" points="598.06,-2048.76 587.94,-2045.62 593.9,-2054.38 598.06,-2048.76"/>
        </g>
        <!-- pran_0 -->
        <g id="node6" class="node">
            <title>pran_0</title>
            <ellipse fill="#ea8aba" stroke="black" cx="565.47" cy="-1955" rx="75.29" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-1951.3" font-family="Arial" font-size="14.00">Identify the hash</text>
        </g>
        <!-- extr_3&#45;&gt;pran_0 -->
        <g id="edge6" class="edge">
            <title>extr_3&#45;&gt;pran_0</title>
            <path fill="none" stroke="black" d="M565.47,-2009.81C565.47,-2001.79 565.47,-1992.05 565.47,-1983.07"/>
            <polygon fill="black" stroke="black" points="568.97,-1983.03 565.47,-1973.03 561.97,-1983.03 568.97,-1983.03"/>
        </g>
        <!-- pran_1 -->
        <g id="node7" class="node">
            <title>pran_1</title>
            <ellipse fill="#ea8aba" stroke="black" cx="565.47" cy="-1882" rx="84.49" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-1878.3" font-family="Arial" font-size="14.00">Check for malware</text>
        </g>
        <!-- pran_0&#45;&gt;pran_1 -->
        <g id="edge7" class="edge">
            <title>pran_0&#45;&gt;pran_1</title>
            <path fill="none" stroke="black" d="M565.47,-1936.81C565.47,-1928.79 565.47,-1919.05 565.47,-1910.07"/>
            <polygon fill="black" stroke="black" points="568.97,-1910.03 565.47,-1900.03 561.97,-1910.03 568.97,-1910.03"/>
        </g>
        <!-- pran_2 -->
        <g id="node8" class="node">
            <title>pran_2</title>
            <ellipse fill="#ea8aba" stroke="black" cx="565.47" cy="-1809" rx="93.68" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-1805.3" font-family="Arial" font-size="14.00">Data in open sources</text>
        </g>
        <!-- pran_1&#45;&gt;pran_2 -->
        <g id="edge8" class="edge">
            <title>pran_1&#45;&gt;pran_2</title>
            <path fill="none" stroke="black" d="M565.47,-1863.81C565.47,-1855.79 565.47,-1846.05 565.47,-1837.07"/>
            <polygon fill="black" stroke="black" points="568.97,-1837.03 565.47,-1827.03 561.97,-1837.03 568.97,-1837.03"/>
        </g>
        <!-- pran_3 -->
        <g id="node9" class="node">
            <title>pran_3</title>
            <ellipse fill="#ea8aba" stroke="black" cx="565.47" cy="-1736" rx="55.49" ry="18"/>
            <text text-anchor="middle" x="565.47" y="-1732.3" font-family="Arial" font-size="14.00">Text strings</text>
        </g>
        <!-- pran_2&#45;&gt;pran_3 -->
        <g id="edge9" class="edge">
            <title>pran_2&#45;&gt;pran_3</title>
            <path fill="none" stroke="black" d="M565.47,-1790.81C565.47,-1782.79 565.47,-1773.05 565.47,-1764.07"/>
            <polygon fill="black" stroke="black" points="568.97,-1764.03 565.47,-1754.03 561.97,-1764.03 568.97,-1764.03"/>
        </g>
        <!-- unpk_0 -->
        <g id="node10" class="node">
            <title>unpk_0</title>
            <ellipse fill="#2cd551" stroke="black" cx="371.47" cy="-1663" rx="136.48" ry="18"/>
            <text text-anchor="middle" x="371.47" y="-1659.3" font-family="Arial" font-size="14.00">Detection of packers or chiphers</text>
        </g>
        <!-- pran_3&#45;&gt;unpk_0 -->
        <g id="edge10" class="edge">
            <title>pran_3&#45;&gt;unpk_0</title>
            <path fill="none" stroke="black" d="M529.88,-1721.98C500.51,-1711.23 458.38,-1695.81 424.95,-1683.57"/>
            <polygon fill="black" stroke="black" points="425.92,-1680.2 415.32,-1680.05 423.51,-1686.78 425.92,-1680.2"/>
        </g>
        <!-- unpk_1 -->
        <g id="node11" class="node">
            <title>unpk_1</title>
            <polygon fill="#2cd551" stroke="black" points="233.47,-1608 0.03,-1590 233.47,-1572 466.9,-1590 233.47,-1608"/>
            <text text-anchor="middle" x="233.47" y="-1586.3" font-family="Arial" font-size="14.00">Obfuscated/Compressed or encrypted?</text>
        </g>
        <!-- unpk_0&#45;&gt;unpk_1 -->
        <g id="edge11" class="edge">
            <title>unpk_0&#45;&gt;unpk_1</title>
            <path fill="none" stroke="black" d="M339.11,-1645.35C318.85,-1634.93 292.64,-1621.45 271.4,-1610.52"/>
            <polygon fill="black" stroke="black" points="272.83,-1607.32 262.33,-1605.85 269.63,-1613.54 272.83,-1607.32"/>
        </g>
        <!-- unpk_2 -->
        <g id="node12" class="node">
            <title>unpk_2</title>
            <ellipse fill="#2cd551" stroke="black" cx="391.47" cy="-1503" rx="145.67" ry="18"/>
            <text text-anchor="middle" x="391.47" y="-1499.3" font-family="Arial" font-size="14.00">Automatic decryption or unpacking</text>
        </g>
        <!-- unpk_1&#45;&gt;unpk_2 -->
        <g id="edge12" class="edge">
            <title>unpk_1&#45;&gt;unpk_2</title>
            <path fill="none" stroke="black" d="M261.35,-1574C286.45,-1560.5 323.62,-1540.5 351.81,-1525.33"/>
            <polygon fill="black" stroke="black" points="353.47,-1528.41 360.62,-1520.59 350.15,-1522.25 353.47,-1528.41"/>
            <text text-anchor="middle" x="333.97" y="-1542.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- imgc_0 -->
        <g id="node16" class="node">
            <title>imgc_0</title>
            <ellipse fill="#05a8f4" stroke="black" cx="482.47" cy="-1183" rx="69.59" ry="18"/>
            <text text-anchor="middle" x="482.47" y="-1179.3" font-family="Arial" font-size="14.00">Digital material</text>
        </g>
        <!-- unpk_1&#45;&gt;imgc_0 -->
        <g id="edge13" class="edge">
            <title>unpk_1&#45;&gt;imgc_0</title>
            <path fill="none" stroke="black" d="M228.4,-1572.24C223.72,-1555.22 217.47,-1528.03 217.47,-1504 217.47,-1504 217.47,-1504 217.47,-1269 217.47,-1228.37 331.86,-1204.43 410.33,-1192.8"/>
            <polygon fill="black" stroke="black" points="411.27,-1196.2 420.67,-1191.3 410.27,-1189.27 411.27,-1196.2"/>
            <text text-anchor="middle" x="226.47" y="-1382.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- unpk_3 -->
        <g id="node13" class="node">
            <title>unpk_3</title>
            <polygon fill="#2cd551" stroke="black" points="459.47,-1448 245.14,-1430 459.47,-1412 673.79,-1430 459.47,-1448"/>
            <text text-anchor="middle" x="459.47" y="-1426.3" font-family="Arial" font-size="14.00">Has it been decrypted or unpacked?</text>
        </g>
        <!-- unpk_2&#45;&gt;unpk_3 -->
        <g id="edge14" class="edge">
            <title>unpk_2&#45;&gt;unpk_3</title>
            <path fill="none" stroke="black" d="M407.93,-1484.81C416.7,-1475.66 427.61,-1464.26 437.14,-1454.32"/>
            <polygon fill="black" stroke="black" points="439.7,-1456.7 444.09,-1447.06 434.64,-1451.86 439.7,-1456.7"/>
        </g>
        <!-- unpk_3&#45;&gt;pran_3 -->
        <g id="edge15" class="edge">
            <title>unpk_3&#45;&gt;pran_3</title>
            <path fill="none" stroke="black" d="M509.05,-1443.9C536.64,-1454.39 565.47,-1472.43 565.47,-1502 565.47,-1664 565.47,-1664 565.47,-1664 565.47,-1678.35 565.47,-1694.33 565.47,-1707.49"/>
            <polygon fill="black" stroke="black" points="561.97,-1707.78 565.47,-1717.78 568.97,-1707.78 561.97,-1707.78"/>
            <text text-anchor="middle" x="576.97" y="-1586.3" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- unpk_4 -->
        <g id="node14" class="node">
            <title>unpk_4</title>
            <ellipse fill="#2cd551" stroke="black" cx="480.47" cy="-1343" rx="135.68" ry="18"/>
            <text text-anchor="middle" x="480.47" y="-1339.3" font-family="Arial" font-size="14.00">Manual decryption or unpacking</text>
        </g>
        <!-- unpk_3&#45;&gt;unpk_4 -->
        <g id="edge16" class="edge">
            <title>unpk_3&#45;&gt;unpk_4</title>
            <path fill="none" stroke="black" d="M463.61,-1412.21C466.53,-1400.41 470.49,-1384.38 473.84,-1370.82"/>
            <polygon fill="black" stroke="black" points="477.25,-1371.6 476.25,-1361.05 470.46,-1369.92 477.25,-1371.6"/>
            <text text-anchor="middle" x="480.47" y="-1382.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- unpk_5 -->
        <g id="node15" class="node">
            <title>unpk_5</title>
            <polygon fill="#2cd551" stroke="black" points="482.47,-1288 268.14,-1270 482.47,-1252 696.79,-1270 482.47,-1288"/>
            <text text-anchor="middle" x="482.47" y="-1266.3" font-family="Arial" font-size="14.00">Has it been decrypted or unpacked?</text>
        </g>
        <!-- unpk_4&#45;&gt;unpk_5 -->
        <g id="edge17" class="edge">
            <title>unpk_4&#45;&gt;unpk_5</title>
            <path fill="none" stroke="black" d="M480.95,-1324.81C481.18,-1316.79 481.45,-1307.05 481.7,-1298.07"/>
            <polygon fill="black" stroke="black" points="485.2,-1298.12 481.99,-1288.03 478.21,-1297.93 485.2,-1298.12"/>
        </g>
        <!-- unpk_5&#45;&gt;pran_3 -->
        <g id="edge18" class="edge">
            <title>unpk_5&#45;&gt;pran_3</title>
            <path fill="none" stroke="black" d="M560.91,-1281.49C623.75,-1292.16 701.47,-1311.52 701.47,-1342 701.47,-1664 701.47,-1664 701.47,-1664 701.47,-1700.4 662.71,-1718.17 626.58,-1726.83"/>
            <polygon fill="black" stroke="black" points="625.51,-1723.48 616.49,-1729.03 627.01,-1730.32 625.51,-1723.48"/>
            <text text-anchor="middle" x="712.97" y="-1499.3" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- unpk_5&#45;&gt;imgc_0 -->
        <g id="edge19" class="edge">
            <title>unpk_5&#45;&gt;imgc_0</title>
            <path fill="none" stroke="black" d="M482.47,-1251.8C482.47,-1240.16 482.47,-1224.55 482.47,-1211.24"/>
            <polygon fill="black" stroke="black" points="485.97,-1211.18 482.47,-1201.18 478.97,-1211.18 485.97,-1211.18"/>
            <text text-anchor="middle" x="491.47" y="-1222.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- imgc_1 -->
        <g id="node17" class="node">
            <title>imgc_1</title>
            <ellipse fill="#05a8f4" stroke="black" cx="517.47" cy="-1110" rx="99.38" ry="18"/>
            <text text-anchor="middle" x="517.47" y="-1106.3" font-family="Arial" font-size="14.00">Build a virtual machine</text>
        </g>
        <!-- imgc_0&#45;&gt;imgc_1 -->
        <g id="edge20" class="edge">
            <title>imgc_0&#45;&gt;imgc_1</title>
            <path fill="none" stroke="black" d="M490.94,-1164.81C495.02,-1156.53 500.01,-1146.41 504.55,-1137.19"/>
            <polygon fill="black" stroke="black" points="507.79,-1138.55 509.07,-1128.03 501.51,-1135.45 507.79,-1138.55"/>
        </g>
        <!-- imgc_2 -->
        <g id="node18" class="node">
            <title>imgc_2</title>
            <ellipse fill="#05a8f4" stroke="black" cx="585.47" cy="-1037" rx="76.89" ry="18"/>
            <text text-anchor="middle" x="585.47" y="-1033.3" font-family="Arial" font-size="14.00">Image animation</text>
        </g>
        <!-- imgc_1&#45;&gt;imgc_2 -->
        <g id="edge21" class="edge">
            <title>imgc_1&#45;&gt;imgc_2</title>
            <path fill="none" stroke="black" d="M533.58,-1092.17C542.22,-1083.15 553.01,-1071.89 562.51,-1061.97"/>
            <polygon fill="black" stroke="black" points="565.08,-1064.35 569.47,-1054.71 560.02,-1059.51 565.08,-1064.35"/>
        </g>
        <!-- stic_0 -->
        <g id="node19" class="node">
            <title>stic_0</title>
            <ellipse fill="#ffc009" stroke="black" cx="586.47" cy="-964" rx="88.28" ry="18"/>
            <text text-anchor="middle" x="586.47" y="-960.3" font-family="Arial" font-size="14.00">Static code analysis</text>
        </g>
        <!-- imgc_2&#45;&gt;stic_0 -->
        <g id="edge22" class="edge">
            <title>imgc_2&#45;&gt;stic_0</title>
            <path fill="none" stroke="black" d="M585.71,-1018.81C585.82,-1010.79 585.96,-1001.05 586.08,-992.07"/>
            <polygon fill="black" stroke="black" points="589.58,-992.08 586.23,-982.03 582.59,-991.98 589.58,-992.08"/>
        </g>
        <!-- stic_1 -->
        <g id="node20" class="node">
            <title>stic_1</title>
            <polygon fill="#ffc009" stroke="black" points="489.47,-909 420.59,-891 489.47,-873 558.34,-891 489.47,-909"/>
            <text text-anchor="middle" x="489.47" y="-887.3" font-family="Arial" font-size="14.00">Problem?</text>
        </g>
        <!-- stic_0&#45;&gt;stic_1 -->
        <g id="edge23" class="edge">
            <title>stic_0&#45;&gt;stic_1</title>
            <path fill="none" stroke="black" d="M563.97,-946.53C549.37,-935.85 530.31,-921.9 515.13,-910.78"/>
            <polygon fill="black" stroke="black" points="516.83,-907.69 506.7,-904.61 512.7,-913.34 516.83,-907.69"/>
        </g>
        <!-- stic_2 -->
        <g id="node21" class="node">
            <title>stic_2</title>
            <ellipse fill="#ffc009" stroke="black" cx="586.47" cy="-804" rx="66.89" ry="18"/>
            <text text-anchor="middle" x="586.47" y="-800.3" font-family="Arial" font-size="14.00">IDA Pro plugin</text>
        </g>
        <!-- stic_1&#45;&gt;stic_2 -->
        <g id="edge24" class="edge">
            <title>stic_1&#45;&gt;stic_2</title>
            <path fill="none" stroke="black" d="M504.62,-876.72C519.41,-863.76 542.21,-843.78 559.99,-828.2"/>
            <polygon fill="black" stroke="black" points="562.55,-830.61 567.76,-821.39 557.94,-825.35 562.55,-830.61"/>
            <text text-anchor="middle" x="555.97" y="-843.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- stic_3 -->
        <g id="node22" class="node">
            <title>stic_3</title>
            <polygon fill="#ffc009" stroke="black" points="350.47,-822 199.48,-804 350.47,-786 501.45,-804 350.47,-822"/>
            <text text-anchor="middle" x="350.47" y="-800.3" font-family="Arial" font-size="14.00">Need dynamic analysis?</text>
        </g>
        <!-- stic_1&#45;&gt;stic_3 -->
        <g id="edge25" class="edge">
            <title>stic_1&#45;&gt;stic_3</title>
            <path fill="none" stroke="black" d="M469.85,-878C447.25,-864.19 409.8,-841.29 382.87,-824.81"/>
            <polygon fill="black" stroke="black" points="384.53,-821.73 374.17,-819.5 380.88,-827.7 384.53,-821.73"/>
            <text text-anchor="middle" x="437.47" y="-843.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- stic_2&#45;&gt;stic_0 -->
        <g id="edge26" class="edge">
            <title>stic_2&#45;&gt;stic_0</title>
            <path fill="none" stroke="black" d="M586.47,-822.19C586.47,-849.48 586.47,-902.97 586.47,-935.59"/>
            <polygon fill="black" stroke="black" points="582.97,-935.79 586.47,-945.79 589.97,-935.79 582.97,-935.79"/>
        </g>
        <!-- dnmc_0 -->
        <g id="node23" class="node">
            <title>dnmc_0</title>
            <ellipse fill="#ff5252" stroke="black" cx="454.47" cy="-717" rx="100.98" ry="18"/>
            <text text-anchor="middle" x="454.47" y="-713.3" font-family="Arial" font-size="14.00">Dynamic code analysis</text>
        </g>
        <!-- stic_3&#45;&gt;dnmc_0 -->
        <g id="edge27" class="edge">
            <title>stic_3&#45;&gt;dnmc_0</title>
            <path fill="none" stroke="black" d="M369.06,-787.8C384.87,-774.88 407.82,-756.13 425.95,-741.31"/>
            <polygon fill="black" stroke="black" points="428.37,-743.85 433.9,-734.81 423.94,-738.43 428.37,-743.85"/>
            <text text-anchor="middle" x="420.97" y="-756.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- impt_0 -->
        <g id="node27" class="node">
            <title>impt_0</title>
            <polygon fill="#9c27b0" stroke="black" points="347.47,-488 210.56,-470 347.47,-452 484.37,-470 347.47,-488"/>
            <text text-anchor="middle" x="347.47" y="-466.3" font-family="Arial" font-size="14.00">Import table corrupted</text>
        </g>
        <!-- stic_3&#45;&gt;impt_0 -->
        <g id="edge28" class="edge">
            <title>stic_3&#45;&gt;impt_0</title>
            <path fill="none" stroke="black" d="M342.69,-786.8C335.35,-770 325.47,-742.76 325.47,-718 325.47,-718 325.47,-718 325.47,-556 325.47,-535.68 331.43,-513.47 337.15,-496.85"/>
            <polygon fill="black" stroke="black" points="340.5,-497.88 340.63,-487.29 333.92,-495.49 340.5,-497.88"/>
            <text text-anchor="middle" x="334.47" y="-640.3" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- dnmc_1 -->
        <g id="node24" class="node">
            <title>dnmc_1</title>
            <polygon fill="#ff5252" stroke="black" points="523.47,-662 454.59,-644 523.47,-626 592.34,-644 523.47,-662"/>
            <text text-anchor="middle" x="523.47" y="-640.3" font-family="Arial" font-size="14.00">Problem?</text>
        </g>
        <!-- dnmc_0&#45;&gt;dnmc_1 -->
        <g id="edge29" class="edge">
            <title>dnmc_0&#45;&gt;dnmc_1</title>
            <path fill="none" stroke="black" d="M470.82,-699.17C480.44,-689.27 492.69,-676.67 502.95,-666.11"/>
            <polygon fill="black" stroke="black" points="505.55,-668.46 510.01,-658.84 500.53,-663.58 505.55,-668.46"/>
        </g>
        <!-- dnmc_2 -->
        <g id="node25" class="node">
            <title>dnmc_2</title>
            <ellipse fill="#ff5252" stroke="black" cx="426.47" cy="-557" rx="72.59" ry="18"/>
            <text text-anchor="middle" x="426.47" y="-553.3" font-family="Arial" font-size="14.00">OllyDBG Plugin</text>
        </g>
        <!-- dnmc_1&#45;&gt;dnmc_2 -->
        <g id="edge30" class="edge">
            <title>dnmc_1&#45;&gt;dnmc_2</title>
            <path fill="none" stroke="black" d="M508.31,-629.72C493.62,-616.84 471.01,-597.03 453.27,-581.49"/>
            <polygon fill="black" stroke="black" points="455.34,-578.65 445.51,-574.69 450.73,-583.91 455.34,-578.65"/>
            <text text-anchor="middle" x="492.97" y="-596.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- dnmc_3 -->
        <g id="node26" class="node">
            <title>dnmc_3</title>
            <polygon fill="#ff5252" stroke="black" points="681.47,-575 516.91,-557 681.47,-539 846.02,-557 681.47,-575"/>
            <text text-anchor="middle" x="681.47" y="-553.3" font-family="Arial" font-size="14.00">Need more static analysis?</text>
        </g>
        <!-- dnmc_1&#45;&gt;dnmc_3 -->
        <g id="edge31" class="edge">
            <title>dnmc_1&#45;&gt;dnmc_3</title>
            <path fill="none" stroke="black" d="M544.77,-631.54C570.65,-617.61 614.69,-593.92 645.78,-577.2"/>
            <polygon fill="black" stroke="black" points="647.83,-580.07 654.97,-572.25 644.51,-573.91 647.83,-580.07"/>
            <text text-anchor="middle" x="620.47" y="-596.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- dnmc_2&#45;&gt;dnmc_0 -->
        <g id="edge32" class="edge">
            <title>dnmc_2&#45;&gt;dnmc_0</title>
            <path fill="none" stroke="black" d="M429.51,-575.19C434.35,-602.48 443.83,-655.97 449.61,-688.59"/>
            <polygon fill="black" stroke="black" points="446.22,-689.55 451.42,-698.79 453.12,-688.33 446.22,-689.55"/>
        </g>
        <!-- dnmc_3&#45;&gt;stic_0 -->
        <g id="edge33" class="edge">
            <title>dnmc_3&#45;&gt;stic_0</title>
            <path fill="none" stroke="black" d="M681.47,-575.26C681.47,-592.43 681.47,-619.54 681.47,-643 681.47,-892 681.47,-892 681.47,-892 681.47,-915.87 661.98,-932.68 640.66,-943.93"/>
            <polygon fill="black" stroke="black" points="638.92,-940.89 631.46,-948.42 641.98,-947.18 638.92,-940.89"/>
            <text text-anchor="middle" x="692.97" y="-756.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- dnmc_3&#45;&gt;impt_0 -->
        <g id="edge34" class="edge">
            <title>dnmc_3&#45;&gt;impt_0</title>
            <path fill="none" stroke="black" d="M634.67,-544.09C573.41,-528.5 466.23,-501.22 401.55,-484.76"/>
            <polygon fill="black" stroke="black" points="402.1,-481.29 391.55,-482.22 400.38,-488.08 402.1,-481.29"/>
            <text text-anchor="middle" x="543.47" y="-509.8" font-family="Arial" font-size="14.00">No</text>
        </g>
        <!-- impt_1 -->
        <g id="node28" class="node">
            <title>impt_1</title>
            <ellipse fill="#9c27b0" stroke="black" cx="171.47" cy="-383" rx="106.68" ry="18"/>
            <text text-anchor="middle" x="171.47" y="-379.3" font-family="Arial" font-size="14.00">Reconstruct import table</text>
        </g>
        <!-- impt_0&#45;&gt;impt_1 -->
        <g id="edge35" class="edge">
            <title>impt_0&#45;&gt;impt_1</title>
            <path fill="none" stroke="black" d="M319.58,-455.53C291.26,-441.85 247.03,-420.5 214.27,-404.67"/>
            <polygon fill="black" stroke="black" points="215.46,-401.36 204.93,-400.16 212.42,-407.66 215.46,-401.36"/>
            <text text-anchor="middle" x="281.97" y="-422.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- bhvr_0 -->
        <g id="node29" class="node">
            <title>bhvr_0</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-383" rx="87.18" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-379.3" font-family="Arial" font-size="14.00">Pre execution tasks</text>
        </g>
        <!-- impt_0&#45;&gt;bhvr_0 -->
        <g id="edge36" class="edge">
            <title>impt_0&#45;&gt;bhvr_0</title>
            <path fill="none" stroke="black" d="M354.41,-452.61C359.44,-440.73 366.35,-424.41 372.17,-410.67"/>
            <polygon fill="black" stroke="black" points="375.5,-411.79 376.18,-401.21 369.05,-409.06 375.5,-411.79"/>
            <text text-anchor="middle" x="379.97" y="-422.8" font-family="Arial" font-size="14.00">Yes</text>
        </g>
        <!-- impt_1&#45;&gt;unpk_1 -->
        <g id="edge37" class="edge">
            <title>impt_1&#45;&gt;unpk_1</title>
            <path fill="none" stroke="black" d="M171.47,-401.26C171.47,-418.43 171.47,-445.54 171.47,-469 171.47,-1504 171.47,-1504 171.47,-1504 171.47,-1528.64 188.69,-1550.92 204.98,-1566.48"/>
            <polygon fill="black" stroke="black" points="203.05,-1569.46 212.82,-1573.56 207.74,-1564.26 203.05,-1569.46"/>
        </g>
        <!-- bhvr_1 -->
        <g id="node30" class="node">
            <title>bhvr_1</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-310" rx="121.58" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-306.3" font-family="Arial" font-size="14.00">Run malware for 10 minutes</text>
        </g>
        <!-- bhvr_0&#45;&gt;bhvr_1 -->
        <g id="edge38" class="edge">
            <title>bhvr_0&#45;&gt;bhvr_1</title>
            <path fill="none" stroke="black" d="M383.47,-364.81C383.47,-356.79 383.47,-347.05 383.47,-338.07"/>
            <polygon fill="black" stroke="black" points="386.97,-338.03 383.47,-328.03 379.97,-338.03 386.97,-338.03"/>
        </g>
        <!-- bhvr_2 -->
        <g id="node31" class="node">
            <title>bhvr_2</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-237" rx="90.98" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-233.3" font-family="Arial" font-size="14.00">Post execution tasks</text>
        </g>
        <!-- bhvr_1&#45;&gt;bhvr_2 -->
        <g id="edge39" class="edge">
            <title>bhvr_1&#45;&gt;bhvr_2</title>
            <path fill="none" stroke="black" d="M383.47,-291.81C383.47,-283.79 383.47,-274.05 383.47,-265.07"/>
            <polygon fill="black" stroke="black" points="386.97,-265.03 383.47,-255.03 379.97,-265.03 386.97,-265.03"/>
        </g>
        <!-- bhvr_3 -->
        <g id="node32" class="node">
            <title>bhvr_3</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-164" rx="108.58" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-160.3" font-family="Arial" font-size="14.00">Dump and RAM analysis</text>
        </g>
        <!-- bhvr_2&#45;&gt;bhvr_3 -->
        <g id="edge40" class="edge">
            <title>bhvr_2&#45;&gt;bhvr_3</title>
            <path fill="none" stroke="black" d="M383.47,-218.81C383.47,-210.79 383.47,-201.05 383.47,-192.07"/>
            <polygon fill="black" stroke="black" points="386.97,-192.03 383.47,-182.03 379.97,-192.03 386.97,-192.03"/>
        </g>
        <!-- bhvr_4 -->
        <g id="node33" class="node">
            <title>bhvr_4</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-91" rx="57.69" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-87.3" font-family="Arial" font-size="14.00">HD analysis</text>
        </g>
        <!-- bhvr_3&#45;&gt;bhvr_4 -->
        <g id="edge41" class="edge">
            <title>bhvr_3&#45;&gt;bhvr_4</title>
            <path fill="none" stroke="black" d="M383.47,-145.81C383.47,-137.79 383.47,-128.05 383.47,-119.07"/>
            <polygon fill="black" stroke="black" points="386.97,-119.03 383.47,-109.03 379.97,-119.03 386.97,-119.03"/>
        </g>
        <!-- bhvr_5 -->
        <g id="node34" class="node">
            <title>bhvr_5</title>
            <ellipse fill="#00a99d" stroke="black" cx="383.47" cy="-18" rx="77.19" ry="18"/>
            <text text-anchor="middle" x="383.47" y="-14.3" font-family="Arial" font-size="14.00">Network analysis</text>
        </g>
        <!-- bhvr_4&#45;&gt;bhvr_5 -->
        <g id="edge42" class="edge">
            <title>bhvr_4&#45;&gt;bhvr_5</title>
            <path fill="none" stroke="black" d="M383.47,-72.81C383.47,-64.79 383.47,-55.05 383.47,-46.07"/>
            <polygon fill="black" stroke="black" points="386.97,-46.03 383.47,-36.03 379.97,-46.03 386.97,-46.03"/>
        </g>
    </g>
</svg>
    '''
    app = QApplication(sys.argv)
    svg_path = io.BytesIO(svg)
    viewer = ClickableSVGViewer(svg_path)
    viewer.show()
    sys.exit(app.exec_())
