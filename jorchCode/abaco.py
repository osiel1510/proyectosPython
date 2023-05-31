import time
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import math
import copy
import random

class Bola: #Clase bola 
    def __init__(self, n = None,x = None, y = None):
        self.valor = n #Valor de la bola entorno al abaco
        self.x = x #Posiciones
        self.y = y
        self.estado = 1 #El estado indica si está activa o no la bola

class Abaco: #Clase del abaco regular
    def __init__(self,columnas = [], filaSuperior = []):
        self.columnas = columnas #Almacena todas las bolas de cada columna
        self.filaSuperior = filaSuperior #Almacena las bolas superiores

    def obtenerBolasColumna(self): #Metodo para obtener todas las bolas inferiores
        bolas = []
        for i in self.columnas:
            for j in i:
                bolas.append(j)
        return bolas
    
    def obtenerBolas(self): #Obtener todas las bolas, tanto de superiores como inferiores
        bolas = []
        
        for i in self.columnas:
            for j in i:
                bolas.append(j)
        
        for i in self.filaSuperior:
            bolas.append(i)

        return bolas

    def obtenerIndice(self,bola): #Obtener la columna y el indice de una bola específica
        for i in range(len(self.columnas)):
            for j in range(len(self.columnas[i])):
                if self.columnas[i][j] == bola:
                    return [i,j]
                    
    def inicializarAbaco(self): #Metodo para inicializar el abaco 
        self.columnas = []
        self.filaSuperior = []
        #Posiciones de las bolas
        x = 120
        y = 300
        valorAbaco = 1000000000 #Valores que tendrán las bolas del abaco
        for i in range(10):
            self.columnas.append([])
            for j in range(4):
                self.columnas[len(self.columnas)-1].append(Bola(valorAbaco,x,y))
                y+=65
            valorAbaco = valorAbaco/10
            x+=80 #Posiciones de las bolas
            y = 300

        y = 100
        x = 120

        #Valores y posiciones para las bolas superiores
        valorAbaco = 5000000000
        for i in range(10):
            self.filaSuperior.append(Bola(valorAbaco,x,y))
            x+=80
            valorAbaco=valorAbaco/10

    def obtenerSumaSuperior(self): #Obtener valor total de las bolas superiores
        suma = 0
        for i in self.obtenerBolasColumna():
            if i.estado == 2:
                suma+=i.valor
        return suma
    
    def obtenerSumaInferior(self): #Obtener valor total de las bolas inferiores
        suma = 0
        for i in self.filaSuperior:
            if i.estado == 2:
                suma+=i.valor
        return suma

    def obtenerSumaTotal(self): #Obtener suma total de todos los valores de las bolas
        return (self.obtenerSumaSuperior() + self.obtenerSumaInferior())

