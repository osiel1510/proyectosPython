from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import math
import copy

#Desarrolladores
#Osiel Alejandro Ordoñez Cruz
#José Antonio Cumpean Morales

class Nodo: #Clase del nodo, el cual corresponde a cada nodo y su valor
    def __init__(self, n,x = None, y = None):
        self.numeroEstado = n
        self.color = qRgb(0,0,0) 
        self.bgColor = qRgb(255,255,150)
        self.textColor = qRgb(0,0,0) 
        self.x = x
        self.y = y
        self.transiciones = {}

class Arbol: #Clase del arbol, el cual contiene todos los nodos
    def __init__(self,estados = []):
        self.estados = estados
    
    def obtenerEstadosDestino(self,estado): #Obtiene todos los nodos hijos de un nodo
        estadosDestino = []
        estado = self.estados[estado]

        for i in list(estado.transiciones.keys()): 
            estadosDestino.append(int(i))
        
        return estadosDestino

class DrawWidget(QWidget):  #Clase para dibujar los elementos gráficos
    def __init__(self, parent=None,boton=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 800) 
        self.automata = Arbol()
        self.boton = boton #Boton de correr BFS
        self.accion = None #Accion actual que se ejecuta
        self.estadoSeleccionado = None #Nodo que ha sido seleccionado por el cursor
        self.representacion = 0 #Tipo de representación seleccionada
        self.queue = [] #Cola del BFS
        self.parents = [] #Lista de nodos y sus parents
        self.visited = [] #Lista de nodos y si están visitados o no
        self.timer = QTimer(self) #Timer que controla la animación
        self.hijoVisitado = -1 #Hijo que está siendo visitado en el momento de la ejecución
        self.numeroHijoVisitado = -1 #Número de nodo hijo del nodo actual de la cola en el momento de la ejecución

        for i in range(8): #inicializar parents y visited
            self.visited.append(False)
            self.parents.append(-1)

        self.timer.timeout.connect(self.animarBFS) #Ligando el timer con el metodo de animacion

    def paintEvent(self, event): #Metodo que se encarga de dibujar los elementos graficos
        if self.representacion == 0: #Representacion logica
            data = self.automata.estados
            if len(data) > 0:
                painter = QPainter()
                painter.begin(self)
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                
                for edge in data: 
                    def dibujarTransicion(linea,valor=None,especial=False): #Funcion para dibujar las lineas y flechas
                        line = copy.deepcopy(linea)
                        line.setLength(line.length() - 28) #Reducir la linea para que se muestre la flecha
                        painter.drawLine(line)
                        arrowhead_size = 10

                        angle = math.atan2(line.p2().y() - line.p1().y(), line.p2().x() - line.p1().x()) #Obtencion del angulo de la flecha
                        p1 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle - math.pi / 6)),
                                    int(line.y2() - arrowhead_size * math.sin(angle - math.pi / 6)))
                        
                        p2 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle + math.pi / 6)),
                                    int(line.y2() - arrowhead_size * math.sin(angle + math.pi / 6)))
                        #Puntos de cada punta de la flecha
                        painter.drawLine(QLineF(line.x2(), line.y2(), p1.x(), p1.y()))
                        painter.drawLine(QLineF(line.x2(), line.y2(), p2.x(), p2.y()))

                    for numeroEstado in edge.transiciones.keys():
                        #Seccion de dibujado de transiciones
                        
                        estadoDestino = self.automata.estados[int(numeroEstado)]

                        if len(self.queue) > 0: #Dibujar la linea del nodo qeu se está visitando
                            if (edge.numeroEstado == self.queue[0] and int(numeroEstado) == self.hijoVisitado):
                                painter.setPen(QPen(QColor(qRgb(255,0,0)),4, Qt.SolidLine))
                            elif (self.parents[int(numeroEstado)] == edge.numeroEstado): #Dibujar la linea de los nodos ya visitados
                                painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine))
                            else: #linea normal
                                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                        else:
                            if (self.parents[int(numeroEstado)] == edge.numeroEstado):
                                painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine)) #Linea de los nodos ya visitados
                            else:
                                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine)) #Linea normal

                        if str(edge.numeroEstado) in list(self.automata.estados[int(numeroEstado)].transiciones.keys()): #Dibujado de lineas cuando ambas lineas comparten los mismos estados
                            distanciax = 0
                            if edge.x > estadoDestino.x: #Dibujar verticalmente
                                distanciax = edge.x - estadoDestino.x
                            else:
                                distanciax = estadoDestino.x - edge.x
                            
                            distanciay = 0
                            if edge.y > estadoDestino.y: #Dibujar horizontalmente
                                distanciay = edge.y - estadoDestino.y
                            else:
                                #Dibujar verticalmente
                                distanciay = estadoDestino.y - edge.y

                            if distanciax > 100:
                                #Dibujado de lineas en base a cual estado es mayor, para asi saber si la linea ira en la parte de arriba o en la de abajo
                                if edge.numeroEstado < int(numeroEstado):
                                    dibujarTransicion(QLineF(edge.x,edge.y+20,estadoDestino.x,estadoDestino.y+20),edge.transiciones[numeroEstado],True)
                                else:
                                    dibujarTransicion(QLineF(edge.x,edge.y-20,estadoDestino.x,estadoDestino.y-20),edge.transiciones[numeroEstado])
                            elif (distanciax <= 100 and distanciay > 50):
                                if edge.numeroEstado < int(numeroEstado):
                                    dibujarTransicion(QLineF(edge.x+20,edge.y,estadoDestino.x+20,estadoDestino.y),edge.transiciones[numeroEstado],True)
                                else:
                                    dibujarTransicion(QLineF(edge.x-20,edge.y,estadoDestino.x-20,estadoDestino.y),edge.transiciones[numeroEstado])
                            else:
                                if edge.numeroEstado < int(numeroEstado):
                                    dibujarTransicion(QLineF(edge.x,edge.y+20,estadoDestino.x,estadoDestino.y+20),edge.transiciones[numeroEstado],True)
                                else:
                                    dibujarTransicion(QLineF(edge.x,edge.y-20,estadoDestino.x,estadoDestino.y-20),edge.transiciones[numeroEstado])
                                
                        else:
                            #Dibujado de lineas normales
                            dibujarTransicion(QLineF(edge.x,edge.y,estadoDestino.x,estadoDestino.y),edge.transiciones[numeroEstado])
                    
                font = QFont()
                font.setPointSize(16)
                painter.setFont(font)

                def dibujarEstado(estado): #Dibujado de nodos
                    painter.setBrush(QBrush(QColor(estado.bgColor), Qt.SolidPattern))
                    painter.setPen(QPen(QColor(estado.color),2, Qt.SolidLine))
                    vertex = {}
                    vertex['x'] = estado.x #Posiciones
                    vertex['y'] = estado.y
                    radio = 30 #Radio del estado

                    #Dibujado de nodos normales
                    if (len(self.queue) > 0):
                        if(estado.numeroEstado == self.queue[0]):
                            painter.setPen(QPen(QColor(estado.color),4, Qt.SolidLine))
                    
                    painter.drawEllipse(vertex['x']-radio, vertex['y']-radio,radio*2, radio*2) #Dibujado de la elipse
                    painter.setPen(QPen(QColor(estado.color),2, Qt.SolidLine))
                    
                    painter.setPen(QPen(QColor(estado.textColor),3, Qt.SolidLine))
                    if(len(str(estado.numeroEstado))>1):
                        painter.drawText(vertex['x']-11, vertex['y'] + 5, str(estado.numeroEstado)) #Dibujado del texto
                    else:
                        painter.drawText(vertex['x']-5, vertex['y'] + 5, str(estado.numeroEstado)) 

                for i in data:
                    dibujarEstado(i)

                painter.end()
        
        elif self.representacion == 1: #Representacion lista de adjacencia
            initX = 100
            initY = 100 
            #Posiciones inciiaels

            for i in range(8): #Dibujar los numeros de nodo desde arriba hacia abajo y su caja lateral
                painter = QPainter()
                painter.begin(self)
                painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine))
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(QPointF(initX,initY),str(i))
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                if len(self.queue)>0:
                    if self.queue[0] == i:
                        painter.drawEllipse(QPointF(initX+5,initY-5),20,20) #Dibujado de una elipse para indicar el elemento actual de la cola que está siendo ejecutado
                painter.drawRect(QRect(initX+40,initY-20,40,40))
                initY+=40

            
            data = self.automata.estados

            initX = 210
            initY = 100
            for edge in data: 
                if (len(list(edge.transiciones.keys())) < 1):
                    painter.drawLine(QPoint(142,100+(40*edge.numeroEstado)-20),QPoint(180,100+(40*edge.numeroEstado)+18)) #Marca en caso de que no tenga ningun nodo hijo
                else:
                    cantidad = len(list(edge.transiciones.keys()))
                    contador=1

                    for numeroEstado in edge.transiciones.keys():
                        initY= 100 + (40*edge.numeroEstado)
                        
                        painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine)) #Dibujado del nodo hijo
                        painter.drawText(QPointF(initX,initY+5),str(numeroEstado))
                        line = QLine(initX-30,initY,initX-10,initY)
                        
                        painter.setPen(QPen(QColor(qRgb(0,0,0)),2, Qt.SolidLine))
                        painter.drawRect(QRect(initX-5,initY-20,20,40)) #Dibujado de la primera caja

                        initX+=25
                        painter.drawRect(QRect(initX-5,initY-20,20,40))
                        
                        painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                        painter.drawText(QPointF(initX,initY+5),'1') #Dibujado del 1 y la segunda caja

                        initX+=25
                        painter.setPen(QPen(QColor(qRgb(0,0,0)),2, Qt.SolidLine))
                        painter.drawRect(QRect(initX-5,initY-20,20,40)) #Dibujado de la caja final con flecha

                        if contador == cantidad:
                            painter.drawLine(initX-5,initY-20,initX-4+20,initY+20)

                        if len(self.queue) > 0: #Dibujado de caja roja para resaltar que se está visitando un nodo
                            if(int(numeroEstado) == self.hijoVisitado and self.queue[0] == edge.numeroEstado):
                                painter.setPen(QPen(QColor(qRgb(255,0,0)),4, Qt.SolidLine))
                                painter.drawRect(QRect(initX-58,initY-22,75,45))
                            
                        painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                        contador+=1

                        initX+=40

                        painter.drawLine(line)
                        arrowhead_size = 10 #Dibujado de las flechas

                        angle = math.atan2(line.p2().y() - line.p1().y(), line.p2().x() - line.p1().x()) #Obtencion del angulo de la flecha
                        p1 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle - math.pi / 6)),
                                    int(line.y2() - arrowhead_size * math.sin(angle - math.pi / 6)))
                        
                        p2 = QPointF(int(line.x2() - arrowhead_size * math.cos(angle + math.pi / 6)),
                                    int(line.y2() - arrowhead_size * math.sin(angle + math.pi / 6)))
                        #Puntos de cada punta de la flecha  
                        painter.drawLine(QLineF(line.x2(), line.y2(), p1.x(), p1.y()))
                        painter.drawLine(QLineF(line.x2(), line.y2(), p2.x(), p2.y()))

                    initY+=40
                    initX=210

        elif self.representacion == 2: #Representacion matriz de adjacencia
            initX = 100
            initY = 110
            initYLine = 80

            for i in range(8): 
                #Dibujado de las lineas horizontales y los numeros en vertical
                painter = QPainter()
                painter.begin(self)
                painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine))
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(QPointF(initX,initY),str(i))
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                painter.drawLine(130,initYLine+5,initX+(40*9),initYLine+5)
                if len(self.queue)>0:
                    if self.queue[0] == i:
                        painter.drawEllipse(QPointF(initX+5,initY-5),20,20) #Dibujar una elipse para indicar cual elemento de la cola está siendo procesado ahora
                initY+=40
                initYLine+=40
            painter.drawLine(130,initY-30,initX+(40*9),initY-30)

            
            initX = 143
            initY = 80
            initXLine = 128

            for i in range(8):#Dibujado de las lineas verticales y los numeros en horizontal
                painter = QPainter()
                painter.begin(self)
                painter.setPen(QPen(QColor(qRgb(0,0,255)),3, Qt.SolidLine))
                font = QFont()
                font.setPointSize(12)
                painter.setFont(font)
                painter.drawText(QPointF(initX,initY),str(i))
                painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                painter.drawLine(initXLine,initY,initXLine,initY+(40*8))
                initXLine+=42
                initX+=42
            
            painter.drawLine(initXLine,initY,initXLine,initY+(40*8))

            painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
            data = self.automata.estados

            initX = 143
            initY = 100
            
            for edge in data: #Dibujado de los 1 que indican los nodos hijos de los elementos
                for numeroEstado in edge.transiciones.keys():
                    initY= 100 + (40*edge.numeroEstado)
                    
                    painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                    painter.drawText(QPointF(initX+(42*int(numeroEstado)),initY+5),'1')
                    line = QLine(initX-30,initY,initX-10,initY)

                    if len(self.queue) > 0:
                        if(int(numeroEstado) == self.hijoVisitado and self.queue[0] == edge.numeroEstado): #Dibujado para indicar que se esta visitando un elemento
                            painter.setPen(QPen(QColor(qRgb(255,0,0)),4, Qt.SolidLine))
                            painter.drawRect(QRect(-15+ initX+(42*int(numeroEstado)),initY-15,45,40))

                initY+=42

    def startBFS(self,nodoInicial): #Metodo para iniciar el proceso de BFS
        self.numeroHijoVisitado = -1
        self.queue = [nodoInicial]
        self.timer.stop()
        self.boton.setEnabled(False) #Deshabilitamos el boton para prevenir una doble animacion
        
        for i in range(8):
            self.visited[i] = False
            self.parents[i] = -1
        
        self.visited[self.queue[0]] = True
            
        self.timer.start(1000)

    def animarBFS(self):
        # print("Cola: ",self.queue)
        # print("Visitados: ", self.visited)
        # print("Parents: ", self.parents)
        # print("Hijo visitado: ", self.hijoVisitado)

        #Obtenemos la lista de los estados del nodo que esta al principio de la cola
        estados = self.automata.obtenerEstadosDestino(self.queue[0])
        # print("Estados del nodo actual: ",estados)
        try:
            #Vamos visitando los hijos de dicho nodo
            self.numeroHijoVisitado+=1
            #Obtenemos el numero de hijo en cuestion
            self.hijoVisitado = estados[self.numeroHijoVisitado]
            
            #En caso de que dicho nodo ya haya sido visitado
            if self.visited[self.hijoVisitado] == True:
                pass
            else:
                #En caso de que el nodo no haya sido visitado
                #Lo agregamos a la cola
                self.queue.append(self.hijoVisitado)
                #Marcamos al hijo como visitado
                self.visited[self.hijoVisitado] = True
                self.parents[self.hijoVisitado] = self.queue[0]
            
            self.update()
        
        #La excepcion ocurre cuando no existen mas nodos hijos que visitar
        except:
            #Eliminamos un elemento de la cola
            del self.queue[0]
            self.numeroHijoVisitado = -1
            if len(self.queue) == 0:
                self.timer.stop()
                self.boton.setEnabled(True) #Habilitamos el boton nuevamente
                self.update()

    def mousePressEvent(self, event): #Listener de acciones del mouse
        if self.representacion == 0:
            if event.button() == Qt.LeftButton:
                if self.accion == 'estados': #Colocar estados
                    self.automata.estados.append(Nodo(len(self.automata.estados),event.x(),event.y()))
                    self.update()

                if self.accion == 'transiciones': #Hacer transiciones
                    if len(self.automata.estados) >0:
                        if self.estadoSeleccionado == None: #Seleccionar el primer estado
                            self.estadoSeleccionado = self.obtenerEstadoCercano(Nodo(-1,event.x(),event.y()))
                        else: #Seleccionar el segundo estado y concluir transicion
                            estadoDestino = self.obtenerEstadoCercano(Nodo(-1,event.x(),event.y()))
                            if estadoDestino != None:
                                if str(estadoDestino.numeroEstado) in self.estadoSeleccionado.transiciones.keys():        #En caso de que las transiciones ya existan
                                    pass
                                else:
                                    if estadoDestino == self.estadoSeleccionado:
                                        pass
                                    else:
                                        #Transicion normal
                                        text = '1'
                                        valores = list(set(text.split()))
                                        linea = QLineF(self.estadoSeleccionado.x,self.estadoSeleccionado.y, estadoDestino.x, estadoDestino.y)
                                        self.estadoSeleccionado.transiciones[str(estadoDestino.numeroEstado)] = valores

                                self.update()
                                self.estadoSeleccionado = None
                            else:
                                pass

                if self.accion == 'moverEstados': 
                    #Mover estado en base a la posicion del mouse
                    if len(self.automata.estados) > 0:
                        if self.estadoSeleccionado == None:
                            self.estadoSeleccionado = self.obtenerEstadoCercano(Nodo(-1,event.x(),event.y()))
                            if self.estadoSeleccionado != None:
                                self.estadoSeleccionado.x = event.x()
                                self.estadoSeleccionado.y = event.y()
                                self.estadoSeleccionado.bgColor = qRgb(100,200,255)
                                self.update()

                #Eliminar transiciones
                if self.accion == 'eliminarTransiciones':
                    estadoSeleccionado = self.obtenerEstadoCercano(Nodo(-1,event.x(),event.y()))
                    if estadoSeleccionado != None:
                        estadoSeleccionado.transicionPropia = []
                        self.update()

                    else:
                        for estado in self.automata.estados:
                            estadoDestinoSeleccionado = None
                            for numeroEstado in estado.transiciones.keys():
                                estadoDestino = self.automata.estados[int(numeroEstado)]

                                if str(estado.numeroEstado) in list(self.automata.estados[int(numeroEstado)].transiciones.keys()):
                                    distanciax = 0
                                    if estado.x > estadoDestino.x:
                                        distanciax = estado.x - estadoDestino.x
                                    else:
                                        distanciax = estadoDestino.x - estado.x
                                    
                                    distanciay = 0
                                    if estado.y > estadoDestino.y:
                                        distanciay = estado.y - estadoDestino.y
                                    else:
                                        distanciay = estadoDestino.y - estado.y
                                    
                                    line = None

                                    if distanciax > 100:
                                        if estado.numeroEstado < int(numeroEstado):
                                            line = QLineF(estado.x,estado.y+20,estadoDestino.x,estadoDestino.y+20)
                                        else:
                                            line = QLineF(estado.x,estado.y-20,estadoDestino.x,estadoDestino.y-20)
                                    elif (distanciax <= 100 and distanciay > 50):
                                        if estado.numeroEstado < int(numeroEstado):
                                            line = QLineF(estado.x+20,estado.y,estadoDestino.x+20,estadoDestino.y)
                                        else:
                                            line = QLineF(estado.x-20,estado.y,estadoDestino.x-20,estadoDestino.y)
                                    else:
                                        if estado.numeroEstado < int(numeroEstado):
                                            line = QLineF(estado.x,estado.y+20,estadoDestino.x,estadoDestino.y+20)
                                        else:
                                            line = QLineF(estado.x,estado.y-20,estadoDestino.x,estadoDestino.y-20)
                                        
                                else:
                                    line = QLineF(estado.x,estado.y,estadoDestino.x,estadoDestino.y)
                                
                                linea = copy.deepcopy(line)

                                contador = 0
                                while linea.length()>2:
                                    contador+=1
                                    if contador == 10000:
                                        break
                                    distancia = math.sqrt((event.x() - linea.p2().x())**2 + (event.y() - linea.p2().y())**2)
                                    if distancia < 10:
                                        estadoDestinoSeleccionado = numeroEstado
                                        break

                                    linea.setLength(linea.length()-5)
                            
                            if estadoDestinoSeleccionado != None:
                                del estado.transiciones[str(estadoDestinoSeleccionado)]
                                self.update()
                                break

    def mouseMoveEvent(self, event): #Mover estados con el click presionado
        if self.representacion == 0:
            if self.accion == 'moverEstados':
                if self.estadoSeleccionado != None:
                    self.estadoSeleccionado.x = event.x()
                    self.estadoSeleccionado.y = event.y()
                    self.update()

    def mouseReleaseEvent(self, event): #Liberar estado, restaurando su color original
        if self.representacion == 0:
            if self.accion == 'moverEstados':
                if self.estadoSeleccionado != None:
                    self.estadoSeleccionado.x = event.x()
                    self.estadoSeleccionado.y = event.y()
                    self.estadoSeleccionado.bgColor = qRgb(255,255,150)
                    self.estadoSeleccionado = None
                    self.update()
    
    def obtenerEstadoCercano(self,punto): #Funcion para obtener el estado mas cercano a un punto
        distanciaCercana = math.inf
        estadoCercano = None
        
        for estado in self.automata.estados:
            distancia = math.sqrt((estado.x - punto.x)**2 + (estado.y - punto.y)**2)

            if distancia < distanciaCercana:
                distanciaCercana = distancia
                estadoCercano = estado
        
        if distanciaCercana <=29:    
            return estadoCercano

