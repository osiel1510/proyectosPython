from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5 import QtGui
import re
import sys

class DrawWidget(QWidget):
    #Clase de dibujo principal
    def __init__(self, parent=None):
        super().__init__(parent)
        self.arreglo = [] #Arreglo de todas las posiciones a dibujar
        self.posicionArreglo = 0 #Posicion de la cabeza de la banda en el arreglo
        
    def paintEvent(self, event):
        qp = QPainter() 
        qp.begin(self)
        qp.setFont(QFont('Arial', 20))
        qp.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        
        x = 10 #Posicion de la primer caja
        for i in self.arreglo: #Dibujamos las cajas en base al ancho de cada caja y el numero de caja
            qp.drawRect(x,320, 79, 80) #Dibujamos la caja
            if i != " ":
                qp.drawText(x+34, 370, i) #Dibujamos el contenido
            x+=79 #Incremenamos el ancho de la caja

        posicionArregloWidth = 10+(self.posicionArreglo*79) #Calculamos la posicion de la cabeza de la banda

        path = QPainterPath() #Dibujamos la flecha con paths 
        path.moveTo(posicionArregloWidth+40, 200)
        path.lineTo(posicionArregloWidth+40, 300)
        path.lineTo(posicionArregloWidth+20, 280)
        path.moveTo(posicionArregloWidth+40, 300)
        path.lineTo(posicionArregloWidth+60, 280)
        qp.setPen(QPen(Qt.black, 5, Qt.SolidLine))
        qp.drawPath(path)

        qp.end()

class SyntaxHighlighter(QSyntaxHighlighter): #Codigo para resaltar de un color una linea de un PlainTextEdit
    def __init__(self, parent):
        super(SyntaxHighlighter, self).__init__(parent)
        self._highlight_lines = dict()

    def highlight_line(self, line, fmt):
        if isinstance(line, int) and line >= 0 and isinstance(fmt, QTextCharFormat):
            self._highlight_lines[line] = fmt
            tb = self.document().findBlockByLineNumber(line)
            self.rehighlightBlock(tb)

    def clear_highlight(self):
        self._highlight_lines = dict()
        self.rehighlight()
        self.highlighted = False

    def highlightBlock(self, text):
        line = self.currentBlock().blockNumber()
        fmt = self._highlight_lines.get(line)
        if fmt is not None:
            self.setFormat(0, len(text), fmt)

