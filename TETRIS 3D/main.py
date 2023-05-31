import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import math
import sys
from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtOpenGL import *
from PyQt5 import QtCore, QtWidgets, QtOpenGL
from PyQt5.QtCore import Qt
from random import randrange
from pygame import mixer
from copy import deepcopy
import numpy as np
from PyQt5.QtWidgets import *

window_width = 1000
window_height= 800
cubos = [] #Arreglo que conteiene todos los cubos que ya no son controlados por el usuario
base = [] #Arreglo que contiene todos los cubos de la base

#Desarrolladores 
#Mauricio Hernandez Cepeda
#Sonia Lizbeth Muñoz Barrientos
#José Antonio Cumpéan Morales
#Osiel Alejandro Ordoñez Cruz
print("Desarrolladores\nMauricio Hernandez Cepeda\nSonia Lizbeth Muñoz Barrientos\nJosé Antonio Cumpean Morales\nOsiel Alejandro Ordoñez Cruz")

class Sounds(object):
    def __init__(self):
        mixer.init()
        self.move = mixer.Sound('move.wav')
        self.rotate = mixer.Sound('rotate.wav')
        self.soundtrack = mixer.Sound('soundtrack.mp3')
        self.gameover = mixer.Sound('gameover.mp3')
        self.drop = mixer.Sound('drop.wav')
        self.drop.set_volume(1)
        self.soundtrack.set_volume(0.4)
        self.clearLine = mixer.Sound('breakLine.mpga')

class RgbColors(object): #Clase que contiene colores utilizados en la apliación
    def __init__(self):
        self.negro = (0/255,0/255,0/255)
        self.grisL = (80/255, 80/255, 80/255) 
        self.rosa = (248/255,45/255,151/255)
        self.morado = (197/255,1/255,226/255)
        self.verde = (46/255,248/255,160/255)
        self.rojo = (255/255,5/255,52/255)
        self.azul = (1/255,196/255,231/255) 
        self.amarillo = (231/255,197/255,0/255)
        self.verdeE = (30/255,255/255,5/255)

    def obtenerColorRandom(self): #Funcion para obtener un color aleatorio
        val = randrange(0,7)

        if val == 0:
            return self.rosa 
        if val == 1:
            return self.morado 
        if val == 2:
            return self.verde 
        if val == 3:
            return self.rojo 
        if val == 4: 
            return self.azul
        if val == 5:
            return self.amarillo
        if val == 6:
            return self.verdeE

class Figuras(object): #Clase que contiene las coordenadas iniciales de cada tipo de figura
    def __init__(self):
        self.color = RgbColors()
        self.l = [Cubo([0,40,-10],0),Cubo([0,38,-10],0),Cubo([0,36,-10],0),Cubo([2,36,-10],0)]
        self.j = [Cubo([0,40,-10],0),Cubo([0,38,-10],0),Cubo([0,36,-10],0),Cubo([-2,36,-10],0)]
        self.cuadrado = [Cubo([0,40,-10],0),Cubo([2,40,-10],0),Cubo([0,38,-10],0),Cubo([2,38,-10],0)]
        self.linea = [Cubo([0,40,-10],0),Cubo([0,38,-10],0),Cubo([0,36,-10],0),Cubo([0,34,-10],0)]
        self.s = [Cubo([0,40,-10],0),Cubo([2,40,-10],0),Cubo([0,38,-10],0),Cubo([-2,38,-10],0)]
        self.z = [Cubo([0,40,-10],0),Cubo([0,42,-10],0),Cubo([-2,42,-10],0),Cubo([2,40,-10],0)]
        self.cruz = [Cubo([0,40,-10],0),Cubo([0,42,-10],0),Cubo([-2,40,-10],0),Cubo([2,40,-10],0)]

        #Sirve para que a la hora de crear una figura, tenga esta forma

    def getRandomFigure(self): #Funcion para obtener una figura aleatoria
        val = randrange(0,7)

        if val == 0:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.l)
            for i in copia:
                i.color = color
            return deepcopy(copia)
        
        elif val == 1:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.j)
            for i in copia:
                i.color = color
            return deepcopy(copia)

        elif val == 2:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.cuadrado)
            for i in copia:
                i.color = color
            return deepcopy(copia)

        elif val == 3:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.linea)
            for i in copia:
                i.color = color
            return deepcopy(copia)

        elif val == 4:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.s)
            for i in copia:
                i.color = color
            return deepcopy(copia)

        elif val == 5:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.z)
            for i in copia:
                i.color = color
            return deepcopy(copia)
        
        elif val == 6:
            color = self.color.obtenerColorRandom()
            copia = deepcopy(self.cruz)
            for i in copia:
                i.color = color
            return deepcopy(copia)

class Figura(object): #Clase figura que guarda las coordenadas de cada bloque que la compone
    def __init__(self,coordenadas):
        self.coordenadas = coordenadas#Coordenadas de cada bloque que compone la figura