class AbacoAzteca: #Claso del abaco azteca
    def __init__(self,columnas = [], filaSuperior = []):
        self.columnas = columnas
        self.columnasSuperiores = filaSuperior

    def obtenerBolasInferiores(self): #Obtener un arreglo de las bolas inferiores
        bolas = []
        for i in self.columnas:
            for j in i:
                bolas.append(j)
        return bolas
    
    def obtenerBolasSuperiores(self): #Obtener un arreglo de las bolas superiores
        bolas = []
        for i in self.columnasSuperiores:
            for j in i:
                bolas.append(j)
        return bolas
    
    def obtenerBolas(self): #Obtener todas las bolas del abaco
        bolas = []
        for i in self.obtenerBolasSuperiores():
            bolas.append(i)

        for i in self.obtenerBolasInferiores():
            bolas.append(i)

        return bolas

    def obtenerIndice(self,bola,columna): #Obtener la columnda y el indice de una bola especifica
        if columna == 0:
            columna = self.columnas
        else:
            columna = self.columnasSuperiores

        for i in range(len(columna)):
            for j in range(len(columna[i])):
                if columna[i][j] == bola:
                    return [i,j]
                    
    def inicializarAbaco(self): #Inicializar o resetear abaco

        self.columnas = []
        self.columnasSuperiores = []

        y = 150
        x = 120

        valorAbaco = 512000000000*5 

        for i in range(10): #Llenando los valores y posiciones de cada bola superior
            self.columnasSuperiores.append([])
            for j in range(3):
                self.columnasSuperiores[len(self.columnasSuperiores)-1].append(Bola(valorAbaco,x,y))
                y+=65
            valorAbaco = valorAbaco/20
            x+=80
            y = 150

        x = 120
        y = 390

        valorAbaco = 512000000000

        for i in range(10): #Llenando los valores y posiciones de cada bola inferior.
            self.columnas.append([])
            for j in range(4):
                self.columnas[len(self.columnas)-1].append(Bola(valorAbaco,x,y))
                y+=65
            valorAbaco = valorAbaco/20
            x+=80
            y = 390
    
    def obtenerSumaSuperior(self): #Obtener suma de las bolas superiores
        suma = 0
        for i in self.obtenerBolasSuperiores():
            if i.estado == 2:
                suma+=i.valor
        return suma
    
    def obtenerSumaInferior(self): #Obtener suma de las bolas inferiores
        suma = 0
        for i in self.obtenerBolasInferiores():
            if i.estado == 2:
                suma+=i.valor
        return suma

    def obtenerSumaTotal(self):
        return (self.obtenerSumaInferior() + self.obtenerSumaSuperior()) #Obtener suma 
        #De todas las bolas

