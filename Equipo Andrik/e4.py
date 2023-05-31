from PyQt5.QtWidgets import *
import re
import os
import subprocess
import xml.etree.ElementTree as ET


class PDFDialog(QDialog):
    """ Ventana de dialogo para preguntar si el usuario quiere abrir el archivo PDF generado"""

    def __init__(self):
        super().__init__()
        self.clayout = QVBoxLayout()  # La ventana de dialogo se acomoda verticalmente
        self.setWindowTitle("PDF")
        self.quest_lab = QLabel("¿Quieres abrir el pdf?")
        self.clayout.addWidget(self.quest_lab)
        self.path = ''  # Se inicializa el valor de la dirección donde se encuentra el archivo PDF
        self.pdf = ''  # Nombre del archivo PDF generado

        QBtn = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        # Se agregan los botones de aceptar y rechazar
        self.buttonBox = QDialogButtonBox(QBtn)

        # Se conectan los valores con las funciones respectivas de cada boton
        self.buttonBox.accepted.connect(self.BotonAcepto)
        self.buttonBox.rejected.connect(self.BotonNoAcpeto)

        self.clayout.addWidget(self.buttonBox)
        self.setLayout(self.clayout)

    # Setters de las variables globales pdf y path
    def set_pdfName(self, name):
        self.pdf = name

    def set_path(self, path):
        self.path = path

    def BotonAcepto(self):
        """ Método conectado con los botones de dialogo en caso de que el usuario acepte ver el pdf """
        self.accept()
        # Se lanza mediante evince el pdf
        open_file = subprocess.Popen(["evince", self.pdf], cwd=self.path)

    def BotonNoAcpeto(self):
        """ Método conectado con los botones de dialogo en caso de que el usuario rechace ver el pdf"""
        self.reject()


class JFFtoTikZ(QWidget):
    def __init__(self):
        super().__init__()
        # Instancia de la clase PDFDialog que muestra una ventana de dialogo para mostrar el pdf
        self.result = PDFDialog()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 1280, 720)
        self.setWindowTitle('JFF to TikZ or SVG Converter')

        self.textEdit = QTextEdit(self)
        self.textEdit.setGeometry(10, 10, 1260, 600)
        # self.textEdit.setDisabled(True)

        self.openButton = QPushButton('Open JFF', self)
        self.openButton.setGeometry(10, 620, 100, 30)
        self.openButton.clicked.connect(self.openJFF)

        self.convertButton = QPushButton('Convert to TikZ', self)
        self.convertButton.setGeometry(120, 620, 110, 30)
        self.convertButton.clicked.connect(self.convertJFF)
        self.convertButton.setDisabled(False)

        self.saveButton = QPushButton('Save as .tex', self)
        self.saveButton.setGeometry(240, 620, 100, 30)
        self.saveButton.clicked.connect(self.saveTex)
        self.saveButton.setDisabled(True)

        self.clearButton = QPushButton('Clear', self)
        self.clearButton.setGeometry(350, 620, 100, 30)
        self.clearButton.clicked.connect(self.clearAll)
        self.clearButton.setDisabled(True)

        self.exitButton = QPushButton('Exit', self)
        self.exitButton.setGeometry(460, 620, 100, 30)
        self.exitButton.clicked.connect(self.exitApp)

        self.convertSVGButton = QPushButton('Convert to SVG', self)
        self.convertSVGButton.setGeometry(10, 660, 110, 30)
        # self.convertSVGButton.clicked.connect(self.convertJFFtoSVG)
        self.convertSVGButton.setDisabled(True)
        self.show()

    def openJFF(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        jffFile, _ = QFileDialog.getOpenFileName(
            self, "Open JFF File", "", "JFLAP files (*.jff);;All Files (*)", options=options)
        if jffFile:
            with open(jffFile, 'r') as f:
                self.textEdit.setText(f.read())
                self.convertButton.setDisabled(False)
                self.clearButton.setDisabled(False)
                self.convertSVGButton.setDisabled(False)

    def convertJFF(self):
        jff = self.textEdit.toPlainText()
        root = ET.fromstring(jff)
        tikz = r"\documentclass{standalone}"
        tikz += r"\usepackage{tikz}"
        tikz += r"\usetikzlibrary{automata, positioning, arrows, shapes, fit, arrows.meta}"
        tikz += r"\begin{document}"
        tikz += r"\begin{tikzpicture}"
        tikz += r"\tikzset{->,>=stealth',node distance=6cm,every state/.style={thick, fill=gray!10}, initial state/.style={thick, fill=gray!10, fill=yellow}initial text=$ $, }"

        for state in root.iter('state'):
            state_id = state.get('id')
            state_name = state.get('name')
            x = float(state.find('x').text)
            y = float(state.find('y').text)
            if state.find('initial') is not None:
                tikz += f"\n\t\\node[state,initial] ({state_id}) at ({x*0.01},{y*0.01}) {{{state_name}}};"
            elif state.find('final') is not None:
                tikz += f"\n\t\\node[state,accepting] ({state_id}) at ({x*0.01},{y*0.01}) {{{state_name}}};"
            else:
                tikz += f"\n\t\\node[state] ({state_id}) at ({x*0.01},{y*0.01}) {{{state_name}}};"
        for transition in root.iter('transition'):
            source = transition.find('from').text
            target = transition.find('to').text
            label = transition.find('read')
            if label is not None:
                if source == target:
                    tikz += f"\n\t\\path ({source}) edge[loop above] node {{{label.text}}} ({target});"
                else:
                    # Check if there is an edge from target to source
                    reverse_edge = False
                    for t in root.iter('transition'):
                        if t.find('from').text == target and t.find('to').text == source:
                            reverse_edge = True
                            break
                    # Add the bend option based on the reverse_edge flag
                    bend_option = "bend left" if reverse_edge else "bend right"
                    tikz += f"\n\t\\path ({source}) edge[{bend_option}] node {{{label.text}}} ({target});"

        tikz += r"\end{tikzpicture}"
        tikz += r"\end{document}"
        self.saveButton.setDisabled(False)
        self.textEdit.setPlainText(tikz)

    def saveTex(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        texFile, _ = QFileDialog.getSaveFileName(
            self, "Save as .tex File", "", "TeX files (*.tex);;All Files (*)", options=options)
        if texFile:
            if not texFile.endswith('.tex'):
                texFile += '.tex'
            with open(texFile, 'w') as f:
                f.write(self.textEdit.toPlainText())
            # path = os.path.dirname(os.path.abspath(__file__))
            l = texFile.split('/')
            name = l[-1][:-4]
            path = '/'.join(l[:-1])
            print(path)
            list_files = subprocess.run(["pdflatex", texFile], cwd=path)
            list_files = subprocess.run(["pdflatex", texFile], cwd=path)
            print("The exit code was: %d" % list_files.returncode)
            QMessageBox.information(
                self, "Alerta", "Se ha guardado con éxito.")
            self.result.set_pdfName(name+'.pdf')
            self.result.set_path(path)
            # Se muestra una ventana para preguntar si se quiere abrir el archivos PDF o no
            self.result.show()
            # self.result.show() # Se muestra una ventana para preguntar si se quiere abrir el archivos PDF o no

    def clearAll(self):
        self.textEdit.clear()
        self.convertButton.setDisabled(True)
        self.saveButton.setDisabled(True)

    def exitApp(self):
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication([])
    ex = JFFtoTikZ()
    app.exec_()
