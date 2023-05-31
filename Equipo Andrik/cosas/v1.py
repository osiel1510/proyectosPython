import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog, QTextEdit, QHBoxLayout, QVBoxLayout
import xml.etree.ElementTree as ET

class JffReader(QWidget):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        self.setWindowTitle('Lector de archivo Jff')

        # Botón para cargar archivo Jff
        self.btnLoad = QPushButton('Cargar archivo Jff', self)
        self.btnLoad.move(50, 50)
        self.btnLoad.clicked.connect(self.loadJff)

        # Cuadro de texto para mostrar la estructura del Jff
        self.txtJff = QTextEdit(self)
        self.txtJff.setGeometry(50, 100, 500, 200)

        # Botones para convertir y mostrar el autómata en formatos TikZ y SVG
        self.btnTikz = QPushButton('Exportar a TikZ', self)
        self.btnTikz.clicked.connect(self.exportTikz)
        self.btnSvg = QPushButton('Exportar a SVG', self)
        self.btnSvg.clicked.connect(self.exportSvg)

        # Añadir los botones de exportación a un layout horizontal
        hbox = QHBoxLayout()
        hbox.addWidget(self.btnTikz)
        hbox.addWidget(self.btnSvg)

        # Añadir el cuadro de texto y el layout horizontal a un layout vertical
        vbox = QVBoxLayout()
        vbox.addWidget(self.btnLoad)
        vbox.addWidget(self.txtJff)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.show()

    def loadJff(self):
        fname = QFileDialog.getOpenFileName(self, 'Cargar archivo Jff', '.', 'Jff files (*.jff)')[0]
        if fname:
            # Cargar el archivo Jff y mostrar su estructura en el cuadro de texto
            tree = ET.parse(fname)
            root = tree.getroot()
            self.txtJff.setText(ET.tostring(root, encoding='unicode'))

    def exportTikz(self):
        print('Exportando a TikZ...')

    def exportSvg(self):
        print('Exportando a SVG...')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = JffReader()
    sys.exit(app.exec_())