class DrawWidget(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(1000,800)
        self.abaco = Abaco() #Abaco regular
        self.abaco.inicializarAbaco() 
        self.abacoAzteca = AbacoAzteca() #Abaco azteca
        self.abacoAzteca.inicializarAbaco()
        self.abacoActivo = self.abaco #Abaco que se muestra en pantalla
        self.contador = None #Lleva la cuenta de cuantas veces se anima la bola
        self.numeroObjetivo = None #Numero final de la animacion de la bola
        self.timer = None #Timer que anima las bolas
        self.tipoNodo = None #En caso de que el nodo sea superior o inferior
        self.bolasAnimadas = None #Arreglo de las bolas que se van a animar
        self.numeroJuego = [None,None] #Numeros a los que se tienen que llegar para terminar el juego
        self.bolasReseteo = None #Bolas que serán reseteadas
        self.resetTimer = None #Timer que controla bolas reseteadas

    def resetearAbaco(self): #Resetear bolas
        self.bolasReseteo = [] 
        #Verificar cuales bolas están activas
        for i in self.abacoActivo.obtenerBolas():
            if i.estado == 2:
                self.bolasReseteo.append(i)
        
        #Animar la desactivación de las bolass
        self.resetTimer = QTimer(self)
        self.resetTimer.timeout.connect(self.animarRemoverBolas)
        self.resetTimer.start(300)

    #Metodo para animar cada bola que será reseteada
    def animarRemoverBolas(self):
        if len(self.bolasReseteo) > 0:
            if self.bolasReseteo[0].estado == 2:
                self.moverBolas(self.bolasReseteo[0])   
                del self.bolasReseteo[0]
            else:
                del self.bolasReseteo[0]
                self.animarRemoverBolas()

        else:
            self.resetTimer.stop()

        
    def paintEvent(self, event): #Método que dibuja toda la escena
            painter = QPainter(self)
            font = QFont()
            font.setPointSize(15)
            painter.setFont(font)
            
            #Dibujado del valor actual de las bolas
            painter.drawText(10,15,'Valor actual del abaco: ' +  str(self.abacoActivo.obtenerSumaTotal()))

            #Verificando si el usuario llega al numero objetivo
            if self.numeroJuego[0]!= None and self.numeroJuego[1] == None:
                painter.drawText(10,40,'Objetivo: ' + str(self.numeroJuego[0]))
                if self.numeroJuego[0] == self.abacoActivo.obtenerSumaTotal():
                    self.numeroJuego[1] = random.randrange(0,1000)
                    self.update()

            elif self.numeroJuego[0] != None and self.numeroJuego[1] != None:
                if self.numeroJuego[0] + self.numeroJuego[1] == self.abacoActivo.obtenerSumaTotal():
                    painter.setPen(QPen(QColor(qRgb(10,10,255)),3, Qt.SolidLine))
                    painter.drawText(600,60,'¡Correcto!')
                    painter.drawText(10,40,str(self.numeroJuego[0]) + ' + ' + str(self.numeroJuego[1]) + ' = ' + str(self.numeroJuego[0] + self.numeroJuego[1]))
                    self.update()
                else:
                    painter.drawText(10,40,str(self.numeroJuego[0]) + ' + ' + str(self.numeroJuego[1]) + ' = ? (Numero Objetivo)')

            painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))

            #Método para dibujar bolas
            def dibujarBola(bola):
                #Dibujado de bolas en base a la posicion
                posBola = {}
                posBola['x'] = bola.x
                posBola['y'] = bola.y
                radio = 25

                if bola.estado == 1:
                    painter.setBrush(QBrush(QColor(qRgb(90,90,90)), Qt.SolidPattern))
                else:
                    painter.setBrush(QBrush(QColor(qRgb(10,10,255)), Qt.SolidPattern))

                painter.drawEllipse(posBola['x']-radio, posBola['y']-radio,radio*2, radio*2)

            if self.abacoActivo == self.abaco:
                for i in range(10):
                    superior = self.abacoActivo.filaSuperior[i]
                    inferior = self.abacoActivo.columnas[i][3]
                    painter.drawLine(QLineF(superior.x,superior.y,inferior.x,inferior.y))
                
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                painter.drawLine(QLineF(90-30,70+120,840+30,70+120))
                painter.setPen(QPen(QColor(qRgb(0,0,0)),1, Qt.SolidLine))
                
                painter.setBrush(QBrush(QColor(qRgb(0,0,255)), Qt.SolidPattern))

                #Dibujar bolas inferiores
                for i in self.abacoActivo.obtenerBolasColumna():
                    dibujarBola(i)

                painter.setBrush(QBrush(QColor(qRgb(255,0,0)), Qt.SolidPattern))
                
                #Dibujar bolas superiores
                for i in self.abacoActivo.filaSuperior:
                    dibujarBola(i)

            else:
                for i in range(10):
                    superior = self.abacoActivo.columnasSuperiores[i][0]
                    inferior = self.abacoActivo.columnas[i][3]
                    painter.drawLine(QLineF(superior.x,superior.y,inferior.x,inferior.y))
                
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                painter.drawLine(QLineF(90-30,70+120+20+100,840+30,70+120+20+100))
                painter.setPen(QPen(QColor(qRgb(0,0,0)),1, Qt.SolidLine))
                
                painter.setBrush(QBrush(QColor(qRgb(0,0,255)), Qt.SolidPattern))

                #Dibujar bolas inferiores abaco azteca
                for i in self.abacoActivo.obtenerBolasInferiores():
                    dibujarBola(i)
                
                #Dibujar bolas superiores abaco azteca
                for i in self.abacoActivo.obtenerBolasSuperiores():
                    dibujarBola(i)
                
            painter.end()

    #Método de click, para mover las bolas presionadas
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            bola = self.obtenerBolaMasCerca([event.x(),event.y()])
            if bola != None:
                self.moverBolas(bola)

    #Mover bolas dependiendo del abaco normal o azteca
    def moverBolas(self,bola):
        if self.abacoActivo == self.abaco:
            self.moverBolasAbacoNormal(bola)
        else:
            self.moverBolaAbacoAzteca(bola)
    
    #Preparar valores para animar bolas del abaco azteca
    def moverBolaAbacoAzteca(self,bola):
        valor = False

        for i in self.abacoActivo.obtenerBolasSuperiores():
            if i == bola:
                valor = True
        
        pila,indiceBola = None,None

        columnas = None

        #Verificar si la bola es superior o inferior
        if valor == True:
            columnas = self.abacoActivo.columnasSuperiores
            pila,indiceBola = self.abacoActivo.obtenerIndice(bola,1)
        else:
            pila,indiceBola = self.abacoActivo.obtenerIndice(bola,0)
            columnas = self.abacoActivo.columnas

        self.tipoNodo = 0
        self.contador = 0
        self.numeroObjetivo = 10
        self.timer = QTimer(self)

        
        self.bolasAnimadas = []
        
        #Animando en base al estado, para saber la dirección en la que se mueve la bola
        if bola.estado == 1:
            if indiceBola != 0:
                if columnas[pila][indiceBola-1].estado == 2: 
                    self.bolasAnimadas = [bola]
                else:
                    #En caso de que el movimiento de las bolas mueva otras bolas
                    while indiceBola >= 0:
                        if columnas[pila][indiceBola].estado == 1:
                            self.bolasAnimadas.append(columnas[pila][indiceBola])
                            indiceBola-=1
                        else:
                            break
            else:
                self.bolasAnimadas = [bola]
        else:
            #Si la bola está en estado 2
            temp = 3
            if valor == True:
                temp = 2
            if indiceBola != temp:
                if columnas[pila][indiceBola+1].estado == 1:
                    self.bolasAnimadas = [bola]
                else:
                    self.bolasAnimadas = [bola]
                    indiceBola+=1
                    while True:
                        try:
                            if columnas[pila][indiceBola].estado == 2:
                                self.bolasAnimadas.append(columnas[pila][indiceBola])
                                indiceBola+=1
                            else:
                                break
                        except:
                            break
            else:
                self.bolasAnimadas = [bola]
        
        #Empezar la animacion de la bola
        self.timer.timeout.connect(self.animacionBola)
        self.timer.start(20)

    #Método para mover bolas del abaco regular
    def moverBolasAbacoNormal(self,bola):
        valor = False

        for i in self.abacoActivo.filaSuperior:
            if i == bola:
                valor = True

        if valor == True:
            #Si la bola es superior
            self.tipoNodo = 1
            self.contador = 0
            self.numeroObjetivo = 10
            self.timer = QTimer(self)
            self.bolasAnimadas = [bola]
            self.timer.timeout.connect(self.animacionBola) 
            self.timer.start(20)
        else:
            #Si la bola es inferior
            self.tipoNodo = 0
            self.contador = 0
            self.numeroObjetivo = 10
            self.timer = QTimer(self)

            pila,indiceBola = self.abacoActivo.obtenerIndice(bola)
            self.bolasAnimadas = []
            
            if bola.estado == 1: #Si el estado es 1
                if indiceBola != 0:
                    if self.abacoActivo.columnas[pila][indiceBola-1].estado == 2: 
                        self.bolasAnimadas = [bola]
                    else:
                        #Si las bolas animadas mueven otras bolas
                        while indiceBola >= 0:
                            if self.abacoActivo.columnas[pila][indiceBola].estado == 1:
                                self.bolasAnimadas.append(self.abacoActivo.columnas[pila][indiceBola])
                                indiceBola-=1
                            else:
                                break
                else:
                    self.bolasAnimadas = [bola]
            else:
                if indiceBola != 3:
                    if self.abacoActivo.columnas[pila][indiceBola+1].estado == 1:
                        self.bolasAnimadas = [bola]
                    else:
                        self.bolasAnimadas = [bola]
                        indiceBola+=1
                        while True:
                            try:
                                if self.abacoActivo.columnas[pila][indiceBola].estado == 2:
                                    self.bolasAnimadas.append(self.abacoActivo.columnas[pila][indiceBola])
                                    indiceBola+=1
                                else:
                                    break
                            except:
                                break
                else:
                    self.bolasAnimadas = [bola]
            
            self.timer.timeout.connect(self.animacionBola)
            self.timer.start(20)

    def resetearVariablesAnimacion(self): #Resetear variables de animacion al finalizar animaciones
        self.contador = None
        self.numeroObjetivo = None
        self.tipoNodo = None
        self.bolasAnimadas = None

    def animacionBola(self): #Animación de la bola
        if self.tipoNodo == 1:
            if self.bolasAnimadas[0].estado == 1:
                self.bolasAnimadas[0].y+=5 #Ir bajando 5 pixeles
                self.contador+=1
                
                if self.numeroObjetivo == self.contador: #En caso de finalice la animación
                    self.timer.stop()
                    self.bolasAnimadas[0].estado = 2
                    self.resetearVariablesAnimacion()
                    
            else:
                self.bolasAnimadas[0].y-=5 #Subir 5 pixeles
                self.contador+=1
                
                if self.numeroObjetivo == self.contador: #En caso de que finalice la animación
                    self.timer.stop()
                    self.bolasAnimadas[0].estado = 1
                    self.resetearVariablesAnimacion()
        else:
            if self.bolasAnimadas[0].estado == 1:
                for i in self.bolasAnimadas:
                    i.y-=5 #Bajar pixeles
                self.contador+=1
                
                if self.numeroObjetivo == self.contador: #Finalizar animación
                    self.timer.stop()
                    for i in self.bolasAnimadas:
                        i.estado = 2
                    self.resetearVariablesAnimacion()
                    
            else:
                for i in self.bolasAnimadas:
                    i.y+=5#Subir pixeles
                self.contador+=1 
                
                if self.numeroObjetivo == self.contador: #Finalizara animación
                    self.timer.stop()
                    for i in self.bolasAnimadas:
                        i.estado = 1
                    self.resetearVariablesAnimacion()

        self.update()
    
    def obtenerBolaMasCerca(self,punto): #Función para saber cuál bola es la que se presiona
        distancaCerca = math.inf
        bolaCerca = None

        for bola in self.abacoActivo.obtenerBolas():
            distancia = math.sqrt((bola.x - punto[0])**2 + (bola.y - punto[1])**2)

            if distancia < distancaCerca: #Obtener distancia más cercana
                distancaCerca = distancia
                bolaCerca = bola
        
        if distancaCerca <=20: #Regresar sólo si la posición presionada está dentro del radio de la bola
            return bolaCerca

