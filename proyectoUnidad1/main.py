from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import json
import math

class DrawWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1300, 600)
        self.data = None

    def getData(self,jsonInput):
        self.data = json.loads(jsonInput) 
        self.update()

    def paintEvent(self, event):
        if self.data != None:
            qp = QPainter()
            qp.begin(self)
            pen = QPen()
            pen.setWidth(2)
            qp.setPen(pen)

            # draw edges
            for edge in self.data['el'].values():
                u = self.data['vl'][str(edge['u'])]
                v = self.data['vl'][str(edge['v'])]

                # create a line object
                line = QLineF(u['x'], u['y'], v['x'], v['y'])

                # shorten the line to stop at the vertex
                line.setLength(line.length() - 28)

                # draw the shortened line
                qp.drawLine(line)

                # draw the arrowhead on the shortened line
                arrowhead_size = 10
                angle = math.atan2(v['y'] - u['y'], v['x'] - u['x'])
                p1 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle - math.pi / 6)),
                            int(line.y2() - arrowhead_size * math.sin(angle - math.pi / 6)))
                p2 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle + math.pi / 6)),
                            int(line.y2() - arrowhead_size * math.sin(angle + math.pi / 6)))
                qp.drawLine(QLineF(line.x2(), line.y2(), p1.x(), p1.y()))
                qp.drawLine(QLineF(line.x2(), line.y2(), p2.x(), p2.y()))

            # draw vertices
            brush = QColor(200, 200, 200)
            qp.setBrush(brush)
            font = QFont()
            font.setPointSize(16)
            qp.setFont(font)
            cont = 0
            for vertex in self.data['vl'].values():
                qp.drawEllipse(vertex['x'] - 25, vertex['y'] - 25, 50, 50)
                qp.drawText(vertex['x'] - 6, vertex['y'] + 8, str(cont))
                cont+=1
            cont = 0

            qp.end()

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        self.width = 800
        self.height = 400
        self.setFixedSize(1300,600)

        self.mainLayout = QVBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.drawWidget = DrawWidget()

        self.inputLineEdit = QLineEdit()
        self.inputLabel = QLabel("Estructura de grafo en formato JSON: ")
        self.inputButton = QPushButton("Visualizar")
        self.inputButton.released.connect(self.enterJsonText)
        
        self.inputLayout.addWidget(self.inputLabel)
        self.inputLayout.addWidget(self.inputLineEdit)
        self.inputLayout.addWidget(self.inputButton)
        
        self.mainLayout.addLayout(self.inputLayout)
        self.mainLayout.addWidget(self.drawWidget)
        
        self.setLayout(self.mainLayout)

    def enterJsonText(self):
        self.drawWidget.getData(self.inputLineEdit.text())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
