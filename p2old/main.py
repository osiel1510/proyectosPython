from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import numpy as np  

class MainWindow(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        
        self.width = 800
        self.height = 800
        self.setFixedSize(800,800)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.tamanio = [self.width,self.width]
        self.tamanioVertices = 5 #Radio de los puntos dibujados
        self.mainCircle = [self.tamanio[0]/2,self.tamanio[1]/2,100,100]
        self.puntos = {}
        self.lineas = {}
        self.lineas['X'] = QLineF(QPointF(0,400),QPointF(800,400))
        self.lineas['Y'] = QLineF(QPointF(400,0),QPointF(400,800))
        self.inicializarPuntos()
        self.update()   

        #Timer que mueve la animación
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizarPuntos)
        self.timer.start(50)#Velocida del timer

    def paintEvent(self, a0:QPaintEvent) -> None:
        painter = QPainter(self)

        self.dibujarCuadricula(painter)
        self.dibujarEjes(painter)
        
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        #Dibujo del circulo
        painter.drawEllipse(QPointF(self.mainCircle[0],self.mainCircle[1]),self.mainCircle[2],self.mainCircle[3])

        self.dibujarCirculosRV(painter)
        self.dibujarLineas(painter)
        self.dibujarVertices(painter)
        self.dibujarPuntos(painter)

        #Dibujo de los datos obtenidos de SEN,COS,TAN,COT,SEC,CSC
        font = QFont()
        font.setPointSizeF(font.pointSizeF()*1.4)
        painter.setFont(font)

        colores = ((14, 110, 1),(212, 25, 0),(79, 10, 191),(205, 100, 209),(250, 128, 114),(9, 255, 0))
        if self.puntos['C'][2] <= 360 and self.puntos['C'][2] >= 270:
            valores = ('SEN = ' + str(np.round(self.lineas['sen'].length()/self.tamanio[0]*8,3)),'COS = ' + str(np.round(self.lineas['cos'].length()/self.tamanio[0]*8,3)),
            'TAN = ' + str(np.round(self.lineas['tan'].length()/self.tamanio[0]*8,3)),'COT = ' + str(np.round(self.lineas['cot'].length()/self.tamanio[0]*8,3)),
            'SEC = ' +str(np.round(self.lineas['sec'].length()/self.tamanio[0]*8,3)),'CSC = ' + str(np.round(self.lineas['csc'].length()/self.tamanio[0]*8,3)))
        elif self.puntos['C'][2] <= 270 and self.puntos['C'][2] >= 180:
            valores = ('SEN = ' + str(np.round(self.lineas['sen'].length()/self.tamanio[0]*8,3)),'COS = ' + str(np.round(self.lineas['cos'].length()/self.tamanio[0]*8*-1,3)),
            'TAN = ' + str(np.round(self.lineas['tan'].length()/self.tamanio[0]*8*-1,3)),'COT = ' + str(np.round(self.lineas['cot'].length()/self.tamanio[0]*8*-1,3)),
            'SEC = ' +str(np.round(self.lineas['sec'].length()/self.tamanio[0]*8*-1,3)),'CSC = ' + str(np.round(self.lineas['csc'].length()/self.tamanio[0]*8,3)))
        elif self.puntos['C'][2] <= 180 and self.puntos['C'][2] >= 90:
            valores = ('SEN = ' + str(np.round(self.lineas['sen'].length()/self.tamanio[0]*8*-1,3)),'COS = ' + str(np.round(self.lineas['cos'].length()/self.tamanio[0]*8*-1,3)),
            'TAN = ' + str(np.round(self.lineas['tan'].length()/self.tamanio[0]*8,3)),'COT = ' + str(np.round(self.lineas['cot'].length()/self.tamanio[0]*8,3)),
            'SEC = ' +str(np.round(self.lineas['sec'].length()/self.tamanio[0]*8*-1,3)),'CSC = ' + str(np.round(self.lineas['csc'].length()/self.tamanio[0]*8*-1,3)))
        elif self.puntos['C'][2] <= 90 and self.puntos['C'][2] >= 0:
            valores = ('SEN = ' + str(np.round(self.lineas['sen'].length()/self.tamanio[0]*8*-1,3)),'COS = ' + str(np.round(self.lineas['cos'].length()/self.tamanio[0]*8,3)),
            'TAN = ' + str(np.round(self.lineas['tan'].length()/self.tamanio[0]*8*-1,3)),'COT = ' + str(np.round(self.lineas['cot'].length()/self.tamanio[0]*8*-1,3)),
            'SEC = ' +str(np.round(self.lineas['sec'].length()/self.tamanio[0]*8,3)),'CSC = ' + str(np.round(self.lineas['csc'].length()/self.tamanio[0]*8*-1,3)))

        for i in range(len(colores)):
            cuadro = QRectF(100,180+(i*30),150,20)
            painter.setBrush(QBrush(QColor(qRgb(colores[i][0],colores[i][1],colores[i][2])), Qt.SolidPattern))
            painter.setPen(QPen(QColor(qRgb(colores[i][0],colores[i][1],colores[i][2])),2, Qt.SolidLine))
            painter.drawRect(cuadro)
            painter.setPen(QPen(QColor(qRgb(0,0,0)),2, Qt.SolidLine))
            painter.drawText(cuadro,valores[i])
        cuadro = QRectF(100,150,150,20)
        painter.setBrush(QBrush(QColor(qRgb(255, 132, 0)), Qt.SolidPattern))
        painter.setPen(QPen(QColor(qRgb(255, 132, 0)),2, Qt.SolidLine))
        painter.drawRect(cuadro)
        painter.setPen(QPen(QColor(qRgb(0,0,0)),2, Qt.SolidLine))
        painter.drawText(cuadro,'Angle = ' + str(np.round(self.lineas['h'].angle(),3)))

    #Dibujar lineas con su respectivo color
    def dibujarLineas(self,painter):

        painter.setPen(QPen(QColor(qRgb(14, 110, 1)),2, Qt.DotLine))
        painter.drawLine(self.lineas['i'])
        painter.setPen(QPen(QColor(qRgb(212, 25, 0)),2, Qt.DotLine))
        painter.drawLine(self.lineas['j'])
        painter.drawLine(self.lineas['k1'])

        painter.setPen(QPen(QColor(qRgb(0, 157, 255)), 3, Qt.SolidLine))
        painter.drawLine(self.lineas['h']) #Linea h

        painter.setPen(QPen(QColor(qRgb(212, 25, 0)), 3, Qt.SolidLine))      
        painter.drawLine(self.lineas['cos'])
       
        painter.setPen(QPen(QColor(qRgb(14, 110, 1)), 3, Qt.SolidLine))
        painter.drawLine(self.lineas['sen'])

        painter.setPen(QPen(QColor(qRgb(79, 10, 191)), 2, Qt.DotLine))
        painter.drawLine(self.lineas['h1'])

        painter.setPen(QPen(QColor(qRgb(79, 10, 191)), 3, Qt.SolidLine))
        painter.drawLine(self.lineas['tan'])
        
        painter.setPen(QPen(QColor(qRgb(205, 100, 209)), 2, Qt.DotLine))
        painter.drawLine(self.lineas['i1'])

        painter.setPen(QPen(QColor(qRgb(9, 255, 0)), 3, Qt.DotLine))
        painter.drawLine(self.lineas['j1'])

        painter.setPen(QPen(QColor(qRgb(9, 255, 0)), 5, Qt.DotLine))
        painter.drawLine(self.lineas['csc'])

        painter.setPen(QPen(QColor(qRgb(250, 128, 114)), 5, Qt.DotLine))
        painter.drawLine(self.lineas['sec'])

        painter.setPen(QPen(QColor(qRgb(205, 100, 209)), 5, Qt.DotLine))
        painter.drawLine(self.lineas['cot'])

        painter.setPen(QPen(QColor(qRgb(255, 132, 0)), 3, Qt.SolidLine))
        painter.drawArc(QRectF(self.puntos['A'][0]-self.pixel,self.puntos['A'][1]-self.pixel,round(self.tamanio[0]/20),round(self.tamanio[0]/20)),0,round(self.lineas['h'].angle()*16))
        
        #Lineas auxiliares que no son necesarias dibujar
        """ 
        try:
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(self.lineas['l'])
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(self.lineas['r'])
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(self.lineas['f1'])
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(self.lineas['m'])
        painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
        painter.drawLine(self.lineas['q'])
        except:
            pass """
        
    #Dibujar puntos con su respectivo color
    def dibujarPuntos(self,painter):
        painter.setPen(QPen(QColor(qRgb(0,0,0)), 1, Qt.SolidLine))
        painter.setBrush(QBrush(QColor(qRgb(255, 132, 0)), Qt.SolidPattern))
        self.dibujarPunto(painter,'C')

        painter.setBrush(QBrush(QColor(qRgb(212, 25, 0)), Qt.SolidPattern))
        self.dibujarPunto(painter,'I')

        painter.setBrush(QBrush(QColor(qRgb(14, 110, 1)), Qt.SolidPattern))
        self.dibujarPunto(painter,'K')
    
        painter.setBrush(QBrush(QColor(qRgb(79, 10, 191)), Qt.SolidPattern))
        self.dibujarPunto(painter,'L')
        self.dibujarPunto(painter,'O')
        self.dibujarPunto(painter,'S')

        painter.setBrush(QBrush(QColor(qRgb(205, 100, 209)), Qt.SolidPattern))
        self.dibujarPunto(painter,'M')
        self.dibujarPunto(painter,'R')
        self.dibujarPunto(painter,'T')

    def dibujarCirculosRV(self,painter):
        #Dibujar el circulo rojo y verde 
        painter.setBrush(QBrush())
        painter.setPen(QPen(QColor(qRgb(212, 25, 0)), 1.5, Qt.DotLine))
        painter.drawEllipse(QPointF(self.puntos['A'][0],self.puntos['A'][1]), self.obtenerDistanciaEntrePuntos('A','L'),self.obtenerDistanciaEntrePuntos('A','L'))
        painter.setPen(QPen(QColor(qRgb(9, 255, 0)), 1.5, Qt.DotLine))
        painter.drawEllipse(QPointF(self.puntos['A'][0],self.puntos['A'][1]), self.obtenerDistanciaEntrePuntos('A','M'),self.obtenerDistanciaEntrePuntos('A','M'))

    def dibujarVertices(self,painter):
        #Dibujar vertices del circulo y puntos estaticos
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        self.dibujarPunto(painter,'B')
        self.dibujarPunto(painter,'G')
        self.dibujarPunto(painter,'D')
        self.dibujarPunto(painter,'F')
        self.dibujarPunto(painter,'A')
        self.dibujarPunto(painter,'P')
        self.dibujarPunto(painter,'Q')
        
    def dibujarEjes(self,painter):
        #Dibujar ejes principales
        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        painter.drawLine(self.lineas['A-B'])
        painter.drawLine(self.lineas['A-G'])
        painter.drawLine(self.lineas['A-D'])
        painter.drawLine(self.lineas['A-F'])
        painter.drawLine(self.lineas['X'])
        painter.drawLine(self.lineas['Y'])

    def actualizarCirculo(self):
        #Coordenadas del circulo de acuerdo al tamanio actual configurado por el usuario
        self.mainCircle = [self.width/2,self.height/2,self.tamanio[0]/8,self.tamanio[1]/8]
        self.puntos['B'] = [self.mainCircle[0]+self.mainCircle[2],self.mainCircle[1]]
        self.puntos['G'] = [self.mainCircle[0],self.mainCircle[1]-self.mainCircle[3]]
        self.puntos['D'] = [self.mainCircle[0]-self.mainCircle[2],self.mainCircle[1]]
        self.puntos['F'] = [self.mainCircle[0],self.mainCircle[1]+self.mainCircle[3]]
        self.puntos['A'] = [self.mainCircle[0],self.mainCircle[1]]
        self.pixel  = (self.puntos['B'][0] - self.puntos['A'][0])/5
        self.puntos['P'] = [self.puntos['A'][0],self.puntos['A'][1]+self.pixel/4.5]
        self.puntos['Q'] = [self.puntos['A'][0]-self.pixel/4.807,self.puntos['A'][1]-self.pixel/60]

    #Funcion principal que se encarga de actualizar las coordenadas de todos los puntos y lineas
    def actualizarPuntos(self):
        self.actualizarCirculo()
        if self.timer.isActive(): #No mover la animacion pero si redimensionar los objetos cuando el timer esta detenido
            self.puntos['C'][2]-=1#Aumentar los grados del punto C

        self.puntos['C'][0],self.puntos['C'][1] = self.getPoint(self.puntos['C'][2],[self.puntos['A'][0],self.puntos['A'][1]],self.mainCircle[2])
        
        if(self.puntos['C'][2] == 0):
            self.puntos['C'][2] = 360
        self.puntos['I'][0],self.puntos['I'][1] = self.puntos['C'][0],self.puntos['A'][1]
        self.puntos['K'][0],self.puntos['K'][1] = self.puntos['A'][0],self.puntos['C'][1]

        self.lineas['h'] = self.obtenerLineaEntrePuntos('A','C')
        self.lineas['cos'] = self.obtenerLineaEntrePuntos('A','I')
        self.lineas['sen'] = self.obtenerLineaEntrePuntos('A','K')
        self.lineas['A-B'] = self.obtenerLineaEntrePuntos('A','B')
        self.lineas['A-D'] = self.obtenerLineaEntrePuntos('A','D')
        self.lineas['A-F'] = self.obtenerLineaEntrePuntos('A','F')
        self.lineas['A-G'] = self.obtenerLineaEntrePuntos('A','G')
        self.lineas['i'] = self.obtenerLineaEntrePuntos('I','C')
        self.lineas['j'] = self.obtenerLineaEntrePuntos('K','C')
        try:
            self.lineas['l'] = self.calcularPerpendicular()
            self.puntos['L'] = self.obtenerInterseccion('X','l')
            self.puntos['M'] = self.obtenerInterseccion('Y','l')
            self.lineas['h1'] = self.obtenerLineaEntrePuntos('L','C')
            self.lineas['i1'] = self.obtenerLineaEntrePuntos('M','C')
            self.lineas['r'] = QLineF(0,self.puntos['M'][1],800,self.puntos['M'][1])
            self.lineas['f1'] = QLineF(self.puntos['B'][0],0,self.puntos['B'][0],800)
            self.lineas['q'] = QLineF(self.puntos['Q'][0],0,self.puntos['Q'][0],800)
            self.lineas['n'] = QLineF(self.puntos['L'][0],0,self.puntos['L'][0],800)
            self.lineas['m'] = QLineF(0,self.puntos['P'][1],800,self.puntos['P'][1])
            self.puntos['R'] = self.obtenerInterseccion('q','r')
            self.puntos['O'] = self.obtenerInterseccion('m','n')
            self.lineas['csc'] = self.obtenerLineaEntrePuntos('R','Q')
            self.lineas['sec'] = self.obtenerLineaEntrePuntos('P','O')
            self.puntos['S'] = self.obtenerInterseccion('f1','h')
            self.lineas['tan'] = self.obtenerLineaEntrePuntos('S','B')
            self.lineas['g1'] = QLineF(0,self.puntos['G'][1],800,self.puntos['G'][1])
            self.puntos['T'] = self.obtenerInterseccion('g1','h')
            self.lineas['cot'] = self.obtenerLineaEntrePuntos('T','G')
            self.lineas['k1'] = self.obtenerLineaEntrePuntos('S','C')
            self.lineas['j1'] = self.obtenerLineaEntrePuntos('C','T')   
        except:
            pass

        self.update()

    #Inicializacion de los puntos y circulos del programa
    def inicializarPuntos(self):
        self.actualizarCirculo()
        #Punto C que inicia con 302 grados
        self.puntos['C'] = self.getPoint(302,[self.puntos['A'][0],self.puntos['A'][1]],self.mainCircle[2]/2)
        self.puntos['C'] = [self.puntos['C'][0],self.puntos['C'][1]]
        self.puntos['C'].append(302)
        self.puntos['I'] = [self.puntos['C'][0],self.puntos['A'][1],0]
        self.puntos['K'] = [self.puntos['A'][0],self.puntos['C'][1],0]
        self.puntos['L'] = [QPointF(0.0,0.0),QPointF(0.0,0.0)]
        self.puntos['M'] = [QPointF(0.0,0.0),QPointF(0.0,0.0)]

    #Funcion que devuelve coordenadas del punto donde intersectan dos lienas del diccionario
    def obtenerInterseccion(self,linea1,linea2):
        return [self.lineas[linea1].intersects(self.lineas[linea2])[1].x(),self.lineas[linea1].intersects(self.lineas[linea2])[1].y()]    

    #Calculos para calcular la perpendicular de la recta C-A
    def calcularPerpendicular(self):
        try:
            pendienteC = self.calcularPendiente('C','A')
            pendientePerpendicular = -1/(pendienteC)
            bPerpendicular = (self.puntos['C'][1]) - (pendientePerpendicular*self.puntos['C'][0])
            return QLineF(QPointF(0,bPerpendicular),QPointF(self.width,bPerpendicular+(pendientePerpendicular*self.width)))
        except:
            pass

    #Formula para calcular la pendiente de una recta
    def calcularPendiente(self,puntoA,puntoB):
        return ((self.puntos[puntoA][1])-self.puntos[puntoB][1]) / (self.puntos[puntoA][0]-self.puntos[puntoB][0])

    def getPoint(self,degrees,origin,radius): #Formula para obtener un punto en una circunferencia
        x = radius * np.cos(degrees*0.0174533) + origin[0]
        y = radius * np.sin(degrees*0.0174533) + origin[1]
        return [round(x),round(y)]

    #Obtener la linea entre dos puntos del diccionario
    def obtenerLineaEntrePuntos(self,puntoA,puntoB):
        return QLineF(self.puntos[puntoA][0],self.puntos[puntoA][1],self.puntos[puntoB][0],self.puntos[puntoB][1])
    
    #Obtener la distancia entre dos puntos del diccionario
    def obtenerDistanciaEntrePuntos(self,puntoA,puntoB):
        return np.sqrt((self.puntos[puntoA][0]-self.puntos[puntoB][0])**2 + (self.puntos[puntoA][1]-self.puntos[puntoB][1])**2)
    
    #Funcion para dibujar la cuadricula de fondo
    def dibujarCuadricula(self,painter):
        painter.setPen(QPen(Qt.lightGray, 1, Qt.SolidLine))
        #Calculo del tamanio que mide cada cuadrado del fondo
        self.pixel  = (self.puntos['B'][0] - self.puntos['A'][0])/5
        #Calculo de la cantidad de lineas que se deben dibujar
        self.cantidadLineas = self.width/self.pixel
        inicio = self.puntos['A']
        valor = [inicio[0],inicio[0]]   
        #Dibujar lineas desde el centro hacia los lados uqe son paralelas el eje x 
        for i in range(round(self.cantidadLineas)):
            painter.drawLine(QLineF(valor[0],0,valor[0],self.height))
            painter.drawLine(QLineF(valor[1],0,valor[1],self.height))
            valor[1]+=self.pixel
            valor[0]-=self.pixel

        valor = [inicio[1],inicio[1]]
        #Dibujar lineas desde el centro hacia los lados que son parlelas al eje y
        for i in range(round(self.cantidadLineas)):
            painter.drawLine(QLineF(0,valor[0],self.width,valor[0]))
            painter.drawLine(QLineF(0,valor[1],self.width,valor[1]))
            valor[1]+=self.pixel
            valor[0]-=self.pixel

    #Funcion que dibuja un punto del diccionario de puntos
    def dibujarPunto(self,painter,punto):
        painter.drawEllipse(QPointF(self.puntos[punto][0],self.puntos[punto][1]),self.tamanioVertices,self.tamanioVertices,)

    def keyPressEvent(self, e):
        #Hacer zoom in al circulo
        if e.key()==Qt.Key_Up:
            self.zoom('+')
        if e.key()==Qt.Key_Down:
        #Hacer zoom out al circulo
            self.zoom('-')
        if e.key()==Qt.Key_Space:
        #Pausar y reanudar la animación
            if(self.timer.isActive()):
                self.timer.stop()
            else:
                self.timer.start()

    #Aumentar el tamanio del circulo principal
    def zoom(self,type):
        if type == '+':
            self.tamanio[0]+=100
            self.tamanio[1]+=100
        if type == '-':
            if self.tamanio[0] != 100:
                self.tamanio[0]-=100
                self.tamanio[1]-=100

        self.actualizarPuntos()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