class MainWindow(QWidget): #Ventana principal y componentes
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        self.setFixedSize(1000,800)

        self.mainLayout = QVBoxLayout()
        self.inputLayout = QHBoxLayout()
        self.comboBoxWidget = QComboBox()
        self.comboBoxWidget.insertItem(0,"Abaco Regular")
        self.comboBoxWidget.insertItem(1,"Abaco azteca")
        self.comboBoxWidget.currentIndexChanged.connect(self.cambiarAbaco)
        self.button = QPushButton("Empezar nuevo juego")
        self.button.clicked.connect(self.empezarJuego)
        self.drawWidget = DrawWidget()
        self.inputLayout.addWidget(self.button)
        self.inputLayout.addWidget(self.comboBoxWidget)
        self.mainLayout.addLayout(self.inputLayout)
        self.mainLayout.addWidget(self.drawWidget)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle("ABACO")

    def cambiarAbaco(self): #Alternar entre abaco normal y azteca
        if self.comboBoxWidget.currentIndex() == 0:
            self.drawWidget.abacoActivo.inicializarAbaco()
            self.drawWidget.abacoActivo = self.drawWidget.abaco
            self.drawWidget.update()
        if self.comboBoxWidget.currentIndex() == 1:
            self.drawWidget.abacoActivo.inicializarAbaco()
            self.drawWidget.abacoActivo = self.drawWidget.abacoAzteca
            self.drawWidget.update()

    def empezarJuego(self): #Empezar el juego
        self.drawWidget.resetearAbaco()
        self.drawWidget.numeroJuego = [random.randrange(0,1000),None]
        self.drawWidget.update()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())