class MainWindow(QWidget): #Clase principal
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        self.setFixedSize(1200,680)
        self.contadorShot = 0

        self.setStyleSheet("background-color: #d3d3d3;")
        mainLayout = QHBoxLayout()
        leftLayout = QVBoxLayout() #Layout izquierda
        self.line_numbers = QPlainTextEdit() #Indicador de numero de lineas
        self.line_numbers.setMaximumWidth(50)
        self.line_numbers.setMinimumWidth(50)
        self.input = QPlainTextEdit() #QPlainTextEdit para ingresar las instrucciones del programa
        self.input.setMinimumWidth(200)
        self.input.setMaximumWidth(240)
        self.labelErrores = QLabel("") #Label para mostrar errores de sintaxis
        self.labelErrores.setMinimumWidth(200)
        self.labelErrores.setMaximumWidth(300)
        self.labelErrores.setWordWrap(True)
        buttonStart = QPushButton("Empezar")
        buttonStart.setMaximumWidth(150)
        buttonNext = QPushButton("Siguiente")
        buttonNext.setMaximumWidth(150)
        buttonNext.clicked.connect(self.animarPrograma)
        firstButtonLayout = QHBoxLayout()
        buttonStart.clicked.connect(self.cargarPrograma)
        self.buttonContinue = QPushButton("Continuar")
        self.buttonContinue.setMaximumWidth(150)
        self.buttonContinue.clicked.connect(self.continuarPrograma)
        buttonStop = QPushButton("Pausar")
        buttonStop.setMaximumWidth(150)
        buttonStop.clicked.connect(self.pausarPrograma)
        programaLayout = QHBoxLayout() #Layout que contiene las lineas y la entrada del programa
        programaLayout.addWidget(self.line_numbers)
        programaLayout.addWidget(self.input)
        leftLayout.addLayout(programaLayout)
        leftLayout.addLayout(firstButtonLayout)
        firstButtonLayout.addWidget(buttonStart)
        firstButtonLayout.addWidget(buttonNext)
        layoutBotonesControladores = QHBoxLayout() #Layout de los botones que controlan el flujo
        leftLayout.addLayout(layoutBotonesControladores)
        layoutBotonesControladores.addWidget(self.buttonContinue)
        layoutBotonesControladores.addWidget(buttonStop)
        layoutBotonesArchivo = QHBoxLayout() #Layout de los botones de importar exportar
        buttonExportar = QPushButton("Exportar")
        buttonImportar = QPushButton("Importar")
        layoutBotonesArchivo.addWidget(buttonImportar)
        layoutBotonesArchivo.addWidget(buttonExportar )
        leftLayout.addLayout(layoutBotonesArchivo)

        self.botonScreenshots = QPushButton("Habilitar Screenshots")
        self.botonScreenshots.setCheckable(True)
        leftLayout.addWidget(self.botonScreenshots)

        leftLayout.addWidget(self.labelErrores)
        buttonImportar.clicked.connect(self.importarCodigo)
        buttonExportar .clicked.connect(self.exportarCodigo)
        self.labelErrores.setStyleSheet("color:red;")
        timerCursor = QTimer(self) #Timer que comprueba que el cursor esté en la misma linea en los dos PlainTextEdit
        timerCursor.timeout.connect(self.copyCursorPosition) 
        timerCursor.start(1)
        self.line_numbers.setReadOnly(True) #Para que no pueda ser modificada
        self.input.verticalScrollBar().valueChanged.connect(self.scrollEditText) #Para que el scroll sea el mismo en ambos PlainTextEdit
        self.line_numbers.setStyleSheet("background-color: #d3d3d3;") 
        self.input.setStyleSheet("background-color: #ffffff")
        self.input.setWordWrapMode(QTextOption.NoWrap)  
        self.rightLayout = QVBoxLayout()
        self.inputEntrada = QLineEdit()
        self.inputEntrada.setStyleSheet("background-color: #ffffff")
        label = QLabel("Entrada:")
        self.inputLayout = QHBoxLayout()
        self.inputLayout.addWidget(label)
        self.inputLayout.addWidget(self.inputEntrada)
        self.rightLayout.addLayout(self.inputLayout)
        self.drawWidget = DrawWidget()
        self.inputAnterior = "" #Input que ayuda a saber si se alteró el programa 


        self.highlighter = SyntaxHighlighter(self.input.document()) #Clase para resaltar las lineas

        #Variables iniciales
        self.returnProgama = None 
        self.arregloPrincipal = [''] #Arreglo de todas las letras
        self.palabraActual = 0 #Palabra que en la que va el código
        self.posicionArregloActual = 0 #Posicion en la que va el código
        self.ultimoElemento = 0 

        self.update_line_numbers()

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(self.rightLayout)

        self.setLayout(mainLayout)
        self.setWindowTitle("Turing Machine")

        self.actions = ['Return','Write','Move','Goto'] #Estas son las palabras clave de acciones

        #Estas son las palabras reservadas
        self.reservedWords = ["If","Blank","Return","False","True","Write","Not","Move","Right","Move","Left","Goto"]

        #Scroll que ayuda a que la banda pueda ser visualizada de manera adecuada
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.drawWidget)
        self.scroll_area.show()

        #self.scroll_area.horizontalScrollBar().valueChanged.connect(self.imprimirValorScroll)

        self.rightLayout.addWidget(self.scroll_area)

        self.actualizarArregloWidget()

        self.buttonContinue.setEnabled(False)

    def limpiarInput(self): #Metodo que ayuda a limpiar el resaltado cuand se está editando el código.
        self.update_line_numbers()
        try:
            if self.inputAnterior != self.input.toPlainText():
                self.highlighter.clear_highlight()
                self.inputAnterior = self.input.toPlainText()
                self.buttonContinue.setEnabled(False)
        except:
            pass
    
    def continuarPrograma(self):#Continuar con la ejecucion del programa
        self.timer.start(600)
        self.buttonContinue.setEnabled(False)

    def scrollEditText(self,value): #Asignar el valor del scroll al otro scroll
        self.line_numbers.verticalScrollBar().setValue(value)
        
    def copyCursorPosition(self):
        self.limpiarInput()
        #Codigo para hacer que el cursor de un input sea igual en ambos inputs
        cursor = self.input.textCursor()
        line_number = cursor.blockNumber()
        cursor2 = self.line_numbers.textCursor()
        cursor2.setPosition(self.line_numbers.document().findBlockByLineNumber(line_number).position())
        self.line_numbers.setTextCursor(cursor2)

    def guardarImagen(self):
        screen = QApplication.primaryScreen()
        screenshot = screen.grabWindow( form.winId() )
        screenshot.save('./shots/shot' + str(self.contadorShot) + '.jpg', 'jpg')
    
    def update_line_numbers(self): #Actualizar el numero de lineas que hay en el codigo
        line_count = self.input.blockCount()

        numbers = ''
        for i in range(0, line_count):
            numbers += str(i) + '\n'

        self.line_numbers.setPlainText(numbers)

    def cargarPrograma(self): #funcion para inicializar los valores del programa
        self.contadorShot = 0
        self.buttonContinue.setEnabled(False)
        self.returnProgama = None
        self.arregloPrincipal = ['']
        self.palabraActual = 0
        self.posicionArregloActual = 0
        self.ultimoElemento = 0

        #Eliminar las lineas vacías
        texto = self.input.toPlainText()
        texto = re.sub(r'\n\s*\n','\n',texto)
        self.input.setPlainText(texto)
        
        #Eliminar espacios en blanco
        texto = self.input.toPlainText().lstrip()
        self.input.setPlainText(texto)
        if texto.replace(" ","") == "":
            return None

        #Obtener cada linea en un arreglo
        lines = texto.split('\n')

        #Obtener cada arreglo de linea en arrego de palabras
        self.programa = [line.split() for line in lines]
        self.programaI = []

        #Obtener todas las palabras en un arreglo, su linea y su número de palabra.
        contador = 0
        for indexLine, line in enumerate(self.programa):
            for word in line:
                self.programaI.append([word,indexLine,contador])
                contador+=1

        #Obtener la ultima linea y el ulimo elemento
        ultimaLinea = self.programaI[len(self.programaI)-1][1]
        ultimoElemento = len(self.programaI)

        #Añadir 10 posiciones más para evitar errores
        for i in range(ultimoElemento,ultimoElemento+10):
            self.programaI.append(['        ',ultimaLinea,i])

        valor = self.verifyLanguage() #Verificar que el codigo no contenga palabras extrañas o no reconocidas

        if self.programaI[len(self.programaI)-12][0] == 'Goto' or self.programaI[len(self.programaI)-12][0] == 'Return':
            pass #Verificar que el programa finalice en una sentencia goto o return
        else:
            valor = ['Error en la última linea: El programa debe terminar con una instruccion Return o Goto',ultimaLinea]
        
        if valor == None:
            valor = self.verifySintaxis() #Veriicar que el prorama esté bien escrito para ser ejecutado
            if valor == None:
                self.correrPrograma() #Correr el programa
            else:
                self.colorearLinea(valor[1],"red") #Marcar que linea tiene el error
                self.colocarCursor(valor[1])
                self.labelErrores.setText(valor[0])
        else:
            self.colorearLinea(valor[1],"red") #Marcar que linea tiene el error
            self.colocarCursor(valor[1])
            self.labelErrores.setText(valor[0])

    def exportarCodigo(self): #Funcion para exportar el codigo
        file_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "Archivo txt (*.txt)")

        if file_path:
            with open(file_path, 'w') as file:
                for i in self.input.toPlainText().strip("\n"):
                    file.write(i)

    def importarCodigo(self): #Funcion para importar el codigo
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivo txt (*.txt)")
        if archivo:
            with open(archivo, "r") as f:
                self.input.setPlainText(f.read())

    def actualizarArregloWidget(self): #Funcion para actualizar las posiciones del widget de dibujo
        self.drawWidget.arreglo = self.arregloPrincipal
        self.drawWidget.posicionArreglo = self.posicionArregloActual
        self.drawWidget.setMinimumWidth(10+(len(self.arregloPrincipal)*79)) #Actualizar el tamaño del widget
        self.scroll_area.horizontalScrollBar().setValue(10+(self.posicionArregloActual*79)) #Actualizar la posicion del scroll para que siga a la cabeza de la banda
        self.update() #Actualizar la visualizacion

    def pausarPrograma(self): #Pausar el programa
        try:
            self.timer.stop()
            self.buttonContinue.setEnabled(True) #Poder continuar el programa
        except:
            return None

    def correrPrograma(self): #Funcion para correr el prorama
        self.arregloPrincipal = list(self.inputEntrada.text()) #Obtener la entrada en un arreglo
        if len(self.arregloPrincipal) == 0:
            self.labelErrores.setText("¡Ingresa al menos un valor en la entrada!") #Verificacion de que ingresen al menos uno
            return None

        #Inicializacion de las variables
        self.labelErrores.setText("")
        self.palabraActual = self.programaI[0]
        self.posicionArregloActual = 0
        self.returnPrograma = None
        self.actualizarArregloWidget()
        self.ultimoElemento = len(self.programaI) - 9
        self.timer = QTimer(self)
        self.inputAnterior = self.input.toPlainText()
        #Asignacion del timer al metodo de animacion
        self.timer.timeout.connect(self.animarPrograma) 
        self.timer.start(600)

    def ejecutarAction(self,words=None): #Metodo para ejecutar una accion dependiendo de la palabra
        if words[0][0] == 'Goto': #Actualizacion de la palabra actual para hacer match con la etiqueta
            palabra = words[1][0] + ':'
            for i in self.programaI:
                if i[0] == palabra:
                    self.palabraActual = i
        elif words[0][0] == 'Write': #Cambiar el valor de la cabeza
            if words[1][0] == 'Blank':
                palabra = ' '
            else:
                palabra = words[1][0][1]
            self.arregloPrincipal[self.posicionArregloActual] = palabra

        elif words[0][0] == 'Return': #Finalizar el programa con un return
            self.returnPrograma = words[1][0]
            self.timer.stop() #Parar la animacion
            self.buttonContinue.setEnabled(False) 
            if words[1][0] == "True": #Dependiendo del true or false, pintar la linea de cierto color
                self.colorearLinea(self.palabraActual[1],qRgb(0,230,0))
                self.colocarCursor(self.palabraActual[1])
            else:
                self.colorearLinea(self.palabraActual[1],"red")
                self.colocarCursor(self.palabraActual[1])

        elif words[0][0] == 'Move': #Mover la cabeza
            if words[1][0] == 'Right':
                if self.posicionArregloActual == len(self.arregloPrincipal)-1: #Hacer el arreglo más grande en caso de llegar al limite
                    self.arregloPrincipal.append(" ")
                self.posicionArregloActual+=1
            else:
                if self.posicionArregloActual == 0: 
                    self.arregloPrincipal.insert(0," ") #Hacer el arreglo más grande en caso de llegar al limite
                else:
                    self.posicionArregloActual-=1

    def ejecutarIf(self,words): #Sentencia IF, dependiendo de las palabras realiza una acción
        if words[0][0] == 'If':
            if words[1][0] == 'Not':
                if words[2][0] == 'Blank':
                    if self.arregloPrincipal[self.posicionArregloActual] != ' ':
                        self.ejecutarAction(words[3:5])
                else:
                    if self.arregloPrincipal[self.posicionArregloActual] != words[2][0][1]:
                        self.ejecutarAction(words[3:5])
            else:
                if words[1][0] == 'Blank':
                    if self.arregloPrincipal[self.posicionArregloActual] == ' ':
                        self.ejecutarAction(words[2:5])
                else:
                    if self.arregloPrincipal[self.posicionArregloActual] == words[1][0][1]:
                        self.ejecutarAction(words[2:5])

    def animarPrograma(self): #Animacion del programa
        if self.palabraActual[2] > self.ultimoElemento:
            self.timer.stop() 
            #En caso de que se llegue al final del programa

        self.colorearLinea(self.palabraActual[1],"yellow") #Marcar la linea en la que va
        self.colocarCursor(self.palabraActual[1]) #Mover el cursor a la linea

        indice = self.palabraActual[2] #Obtener el indice de la palabra
        indiceInicial = self.palabraActual[2] #Respaldar el indice
        word = self.palabraActual #Actualizar la variable word
        
        if word[0] == 'If': #En caso de ser sentencia if
            if self.programaI[indice+1][0] == 'Not':
                self.ejecutarIf(self.programaI[indice:indice+5])
                indice+=4 #Actualizar indcie para saltar las palabras ya utilizadas
            else:
                self.ejecutarIf(self.programaI[indice:indice+4])
                indice+=3#Actualizar indcie para saltar las palabras ya utilizadas

        elif word[0] in self.actions: #En caso de que sea una acción
            self.ejecutarAction(self.programaI[indice:indice+2])
            indice+=1#Actualizar indcie para saltar las palabras ya utilizadas
        
        indice += 1 #Mover al siguiente indice
        if indiceInicial == self.palabraActual[2]: #Actualizar la palabra actual
            self.palabraActual = self.programaI[indice]

        self.contadorShot+=1
        if self.botonScreenshots.isChecked():
            self.guardarImagen()
        self.actualizarArregloWidget()

    def colocarCursor(self,paso): #Colocar cursor en cierta posicion
        cursor = self.input.textCursor()
        cursor.movePosition(QTextCursor.StartOfLine, QTextCursor.MoveAnchor)
        for i in range(paso):
            cursor.movePosition(QTextCursor.Down)
        self.input.setTextCursor(cursor)

    def colorearLinea(self,line,color): #Colorear una linea en base al numero de linea y el color.
        fmt = QTextCharFormat()
        fmt.setBackground(QColor(color))
        self.highlighter.clear_highlight()
        self.highlighter.highlight_line(line, fmt)

    def isCallFunction(self,word): #Verificar si es el llamado de un tag o es la declaracion del tag
        if list(word)[len(list(word))-1] != ':':
            return True
        else:
            return False

    def isFunction(self,word): #Verificar si es un tag
        if list(word)[0].isupper():
            return True
        else:
            return False

    def isCharacter(self,word): #Verificar si es un caracter
        if list(word)[0] == "'" and list(word)[len(list(word))-1] == "'" and len(list(word)) == 3:
            return True
        else:
            return False
        
    def verifyWrite(self,words): #Verificar si un write esta bien escrito
        if words[1][0] == 'Blank' or self.isCharacter(words[1][0]):
            return [True,None]
        else:
            return [False,'Error, instruccion erronea ' + words[1][0] + ' en la linea: ' + str(words[1][1]),words[1][1]]
    
    def verifyReturn(self,words):#Verificar si un return esta bien escrito
        if words[1][0] == 'True' or words[1][0] == 'False':
            return [True,None]
        else:
            return [False,'Error, instruccion erronea ' + words[1][0] + ' en la linea: ' + str(words[1][1]),words[1][1]]
    
    def verifyGoto(self,words):#Verificar si un goto esta bien escrito
        if words[1][0] not in self.reservedWords:
            return [True,None]
        else:
            return [False,'Error, instruccion erronea ' + words[1][0] + ' en la linea: ' + str(words[1][1]),words[1][1]]

    def verifyAction(self,words): #Verificar que las acciones estén bien escritas
        if words[0][0] == 'Goto':
            return self.verifyGoto(words)
        elif words[0][0] == 'Write':
            return self.verifyWrite(words)
        elif words[0][0] == 'Return':
            return self.verifyReturn(words)
        elif words[0][0] == 'Move':
            if words[1][0] == 'Right' or words[1][0] == 'Left':
                return [True,None]
            else:
                return [False,'Error, instruccion erronea ' + words[1][0] + ' en la linea: ' + str(words[1][1]),words[1][1]]
        else:
            return [False,'Error, instruccion erronea ' + words[0][0] + ' en la linea: ' + str(words[0][1]),words[0][1]]

    def verifyIf(self,words): #Verificar que las sentencias if estén bien escritas
        if words[0][0] == 'If':
            if words[1][0] == 'Not':
                if words[2][0] == 'Blank' or self.isCharacter(words[2][0]):
                    return self.verifyAction(words[3:5])
                else:
                    return [False,'Error, instruccion erronea ' + words[2][0] + ' en la linea: ' + str(words[2][1]),words[2][1]]
            else:
                if words[1][0] == 'Blank' or self.isCharacter(words[1][0]):
                    return self.verifyAction(words[2:5])
                else:
                    return [False,'Error, instruccion erronea ' + words[1][0] + ' en la linea: ' + str(words[1][1]),words[1][1]]
    
    def verifySintaxis(self): #Verificar la sintaxis dle programa
        indice = 0
        while indice < len(self.programaI): 
            word = self.programaI[indice]
            if word[0] == 'If': #Verificar sentencia if
                if self.programaI[indice+1][0] == 'Not':
                    if self.verifyIf(self.programaI[indice:indice+5])[0] == False:
                        return self.verifyIf(self.programaI[indice:indice+5])[1]
                    else:
                        indice+=4
                else:
                    if self.verifyIf(self.programaI[indice:indice+4])[0] == False:
                        return self.verifyIf(self.programaI[indice:indice+4])[1]
                    else:
                        indice+=3

            elif word[0] in self.actions: #Verificar acciones
                if self.verifyAction(self.programaI[indice:indice+2])[0] == False:
                    return ['Error, instrucción incompleta en la linea: ' + str(word[1]) +', ' + word[0],word[1]]
                else:
                    indice+=1

            elif self.isCharacter(word[0]) or word[0] == 'Blank': #Verificar caracter
                return ['Error, caracter "' + word[0] + '" en posición incorrecta, linea: ' + str(word[1]),word[1]]
                
            elif self.isFunction(word[0]) and self.isCallFunction(word[0]): #Verificar si es un tag
                return ['Error, etiqueta "' + word[0] + '" en posición incorrecta, linea: ' + str(word[1]),word[1]]

            if self.isFunction(word[0]) and self.isFunction(self.programaI[indice+1][0]):
                if self.isCallFunction(word[0]) == False and self.isCallFunction(self.programaI[indice+1][0]) == False:
                    return ['Error, etiqueta vacía "' + word[0] + '" en la línea: ' + str(word[1]),word[1]]
            
            indice += 1

    def verifyLanguage(self): #Funcion para verificar que no existan palabras extrañas en el codigo
        funciones = []
        if self.programa[0][0]!= 'Start:':
            return ['Error en la linea 0: El programa debe iniciar con la etiqueta Start',0]
        for indexLine, line in enumerate(self.programa):
            for word in line:
                if word in self.reservedWords:
                    pass
                else:
                    if self.isCharacter(word):
                        pass
                    else:
                        if self.isFunction(word) == False:
                            return ['Error en la linea ' + str(indexLine) + ': Palabra desconocida, ' + word,indexLine]
                        else:
                            if word[:-1] in self.reservedWords:
                                return ['Error en la linea ' + str(indexLine) + ': Las etiquetas no se pueden llamar como alguna palabra reservada, ' + word ,indexLine]
                            else:
                                if self.isCallFunction(word):
                                    valor = False
                                    for line2 in self.programa:
                                        for word2 in line2:
                                            if word + ':' == word2:
                                                valor = True
                                    if valor == False:
                                        return ['Error en la linea ' + str(indexLine) + ': Etiqueta llamada sin declarar, ' + word ,indexLine]
                                    
                if self.isFunction(word): #Verificar si la declaracion de una etiqueta se repite
                    if self.isCallFunction(word) == False:
                        funciones.append(word)
                        if funciones.count(word) > 1:
                            return ['Error, etiqueta repetida: ' + word,indexLine]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())