class Camera():
    def __init__(self):
        self.PI = 3.1415
        self.angle=3
        self.speed=0.3
        self.sight=100

        self.rotate_yz=-4
        self.rotate_xz=-90
        self.rad_yz=self.rotate_yz*self.PI/180.0
        self.rad_xz=self.rotate_xz*self.PI/180.0

        self.camera_x=-0.2740393373829466
        self.camera_y=30
        self.camera_z=65

        self.lookat_x= self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y= self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z= self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)
    
    def init(self):
        self.angle=3
        self.speed=0.3
        self.sight=100

        self.rotate_yz=-4
        self.rotate_xz=-90
        self.rad_yz=self.rotate_yz*self.PI/180.0
        self.rad_xz=self.rotate_xz*self.PI/180.0

        self.camera_x=-0.2740393373829466
        self.camera_y=30
        self.camera_z=65

        self.lookat_x= self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y= self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z= self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)

    def YawCamera(self,fAngle):
        self.rotate_xz=int(self.rotate_xz+fAngle)%360
        self.rad_xz=self.rotate_xz*self.PI / 180.0

        self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)

    def ZawCamera(self,fAngle):
        self.rotate_yz=int(self.rotate_yz+fAngle)%360
        self.rad_yz=self.rotate_yz*self.PI / 180.0

        #self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_xz)*math.cos(self.rad_yz)
        #self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_xz)
        #self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_xz)*math.sin(self.rad_yz)

    def PitchCamera(self,fAngle):
        self.rotate_yz=int(self.rotate_yz+fAngle)%360
        self.rad_yz=self.rotate_yz*self.PI/180.0

        self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xzWalkT)
        self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)

    def WalkStraight(self, fSpeed):
        self.camera_x =self.camera_x+fSpeed*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.camera_y =self.camera_y+fSpeed*math.sin(self.rad_yz)
        self.camera_z =self.camera_z+fSpeed*math.cos(self.rad_yz)*math.sin(self.rad_xz)

        self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)

    def WalkTransverse(self, fSpeed):
        self.camera_x+=fSpeed*math.cos(self.rad_yz)*math.sin(self.rad_xz)
        self.camera_z-=fSpeed*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)
    
    def WalkTransverseY(self, fSpeed):
        self.camera_y+=fSpeed*math.cos(self.rad_yz)*math.sin(self.rad_xz)
        self.camera_z-=fSpeed*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_x = self.camera_x + self.sight*math.cos(self.rad_yz)*math.cos(self.rad_xz)
        self.lookat_y = self.camera_y + self.sight*math.sin(self.rad_yz)
        self.lookat_z = self.camera_z + self.sight*math.cos(self.rad_yz)*math.sin(self.rad_xz)

class Cubo(object): #Clase que almacena la coordenada de un cubo y su color.
	def __init__(self,coordenadas,color):
		self.coordenadas = coordenadas
		self.color = color

