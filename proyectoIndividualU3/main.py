from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import sys

class MainWindow(QWidget): #Clase principal
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        self.setFixedSize(1200,680)
        self.setWindowTitle("Pretty Print de Tablas Latex")
        
        #Interfaz de la aplicacion
        buttonLayout = QHBoxLayout()
        self.button = QPushButton("Transformar tabla")
        self.button.clicked.connect(self.transformarTabla)
        self.buttonImportar = QPushButton("Importar texto")
        self.buttonImportar.clicked.connect(self.importarTexto)
        self.buttonExportar = QPushButton("Exportar texto")
        self.buttonExportar.clicked.connect(self.exportarTexto)
        self.inputET = QPlainTextEdit()
        self.labelInput = QLabel("Entrada")
        self.labelOutput = QLabel("Salida")
        self.outputET = QPlainTextEdit()
        self.mainLayout = QVBoxLayout()

        buttonLayout.addWidget(self.buttonImportar)
        buttonLayout.addWidget(self.button)
        buttonLayout.addWidget(self.buttonExportar)

        self.mainLayout.addLayout(buttonLayout)
        self.mainLayout.addWidget(self.labelInput)
        self.mainLayout.addWidget(self.inputET)
        self.mainLayout.addWidget(self.labelOutput)
        self.mainLayout.addWidget(self.outputET)
        self.setLayout(self.mainLayout)

        #Colocando una fuente monoespaciada
        font = QFont("Courier New")
        self.inputET.setFont(font)
        self.outputET.setFont(font)

        #Mensaje en caso de error
        self.message_box = QMessageBox()
        self.message_box.setIcon(QMessageBox.Information)
        self.message_box.setWindowTitle("Error!")
        self.message_box.setText("Porfavor, asegúrate que la tabla tiene sus celdas bien definidas con símbolos & y que cuenta con el formato correcto")


    def exportarTexto(self): #Funcion para exportar el texto
        file_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "Archivo txt (*.txt)")

        if file_path:
            with open(file_path, 'w') as file:
                for i in self.outputET.toPlainText().strip("\n"):
                    file.write(i)

    def importarTexto(self): #Funcion para importar el texto
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivo txt (*.txt)")
        if archivo:
            with open(archivo, "r") as f:
                self.inputET.setPlainText(f.read())

    def transformarTabla(self): #Funcion principal
        try:
            self.outputET.setPlainText("")
            self.texto = self.inputET.toPlainText()
            self.texto = self.texto.split('\n') #Obtener el texto por filas
            numColumnas = self.obtenerColumnaMayor()#Obtener el numero de columnas
            
            arreglo = [] 

            for i in range(numColumnas):
                arreglo.append([])

            lineasAfectadasIndice = [] #Obtener el numero de linea que va a ser afectada

            for index,i in enumerate(self.texto): #Proceso para obtener el contenido de las celdas de la tabla
                if '&' in i:
                    palabrasObtenidas = i.split('&')
                    lineasAfectadasIndice.append(index)
                    for index,i in enumerate(arreglo):
                        i.append(palabrasObtenidas[index].replace(" ",""))

            longitudMayor = [] 
            for i in range(numColumnas): 
                longitudMayor.append(0)

            for index,i in enumerate(arreglo): #Obtener la longitud mayor de cada columna
                for j in i:
                    if len(j) > longitudMayor[index]:
                        longitudMayor[index] = len(j)

            for index,i in enumerate(arreglo): #Cambiar el ancho de las lineas en base a la longitud mayor
                for j in range(len(i)):
                    longitudFaltante = longitudMayor[index] - len(arreglo[index][j])
                    for k in range(longitudFaltante):
                        arreglo[index][j]+=" "
                    if len(arreglo)-1 != index:
                        arreglo[index][j]+=" & "

            zipp = zip(*arreglo) #Intercambiar las lineas por columnas para su impresión

            salto = True
            lineasAfectadas = []

            
            for fila in zipp: #Juntar las palabras por linea
                temp = ""
                for elemento in fila:
                    if salto == True:
                        temp+=elemento
                        salto = False
                    else:
                        temp+= " " + elemento
                salto = True
                lineasAfectadas.append(temp)

            for index,i in enumerate(lineasAfectadasIndice): #Reemplazar las lineas afectadas en el texto original
                self.texto[i] = lineasAfectadas[index]

            self.outputET.setPlainText("")
            
            for i in self.texto: #Impresión en el PlainText de salida
                self.outputET.setPlainText(self.outputET.toPlainText() + i + "\n")
        except:
            self.message_box.exec_()

    def obtenerColumnaMayor(self): #Función para obtener la columna mayor
        numColumnas = 0
        for i in self.texto:
            temp = i.count('&')
            if temp > numColumnas:
                numColumnas = temp

        return numColumnas+1

if __name__ == "__main__":  
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