class MainWindow(QWidget): #Clase principal
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        #Tamaño máximo de la ventana
        self.setFixedSize(1280,800)

        #Diseño de toda la interfaz
        self.mainLayout = QHBoxLayout()
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()
        self.representationLayout = QVBoxLayout()
        self.btnLogical = QRadioButton("Logical Representation")
        self.btnAdjacencyList = QRadioButton("Adjacency List Representation")
        self.btnAdjacencyMatrix = QRadioButton("Adjacency Matrix Representation")

        self.botonesRepresentation = [
            self.btnLogical,
            self.btnAdjacencyList,
            self.btnAdjacencyMatrix
        ]

        self.btnLogical.clicked.connect(self.activarLogical)
        self.btnAdjacencyList.clicked.connect(self.activarAdjacencyList)
        self.btnAdjacencyMatrix.clicked.connect(self.activarAdjacencyMatrix)

        self.btnLogical.setChecked(True)

        for i in self.botonesRepresentation:
            self.representationLayout.addWidget(i)
        
        self.label = QLabel("Set start vertex")
        
        self.rightLayout.addWidget(self.label)
        
        
        self.hRunLayout = QHBoxLayout()
        self.btnProbar = QPushButton("Run BFS")
        
        self.editTextInitValue = QLineEdit()
        self.editTextInitValue.setMaximumHeight(20)

        self.hRunLayout.addWidget(self.editTextInitValue)
        self.hRunLayout.addWidget(self.btnProbar)
        
        self.btnProbar.clicked.connect(self.ejecutarBFS)
        self.rightLayout.addLayout(self.hRunLayout)
        self.table = QTableWidget()
        self.rightLayout.addWidget(self.table)
        self.table.setColumnCount(2)
        self.table.setRowCount(8)
        self.table.setHorizontalHeaderLabels(['Parent', 'Visited'])

        #Creacion de la tabla de prueba
        for row in range(self.table.rowCount()):
            entrada_item = QTableWidgetItem('')
            self.table.setItem(row, 0, entrada_item)
            
            aprobacion_item = QTableWidgetItem('')
            self.table.setItem(row, 1, aprobacion_item)

        header_labels = [str(i) for i in range(8)]
        self.table.setVerticalHeaderLabels(header_labels)
        self.table.setMaximumHeight(270)
        self.table.show()
        self.label.setMaximumHeight(20)

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)

        self.inputLayout = QHBoxLayout()
        self.cadenaLayout = QHBoxLayout()

        #Todos los botones
        self.btnTransiciones = QPushButton("Transiciones")
        self.btnMoverEstado = QPushButton("Mover estado")
        self.btnEliminarTransicion = QPushButton("Eliminar transiciones")

        self.btnTransiciones.clicked.connect(self.accionTransiciones)
        self.btnMoverEstado.clicked.connect(self.accionMoverEstado)
        self.btnEliminarTransicion.clicked.connect(self.accionEliminarTransicion)

        self.botones = [
            self.btnMoverEstado,
            self.btnTransiciones,
            self.btnEliminarTransicion
        ]

        self.drawWidget = DrawWidget(boton=self.btnProbar)
        self.drawWidget.setStyleSheet("background-color: #d3d3d3;")  
        self.setStyleSheet("background-color: #d3d3d3;") 

        self.inputLayout.addLayout(self.representationLayout)

        #hacer que los botones puedan mantenerse presionados
        for i in self.botones:
            self.inputLayout.addWidget(i)
            i.setCheckable(True)
        
        self.leftLayout.addLayout(self.inputLayout)
        self.leftLayout.addWidget(self.drawWidget)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle("PYFLAP")

        initX = 100
        initY = 500

        for i in range(8):
            self.drawWidget.automata.estados.append(Nodo(i,initX,initY))
            initX+=80

        self.labelQueue = QLabel()
        self.labelQueue.setMaximumHeight(40)
        self.rightLayout.addWidget(self.labelQueue)
        self.drawWidget.update()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.actualizarDatos)
        self.timer.start(10)

        self.rightLayout.setAlignment(Qt.AlignTop)

    def actualizarDatos(self):
        #Mantener actualizados los datos de la interfaz principal de acuerdo a los elementos de la clase drawWidgets.
        for fila in range(self.table.rowCount()): #Actualizar la tabla de parents y visiteds
            if (self.drawWidget.parents[fila] == -1):
                item1 = QTableWidgetItem('')
            else:
                item1 = QTableWidgetItem(str(self.drawWidget.parents[fila]))
            item = QTableWidgetItem(str(self.drawWidget.visited[fila]))
            self.table.setItem(fila, 0, item1)
            self.table.setItem(fila, 1, item)

        self.labelQueue.setText("BFS Queue\n\n")
        for i in self.drawWidget.queue:
            self.labelQueue.setText(self.labelQueue.text() + " " + str(i))


    #Funcion para ejecutar el BFS
    def ejecutarBFS(self):
        try:    
            self.drawWidget.startBFS(int(self.editTextInitValue.text()))
        except:
            pass

    #Funciones para cada boton
    def botonPresionado(self,numero):
        for i in self.botones:
            i.setChecked(False)

        self.botones[numero].setChecked(True)
        self.drawWidget.estadoSeleccionado = None
        self.update()


    #Botone spara cambiar de representacion
    def botonPresionadoRepresentacion(self,numero):
        for i in self.botonesRepresentation:
            i.setChecked(False)

        self.botonesRepresentation[numero].setChecked(True)
        self.drawWidget.estadoSeleccionado = None

        #Habilitar o deshabilitar los botones de edicion de arbol dependiendo de la representacion
        if numero == 0:
            for i in self.botones:
                i.setVisible(True)
        else:
            for i in self.botones:
                i.setVisible(False)

        self.drawWidget.representacion = numero
        self.drawWidget.update()

    #Cambiar de representacion
    def activarLogical(self):
        self.botonPresionadoRepresentacion(0)
    #Cambiar de representacion
    def activarAdjacencyList(self):
        self.botonPresionadoRepresentacion(1)
    
    #Cambiar de representacion
    def activarAdjacencyMatrix(self):        
        self.botonPresionadoRepresentacion(2)

    #Mover un nodo
    def accionMoverEstado(self):
        self.botonPresionado(0)
        self.drawWidget.accion = 'moverEstados'

    #Colocar transicones de hijo a un nodo
    def accionTransiciones(self):
        self.botonPresionado(1)
        self.drawWidget.accion = 'transiciones'

    #Borrar la relacion de hijo de un nodo
    def accionEliminarTransicion(self):
        self.botonPresionado(2)
        self.drawWidget.accion = 'eliminarTransiciones'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())