class Ui_MainWindow(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Ui_MainWindow, self).__init__()
        self.widget = glWidget()
        self.pausa = False
        mainLayout = QtWidgets.QHBoxLayout()
        rightLayout = QtWidgets.QVBoxLayout()
        self.scoreLabel = QLabel("SCORE: 0")
        self.labelInstrucciones = QLabel("\n\nInstrucciones: \n\nRotacion: Q E SHIFT\n\nMover camara: ARRIBA ABAJO IZQUIERDA DERECHA\n\nMover pieza: A W S D CTRL\n\nPausa: Enter\n\nTirar pieza: Barra espaciadora\n\nReiniciar Camara: F\n\nReiniciar partida: R  ")
        rightLayout.addWidget(self.scoreLabel)
        rightLayout.addWidget(self.labelInstrucciones)
        mainLayout.addWidget(self.widget)
        mainLayout.addLayout(rightLayout)
        
        self.setStyleSheet("background-color: #000; font-size: 20px;")
        self.scoreLabel.setStyleSheet("font-size: 30px; color: #fff;")
        self.labelInstrucciones.setStyleSheet("color: #fff;")

        rightLayout.setContentsMargins(0,0,50,0)
        mainLayout.setContentsMargins(0,0,0,0)
        
        rightLayout.setAlignment(Qt.AlignCenter)
        self.setLayout(mainLayout)
        self.timer = QtCore.QTimer(self)  # period, in milliseconds
        self.timer.timeout.connect(lambda: self.widget.bajarFigura(self.widget.figuraActual.coordenadas)) #Cada 600 milisegundos va a llamar bajarFigura
        self.timer.timeout.connect(self.verificarScore) #Cada 600 milisegundos actualiza el score en base al score del widget glWidget

        self.timer.start(600)
        self.ultimaRotacion = -20
        self.ultimaRotacionCamara = 0
        self.rotacionVertical = 0
        for i in range(3):
            self.RotacionAbajo()

    def verificarScore(self): #Actualiza el score
        self.scoreLabel.setText("SCORE: " + str(self.widget.score))
        color = self.widget.figuraActual.coordenadas[0].color
        self.scoreLabel.setStyleSheet("font-size: 30px; color: rgb(" + str(color[0]*255) + "," + str(color[1]*255) + "," + str(color[2]*255) + ")") 
        self.labelInstrucciones.setStyleSheet("color: rgb(" + str(color[0]*255) + "," + str(color[1]*255) + "," + str(color[2]*255) + ")") 
        if self.widget.derrota == True:
            self.scoreLabel.setText("GAME OVER\n\n"+  self.scoreLabel.text())
            self.timer.stop()

    def moveCameraRight(self): #Mover camara hacia la derecha
        self.RotacionDerecha()
        for i in range(20):
            self.MoverCamaraDerecha()

    def moverDerecha(self): #Mover la camara y hacer animación de movimiento de camara, además de controlar cuanto gira
        for i in range(18):
            self.moveCameraRight()
            if i%2 == 0:
                self.widget.updateGL()
        for i in self.widget.figuraActual.coordenadas:
            i.coordenadas[1] +=2
        self.ultimaRotacion = self.widget.contador
        self.ultimaRotacionCamara +=1
        if self.ultimaRotacionCamara == 4:
            self.ultimaRotacionCamara = 0 

    def moverDerechaNoUpdate(self): #Mover la camara cierto angulo pero sin animación
        for i in range(18):
            self.moveCameraRight()
        self.ultimaRotacion = self.widget.contador
        self.ultimaRotacionCamara +=1
        if self.ultimaRotacionCamara == 4:
            self.ultimaRotacionCamara = 0 

    def keyPressEvent(self,e): #Todos los contorles básicos
        if e.key() == 16777220:
            if self.timer.isActive(): #Pause
                self.timer.stop()
                mixer.pause()
                self.pausa = True
            else:
                mixer.unpause()
                self.timer.start(600)
                self.pausa = False
        if self.pausa == False:
            if e.key() == Qt.Key_Right and self.widget.contador - self.ultimaRotacion >= 0.0001:
                self.moverDerecha()

            if e.key() == 16777249:
                self.widget.bajarFigura(self.widget.figuraActual.coordenadas)

            if e.key() == Qt.Key_D:
                if self.ultimaRotacionCamara == 0:
                    self.widget.moverFiguraDerecha()
                if self.ultimaRotacionCamara == 1:
                    self.widget.moverFiguraAtras()

                if self.ultimaRotacionCamara == 2:
                    self.widget.moverFiguraIzquierda()

                if self.ultimaRotacionCamara == 3:
                    self.widget.moverFiguraFrente()
                self.widget.updateGL()
            if e.key() == Qt.Key_A:
                if self.ultimaRotacionCamara == 0:
                    self.widget.moverFiguraIzquierda()
                if self.ultimaRotacionCamara == 1:
                    self.widget.moverFiguraFrente()

                if self.ultimaRotacionCamara == 2:
                    self.widget.moverFiguraDerecha()

                if self.ultimaRotacionCamara == 3:
                    self.widget.moverFiguraAtras()
                self.widget.updateGL()
            if e.key() == Qt.Key_W:
                if self.ultimaRotacionCamara == 0:
                    self.widget.moverFiguraFrente()
                if self.ultimaRotacionCamara == 1:
                    self.widget.moverFiguraDerecha()

                if self.ultimaRotacionCamara == 2:
                    self.widget.moverFiguraAtras()

                if self.ultimaRotacionCamara == 3:
                    self.widget.moverFiguraIzquierda()
                self.widget.updateGL()

            if e.key() == Qt.Key_Up:
                if self.rotacionVertical >0:
                    if self.ultimaRotacionCamara != 0:
                        ultima = deepcopy(self.ultimaRotacionCamara)
                        for i in range((4-ultima)):
                            self.moverDerechaNoUpdate()
                        self.RotacionArriba()
                        for i in range((ultima)):
                            self.moverDerechaNoUpdate()
                    else:
                        self.RotacionArriba()
                    
                    self.widget.updateGL()
                    self.rotacionVertical-=1

            if e.key() == Qt.Key_Down:
                if self.rotacionVertical <=11 :
                    if self.ultimaRotacionCamara != 0:
                        ultima = deepcopy(self.ultimaRotacionCamara)
                        for i in range((4-ultima)):
                            self.moverDerechaNoUpdate()
                        self.RotacionAbajo()
                        for i in range((ultima)):
                            self.moverDerechaNoUpdate()
                    else:
                        self.RotacionAbajo()
                    self.widget.updateGL()
                    self.rotacionVertical +=1

            if e.key() == Qt.Key_S:
                if self.ultimaRotacionCamara == 0:
                    self.widget.moverFiguraAtras()
                if self.ultimaRotacionCamara == 1:
                    self.widget.moverFiguraIzquierda()

                if self.ultimaRotacionCamara == 2:
                    self.widget.moverFiguraFrente()

                if self.ultimaRotacionCamara == 3:
                    self.widget.moverFiguraDerecha()
                self.widget.updateGL()

            if e.key() == Qt.Key_Space: #Tirar figura
                mixer.Sound.play(self.widget.sound.drop)
                self.widget.tirarFigura()
                self.widget.updateGL()
                

            if e.key() == Qt.Key_Q: #Rotar figura y
                self.widget.rotarFiguraX()
                self.widget.actualizarVisualizacion()
                self.widget.updateGL()

            if e.key() == Qt.Key_E: #Rotar figura x
                self.widget.rotarFiguraY()
                self.widget.actualizarVisualizacion()
                self.widget.updateGL()

            if e.key() == 16777248: #Rotar figura z 
                self.widget.rotarFiguraZ()
                self.widget.actualizarVisualizacion()
                self.widget.updateGL()

            if e.key() == Qt.Key_F:
                self.ultimaRotacion = -20
                self.ultimaRotacionCamara = 0
                self.rotacionVertical = 0
                self.widget.camera.init()
                self.widget.initCamera()
                for i in range(3):
                    self.RotacionAbajo()
                self.widget.updateGL()

            if e.key() == Qt.Key_R:
                self.ultimaRotacion = -20
                self.ultimaRotacionCamara = 0
                self.rotacionVertical = 0
                self.widget.camera.init()
                self.widget.initCamera()
                for i in range(3):
                    self.RotacionAbajo()
                self.widget.updateGL()
                self.widget.score = 0
                
                while(len(cubos)>0):
                    del cubos[0]

                if self.timer.isActive() == False:
                    self.timer.start(600)
                self.widget.derrota = False
                self.widget.figuraActual = Figura(self.widget.figuras.getRandomFigure())
                self.widget.visualizacionFinalFigura = deepcopy(self.widget.figuraActual.coordenadas) #Generacion de primer figura
                self.widget.actualizarVisualizacion()
                mixer.Sound.stop(self.widget.sound.soundtrack)
                mixer.Sound.play(self.widget.sound.soundtrack,loops=-1)


    def RotacionDerecha(self):
        
        self.widget.camera.YawCamera(5.0)
        #self.widget.rtz+=0.3

    def RotacionIzquierda(self):
        
        self.widget.camera.YawCamera(-5.0)
        #self.widget.rtz+=0.3

    def RotacionArriba(self):
        self.widget.camera.ZawCamera(5.0)
        for i in range(20):
            self.MoverCamaraArriba()
        for i in range(10):
            self.Alejamiento()
        self.widget.paintGL()
        
        #self.widget.rtz+=0.3

    def RotacionAbajo(self):
        self.widget.camera.ZawCamera(-5.0)
        for i in range(20):
            self.MoverCamaraAbajo()
        for i in range(10):
            self.Acercamiento()
        self.widget.paintGL()
        #self.widget.rtz+=0.3

    def MoverCamaraIzquierda(self):
        
        self.widget.camera.WalkTransverse(-1*self.widget.camera.speed)
        #self.widget.camera.WalkStraight(-self.widget.camera.speed)

    def MoverCamaraArriba(self):
       
        self.widget.camera.WalkTransverseY(self.widget.camera.speed)
        #self.widget.camera.WalkStraight(self.widget.camera.speed)

    def MoverCamaraAbajo(self):
        
        self.widget.camera.WalkTransverseY(-1*self.widget.camera.speed)
        #self.widget.camera.WalkStraight(-self.widget.camera.speed)

    def MoverCamaraDerecha(self):
        self.widget.camera.WalkTransverse(self.widget.camera.speed)
        #self.widget.camera.WalkStraight(self.widget.camera.speed)

    def Acercamiento(self):
        
        self.widget.rtz = self.widget.rtz + 0.31
    def Alejamiento(self):
        
        self.widget.rtz = self.widget.rtz - 0.3
    #self.widget.camera.WalkStraight(self.widget.camera.speed)

class glWidget(QGLWidget):
    def __init__(self, parent=None):
        QGLWidget.__init__(self, parent)
        self.width=800
        self.height=600
        self.derrota = False #variable si para saber si perdio
        self.setMinimumSize(self.width, self.height)
        self.aspect = self.width / float(self.height)
        self.V=-0.0
        self.rotX = True
        self.rotY = 0.0
        self.rotZ = 0.0
        self.contador = 0
        self.score = 0
        self.rtx=0
        self.rty=0
        self.rtz=0

        self.sound = Sounds()
        mixer.Sound.play(self.sound.soundtrack,loops=-1)
        
        self.color = RgbColors()

        for i in range(10): #Generacion de la base
            for j in range(5):
                base.append(Cubo([-j*2,0,-i*2],self.color.grisL))
            for j in range(6):
                base.append(Cubo([j*2,0,-i*2],self.color.grisL))

        self.figuras = Figuras()
        self.figuraActual = Figura(self.figuras.getRandomFigure())
        self.visualizacionFinalFigura = deepcopy(self.figuraActual.coordenadas) #Generacion de primer figura

        self.actualizarVisualizacion()
        self.camera=Camera()

    def initCamera(self):
        self.V=-0.0
        self.rotX = True
        self.rotY = 0.0
        self.rotZ = 0.0
        self.contador = 0
        self.score = 0
        self.rtx=0
        self.rty=0
        self.rtz=0

    def tirarFigura(self): #Tirar figura baja la figura hacia su punto maximo
        valor = True 
        while valor == True: #Bajar figura hasta que ya no pueda bajar mas
            valor = self.bajarFiguraNoAnimacion(self.figuraActual.coordenadas) #Cambiar en caso de querer animacion de bajada

    def generarFiguraNueva(self): #Genera figura nueva 
        for i in self.figuraActual.coordenadas: #Agregar todos los cubos de la figura actual al arreglo cubos
            cubos.append(i)
        self.figuraActual = Figura(self.figuras.getRandomFigure()) #Generar una nueva figura actual
        valor = True 

        while valor == True:
            valor = self.verificarLineas() #Verifica que alguna linea este llena para borrarla

        self.actualizarVisualizacion() #Actualizar visualizacion de la figura en su punto mas bajo

    def actualizarVisualizacion(self): #Actualiza la visualizacion de la figura en su punto mas bajo
        self.visualizacionFinalFigura = deepcopy(self.figuraActual.coordenadas) #Genera una copia de la figura actual
        valor = True 

        while valor == True: 
            valor = self.bajarFigura(self.visualizacionFinalFigura) #Es bajada como si la tiraramos

    def rotarFiguraZ(self): 
        copyFigura = deepcopy(self.figuraActual)
        #Intercambiar posiciones en X y Y
        coordenada = self.figuraActual.coordenadas[0].coordenadas[0]
        coordenaday = self.figuraActual.coordenadas[0].coordenadas[1]

        copy = deepcopy(self.figuraActual.coordenadas[0].coordenadas[0])
        self.figuraActual.coordenadas[0].coordenadas[0] = -40 + self.figuraActual.coordenadas[0].coordenadas[1]
        self.figuraActual.coordenadas[0].coordenadas[1] = 40 - copy
        copy = deepcopy(self.figuraActual.coordenadas[1].coordenadas[0])
        self.figuraActual.coordenadas[1].coordenadas[0] = -40 + self.figuraActual.coordenadas[1].coordenadas[1]
        self.figuraActual.coordenadas[1].coordenadas[1] = 40 - copy
        copy = deepcopy(self.figuraActual.coordenadas[2].coordenadas[0])
        self.figuraActual.coordenadas[2].coordenadas[0] = -40 + self.figuraActual.coordenadas[2].coordenadas[1]
        self.figuraActual.coordenadas[2].coordenadas[1] = 40 - copy
        copy = deepcopy(self.figuraActual.coordenadas[3].coordenadas[0])
        self.figuraActual.coordenadas[3].coordenadas[0] = -40 + self.figuraActual.coordenadas[3].coordenadas[1]
        self.figuraActual.coordenadas[3].coordenadas[1] = 40 - copy

        coordenaday = coordenaday - 40
        
        for i in self.figuraActual.coordenadas: 
            i.coordenadas[0]+=coordenada
            i.coordenadas[1]+=coordenada
            i.coordenadas[0]-=coordenaday
            i.coordenadas[1]+=coordenaday

        if (self.verificarPosicionIncorrecta() == False):  #Verifica que la posicion nueva no esté fuera de los limites o afectando a otra figura
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.rotate)

    def rotarFiguraX(self):
        copyFigura = deepcopy(self.figuraActual)
        #Intercambiar posiciones en X y Z

        coordenada = self.figuraActual.coordenadas[0].coordenadas[0]
        coordenadaz = self.figuraActual.coordenadas[0].coordenadas[2]
        copy = deepcopy(self.figuraActual.coordenadas[0].coordenadas[0])
        self.figuraActual.coordenadas[0].coordenadas[0] = 10 + self.figuraActual.coordenadas[0].coordenadas[2]
        self.figuraActual.coordenadas[0].coordenadas[2] = -10 - copy
        copy = deepcopy(self.figuraActual.coordenadas[1].coordenadas[0])
        self.figuraActual.coordenadas[1].coordenadas[0] = 10 + self.figuraActual.coordenadas[1].coordenadas[2]
        self.figuraActual.coordenadas[1].coordenadas[2] = -10 -copy
        copy = deepcopy(self.figuraActual.coordenadas[2].coordenadas[0])
        self.figuraActual.coordenadas[2].coordenadas[0] = 10 + self.figuraActual.coordenadas[2].coordenadas[2]
        self.figuraActual.coordenadas[2].coordenadas[2] = -10 -copy
        copy = deepcopy(self.figuraActual.coordenadas[3].coordenadas[0])
        self.figuraActual.coordenadas[3].coordenadas[0] = 10 + self.figuraActual.coordenadas[3].coordenadas[2]
        self.figuraActual.coordenadas[3].coordenadas[2] = -10 -copy

        coordenadaz = coordenadaz - -10
        
        for i in self.figuraActual.coordenadas: 
            i.coordenadas[0]+=coordenada
            i.coordenadas[2]+=coordenada
            i.coordenadas[0]-=coordenadaz
            i.coordenadas[2]+=coordenadaz

        if (self.verificarPosicionIncorrecta() == False): #Verifica que la posicion nueva no esté fuera de los limites o afectando a otra figura
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.rotate)

    def rotarFiguraY(self):
        copyFigura = deepcopy(self.figuraActual)
        coordenaday = self.figuraActual.coordenadas[0].coordenadas[1]
        coordenadaz = self.figuraActual.coordenadas[0].coordenadas[2]
        #Intercambiar posiciones en Y y Z
        copy = deepcopy(self.figuraActual.coordenadas[0].coordenadas[1])
        self.figuraActual.coordenadas[0].coordenadas[1] = 50 + self.figuraActual.coordenadas[0].coordenadas[2]
        self.figuraActual.coordenadas[0].coordenadas[2] = 50 - copy
        copy = deepcopy(self.figuraActual.coordenadas[1].coordenadas[1])
        self.figuraActual.coordenadas[1].coordenadas[1] = 50 + self.figuraActual.coordenadas[1].coordenadas[2]
        self.figuraActual.coordenadas[1].coordenadas[2] = 50 - copy
        copy = deepcopy(self.figuraActual.coordenadas[2].coordenadas[1])
        self.figuraActual.coordenadas[2].coordenadas[1] = 50 + self.figuraActual.coordenadas[2].coordenadas[2]
        self.figuraActual.coordenadas[2].coordenadas[2] = 50 - copy
        copy = deepcopy(self.figuraActual.coordenadas[3].coordenadas[1])
        self.figuraActual.coordenadas[3].coordenadas[1] = 50 + self.figuraActual.coordenadas[3].coordenadas[2]
        self.figuraActual.coordenadas[3].coordenadas[2] = 50 - copy

        contador = 0
        while(self.figuraActual.coordenadas[0].coordenadas[1] != coordenaday):
            self.figuraActual.coordenadas[0].coordenadas[1]-=2
            self.figuraActual.coordenadas[1].coordenadas[1]-=2
            self.figuraActual.coordenadas[2].coordenadas[1]-=2
            self.figuraActual.coordenadas[3].coordenadas[1]-=2
            contador+=1
            if contador == 100:
                while(self.figuraActual.coordenadas[0].coordenadas[1] != coordenaday):
                    self.figuraActual.coordenadas[0].coordenadas[1]+=2
                    self.figuraActual.coordenadas[1].coordenadas[1]+=2
                    self.figuraActual.coordenadas[2].coordenadas[1]+=2
                    self.figuraActual.coordenadas[3].coordenadas[1]+=2

        contador = 0

        while(self.figuraActual.coordenadas[0].coordenadas[2] != coordenadaz):
             self.figuraActual.coordenadas[0].coordenadas[2]-=2
             self.figuraActual.coordenadas[1].coordenadas[2]-=2
             self.figuraActual.coordenadas[2].coordenadas[2]-=2
             self.figuraActual.coordenadas[3].coordenadas[2]-=2
             contador+=1
             if contador == 100:
                while(self.figuraActual.coordenadas[0].coordenadas[2] != coordenadaz):
                    self.figuraActual.coordenadas[0].coordenadas[2]+=2
                    self.figuraActual.coordenadas[1].coordenadas[2]+=2
                    self.figuraActual.coordenadas[2].coordenadas[2]+=2
                    self.figuraActual.coordenadas[3].coordenadas[2]+=2
                    

        if (self.verificarPosicionIncorrecta() == False): 
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.rotate)

    def CuboTriangles(self): #Dibujar todos los cubos y las lineas
        if self.rotX:
            self.camera.WalkStraight(self.V)
			#self.V-=0.1
        for i in base:
            self.dibujarCubo(i)

            #Dibujar lineas del area
        for i in cubos:
            self.dibujarCubo(i)
        
        for i in self.figuraActual.coordenadas: 
            self.dibujarCubo(i)
            
        for i in self.visualizacionFinalFigura:
            self.dibujarCubo(i)


    def paintGL(self): #Dibujado de toda la escena
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.setProjection()
        glEnable(GL_DEPTH_TEST)
        #glTranslatef(rtx,rty,rtz)
        glTranslatef(self.rtx,self.rty,self.rtz)
        self.CuboTriangles()    
        #glutWireTeapot(0.5)
        #glutWireSphere(0.5,10,10)		
        glFlush()

    def bajarFigura(self,figura): #Baja la figura que recibe una cordenada en Y, en caso de que llegue al limite, es decir,la base o otra figura, no baja.
        move = True
        for i in figura:
            if i.coordenadas[1] == 2:
                move = False
        
        for i in figura:
            k = deepcopy(i.coordenadas)
            k[1]-=2
            for j in cubos:
                if k == j.coordenadas:
                    move = False
                
        if move == True:
            for i in figura:
                    i.coordenadas[1]-=2
        else:
            if figura == self.figuraActual.coordenadas:
                if(self.verificarDerrota()) == False:
                    self.generarFiguraNueva()

        self.contador+=0.0001
        self.contador = np.round(self.contador,5)

        if figura == self.figuraActual.coordenadas:
            self.updateGL()
        return move

    def bajarFiguraNoAnimacion(self,figura): #Baja la figura que recibe una cordenada en Y, en caso de que llegue al limite, es decir,la base o otra figura, no baja.
        move = True
        for i in figura:
            if i.coordenadas[1] == 2:
                move = False
        
        for i in figura:
            k = deepcopy(i.coordenadas)
            k[1]-=2
            for j in cubos:
                if k == j.coordenadas:
                    move = False
                
        if move == True:
            for i in figura:
                    i.coordenadas[1]-=2
        else:
            if figura == self.figuraActual.coordenadas:
                if(self.verificarDerrota()) == False:
                    self.generarFiguraNueva()

        self.contador+=0.0001
        self.contador = np.round(self.contador,5)

        return move

    def moverFiguraDerecha(self): #Mover figura hacia la derecha
        copyFigura = deepcopy(self.figuraActual)
        for i in self.figuraActual.coordenadas:
            i.coordenadas[0]+=2

        if (self.verificarPosicionIncorrecta() == False): #Verifica que no tenga posicion incorrecta
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.move)
        self.actualizarVisualizacion()

    def moverFiguraIzquierda(self): #Mover hacia la izquierda
        copyFigura = deepcopy(self.figuraActual)
        for i in self.figuraActual.coordenadas:
            i.coordenadas[0]-=2
        if (self.verificarPosicionIncorrecta() == False): #Verifica que no tenga posicion incorrecta
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.move)
        self.actualizarVisualizacion()

    def moverFiguraFrente(self):
        copyFigura = deepcopy(self.figuraActual)
        for i in self.figuraActual.coordenadas:
            i.coordenadas[2]-=2
        if (self.verificarPosicionIncorrecta() == False):#Verifica que no tenga posicion incorrecta
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.move)
        self.actualizarVisualizacion()

    def moverFiguraAtras(self):
        copyFigura = deepcopy(self.figuraActual)
        for i in self.figuraActual.coordenadas:
            i.coordenadas[2]+=2
        if (self.verificarPosicionIncorrecta() == False):#Verifica que no tenga posicion incorrecta
            self.figuraActual = copyFigura
        else:
            mixer.Sound.play(self.sound.move)
        self.actualizarVisualizacion()

    def initializeGL(self):
        #glViewport(0, 0, self.width, self.height) # Esta linea no estaba en el demo original

        self.ratio=1.0*self.width/self.height

        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45,self.ratio, 0.01, 100)
        glViewport(0,0,self.width,self.height)
        glMatrixMode(GL_MODELVIEW)

    def setProjection(self):
        glLoadIdentity()
        gluLookAt(self.camera.camera_x, self.camera.camera_y, self.camera.camera_z, self.camera.lookat_x, self.camera.lookat_y, self.camera.lookat_z, 0.0, 1.0, 0.0)

    def dibujarCubo(self,i): #Dibuja cubo en base a las coordenadas que reciba y al color
        
        x = i.coordenadas[0]
        y = i.coordenadas[1]
        z = i.coordenadas[2]
        color = i.color
        # Cara roja Frontal
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f( 1.0+x, 1.0+y,1.0+z)
        glVertex3f( 1.0+x,-1.0+y,1.0+z)
        glVertex3f(-1.0+x,-1.0+y, 1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x,1.0+y, 1.0+z)
        glVertex3f(-1.0+x,-1.0+y, 1.0+z)
        glVertex3f( 1.0+x, 1.0+y,1.0+z)        
        glEnd()

        # Cara roja trasera
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f( 1.0+x, 1.0+y,-1.0+z)
        glVertex3f( 1.0+x,-1.0+y,-1.0+z)
        glVertex3f(-1.0+x,-1.0+y, -1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x,1.0+y, -1.0+z)
        glVertex3f(-1.0+x,-1.0+y, -1.0+z)
        glVertex3f( 1.0+x, 1.0+y,-1.0+z)        
        glEnd()

        # Cara Amarilla  Izquierda
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x, 1.0+y, 1.0+z)
        glVertex3f(-1.0+x, 1.0+y,-1.0+z)
        glVertex3f(-1.0+x,-1.0+y,-1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x,-1.0+y,1.0+z)
        glVertex3f(-1.0+x,-1.0+y,-1.0+z)
        glVertex3f(-1.0+x, 1.0+y, 1.0+z)        
        glEnd()

        # Cara Azul  Derecha
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(1.0+x, 1.0+y, 1.0+z)
        glVertex3f(1.0+x, 1.0+y,-1.0+z)
        glVertex3f(1.0+x,-1.0+y,-1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(1.0+x,-1.0+y,1.0+z)
        glVertex3f(1.0+x,-1.0+y,-1.0+z)
        glVertex3f(1.0+x, 1.0+y, 1.0+z)        
        glEnd()

        # Cara Morada: Inferior
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f( 1.0+x,-1.0+y, 1.0+z)
        glVertex3f( 1.0+x,-1.0+y,-1.0+z)
        glVertex3f(-1.0+x,-1.0+y,-1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x,-1.0+y,1.0+z)
        glVertex3f(-1.0+x,-1.0+y,-1.0+z)
        glVertex3f( 1.0+x,-1.0+y, 1.0+z)        
        glEnd() 

        # Cara Morada: Superior
        glBegin(GL_TRIANGLES)
        glColor3f(color[0],color[1],color[2])
        glVertex3f( 1.0+x,1.0+y, 1.0+z)
        glVertex3f( 1.0+x,1.0+y,-1.0+z)
        glVertex3f(-1.0+x,1.0+y,-1.0+z)
        glColor3f(color[0],color[1],color[2])
        glVertex3f(-1.0+x,1.0+y,1.0+z)
        glVertex3f(-1.0+x,1.0+y,-1.0+z)
        glVertex3f( 1.0+x,1.0+y, 1.0+z)        
        glEnd() 

        colorLineas = 0,0,0
        for j in self.visualizacionFinalFigura:
            if i == j:
                colorLineas = (1,1,1)
        
        #Aristas cara frontal
        glBegin(GL_LINES) #Superior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y,1+z+0.1)
        glVertex3f(1+x,1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y+0.05,1+z+0.1)
        glVertex3f(1+x,1+y+0.05,1+z+0.1)
        glEnd()

        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y,1+z+0.1)
        glVertex3f(1+x,-1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y+0.05,1+z+0.1)
        glVertex3f(1+x,-1+y+0.05,1+z+0.1)
        glEnd()

        glBegin(GL_LINES)#Izquierda
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y,1+z+0.1)
        glVertex3f(-1+x,-1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x-0.1,1+y,1+z+0.1)
        glVertex3f(-1+x-0.1,-1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)#Derecha
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,1+y,1+z+0.1)
        glVertex3f(1+x,-1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x-0.1,1+y,-1+z+0.1)
        glVertex3f(1+x-0.1,-1+y,-1+z+0.1)
        glEnd()


        #Aristas cara trasera
        glBegin(GL_LINES) #Superior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y,-1+z-0.1)
        glVertex3f(1+x,1+y,-1+z-0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y+0.05,-1+z-0.1)
        glVertex3f(1+x,1+y+0.05,-1+z-0.1)
        glEnd()

        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y,-1+z-0.1)
        glVertex3f(1+x,-1+y,-1+z-0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y+0.05,-1+z-0.1)
        glVertex3f(1+x,-1+y+0.05,-1+z-0.1)
        glEnd()

        glBegin(GL_LINES)#Izquierda
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y,-1+z-0.1)
        glVertex3f(-1+x,-1+y,-1+z-0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x-0.1,1+y,-1+z-0.1)
        glVertex3f(-1+x-0.1,-1+y,-1+z-0.1)
        glEnd()
        
        glBegin(GL_LINES)#Derecha
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,1+y,-1+z-0.1)
        glVertex3f(1+x,-1+y,-1+z-0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x+0.1,1+y,-1+z-0.1)
        glVertex3f(1+x+0.1,-1+y,-1+z-0.1)
        glEnd()

        #Aristas cara izquierda
        glBegin(GL_LINES) #Superior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y,-1+z+0.1)
        glVertex3f(-1+x,1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,1+y+0.05,-1+z)
        glVertex3f(-1+x,1+y+0.05,1+z)
        glEnd()

        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y,-1+z)
        glVertex3f(-1+x,-1+y,1+z)
        glEnd()

        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(-1+x,-1+y+0.05,-1+z)
        glVertex3f(-1+x,-1+y+0.05,1+z)
        glEnd()

        #Aristas cara derecha
        glBegin(GL_LINES) #Superior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,1+y,-1+z+0.1)
        glVertex3f(1+x,1+y,1+z+0.1)
        glEnd()
        
        glBegin(GL_LINES)
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,1+y+0.05,-1+z)
        glVertex3f(1+x,1+y+0.05,1+z)
        glEnd()

        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,-1+y,-1+z)
        glVertex3f(1+x,-1+y,1+z)
        glEnd()


        glBegin(GL_LINES)#Inferior
        glColor3f(colorLineas[0],colorLineas[1],colorLineas[2])
        glVertex3f(1+x,-1+y+0.05,-1+z)
        glVertex3f(1+x,-1+y+0.05,1+z)
        glEnd()

    
    
    def verificarPosicionIncorrecta(self): 
        move = True 
        for i in self.figuraActual.coordenadas:
            if i.coordenadas[0] == -10 or i.coordenadas[0] == 12: #Verifica que no se salga en X
                move = False 
            if i.coordenadas[2] == -20 or i.coordenadas[2] == 2: #Verifica que no se salga en Z
                move = False 
            for j in cubos: #Verifica que no choque la figura con otra figura almacenada
                if i.coordenadas == j.coordenadas:
                    move = False 
        return move

    def verificarLineas(self): #Verifica que alguna linea este llena
        valor = False
        for i in range(40):
            if self.verificarLinea(i): #Verifica que la linea cuente con 100 bloques dibujados
                self.eliminarLinea(i) #Elimina dicha linea
                mixer.Sound.play(self.sound.clearLine)
                self.bajarFiguras() #Baja todas las demás lineas 
                valor = True
                break
        return valor #Retornar valor para seguir verificando si alguna otra linea se lleno al eliminar esta
    
    def bajarFiguras(self): #Verifica que una linea este vacia y la de arriba este llena, en dicho caso, baja todas las de arriba.
        punto = -1
        for i in range(2,41):
            if self.verificarLineaVacia(i):
                print(i)
                if self.verificarLineaVacia(i+2) == False:
                    punto = i
                break
        
        if punto != -1:
            for i in range(punto,41):
                self.bajarLinea(i)
            self.bajarFiguras()
    
    def bajarLinea(self,linea): #Baja una linea completa en Y
        for j in range(-12,12):
            for k in range(-22,4):
                if self.buscarCubo([j,linea,k])[0] == True:
                    self.buscarCubo([j,linea,k])[1].coordenadas[1]-=2

    def eliminarLinea(self,linea): #Elimina una linea completa
        contador = 0
        for j in range(-12,12):
            for k in range(-22,4):
                if self.buscarCubo([j,linea,k])[0] == True:
                    del cubos[self.buscarCubo([j,linea,k])[2]]
                    contador+=1 

        self.score+=1

        for i in cubos:
            contador+=1

    def verificarLineaVacia(self,linea): #Verifica que no exista ningun bloque en la linea 
        contador = 0
        for j in range(-12,12):
            for k in range(-22,4):
                if self.buscarCubo([j,linea,k])[0] == True:
                    contador+=1
        if contador == 0:
            return True 
        else:
            return False

    def verificarLinea(self,linea): #Verifica que una linea tenga 100 cubos almacenados.
        contador = 0
        for j in range(-12,12):
            for k in range(-22,4):
                if self.buscarCubo([j,linea,k])[0] == True:
                    contador+=1
        if contador == 100:
            return True 
        else:
            return False

    def buscarCubo(self,coordenadas): #Busca un cubo en los cubos almacenados
        j = 0
        for i in cubos:
            if i.coordenadas == coordenadas:
                return [True,i,j]
            j+=1
        return [False,None]

    def verificarDerrota(self): #Si una figura llega al limite, el juego termina
        move = False 
        for i in cubos:
            if i.coordenadas[1] == 40:
                move = True
                self.derrota = True 
                mixer.Sound.stop(self.sound.soundtrack)
                mixer.Sound.play(self.sound.gameover)
                break
        return move

if __name__ == '__main__':    
    app = QtWidgets.QApplication(sys.argv)    
    Form = QtWidgets.QMainWindow()
    ui = Ui_MainWindow(Form)    
    ui.show()    
    sys.exit(app.exec_())
