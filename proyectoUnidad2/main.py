from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import math
import copy

class Estado: #Clase de estado, la cual contiene su posicion y transiciones hacia otros estados
    def __init__(self, n,x = None, y = None):
        self.numeroEstado = n
        self.color = qRgb(0,0,0) 
        self.bgColor = qRgb(255,255,150)
        self.textColor = qRgb(0,0,0) 
        self.x = x
        self.y = y
        self.transiciones = {}
        self.transicionPropia = []

class Automata: #Clase del automata, el cual contiene dtodos los estados, estados finales y el inicial
    def __init__(self,estadoInicial = None,estadoFinal = [],entradas = [],estados = []):
        self.estadoInicial = estadoInicial
        self.estadoFinal = estadoFinal
        self.estados = estados

    def obtenerLenguaje(self): #Método para obtener todas las letras que se utilizan en el automata
        lenguaje = []
        for i in self.estados:
            for j in i.transiciones.values(): #Esto se logra mediante los valores de las transiciones
                for k in j:
                    lenguaje.append(k)
            for j in i.transicionPropia:
                lenguaje.append(j)


        return list(set(lenguaje))
    
    def obtenerEstadosDestino(self,estado,valor): #Obtener todos los de transicion "valor" del estado "estado"
        estadosDestino = []
        estado = self.estados[estado]

        for i in list(estado.transiciones.keys()): #Verificar si el valor se encuentra en las transiciones del estado
            if valor in estado.transiciones[i]:
                estadosDestino.append(int(i))

        if valor in estado.transicionPropia:
            estadosDestino.append(estado.numeroEstado)
        
        return estadosDestino

    def probarCadena(self,cadena): #Funcion principal para probar el automata con una cadena detexto
        try:
            transitionTable = [] #Tabla de transiciones

            dict = {} #Diccionario de las transiciones
            epsilonColumn = None  #Columna epsilon

            for indice,letra in enumerate(self.obtenerLenguaje()):  #Generacion del diccionario de transiciones
                if letra == 'λ':
                    epsilonColumn = indice
                dict[letra] = indice

            for i in self.estados: #Crecion del arreglo transition table
                transitionTable.append({})

            for indice,estado in enumerate(transitionTable): #Llenado del transition table
                for i in list(dict.keys()):
                    estado[i] = self.obtenerEstadosDestino(indice,i)
                if epsilonColumn == None:
                    estado['λ'] = []
            
            if epsilonColumn == None: #Registro de la columna epsilon
                epsilonColumn = len(list(dict.values()))

            acceptTable = [] #Creacion y llendo de la tabla de de estados aceptados.
            for i in self.estadoFinal:
                acceptTable.append(i.numeroEstado)

            def epsilon_closure(state, visited=None): 
                if visited is None:
                    visited = set()
                visited.add(state)
                if 'ε' in transitionTable[state]:
                    for next_state in transitionTable[state]['ε']:
                        if next_state not in visited:
                            epsilon_closure(next_state, visited)
                return visited

            def simulate_nfa(input_string):
                current_states = epsilon_closure(0)
                for ch in input_string:
                    symbol = ch
                    new_states = set()
                    for state in current_states:
                        if symbol in transitionTable[state]:
                            for next_state in transitionTable[state][symbol]:
                                new_states.update(epsilon_closure(next_state))
                    current_states = new_states
                return any(state in acceptTable for state in current_states)

            return simulate_nfa(cadena)
        except:
            return False        
            
    def eliminarEstado(self,estado): #Fucion para eliminar un estado y actualizar la lista de estados

        for i in range(estado,len(self.estados)):
            self.estados[i].numeroEstado-=1

        del(self.estados[estado])

        self.actualizarTransicionesEliminarEstado(estado) #Actualizar las transiciones
        

    def actualizarTransicionesEliminarEstado(self,estado): #Funcion para actualizar las transciones en caso de que se tenga que borrar un estado
        for i in self.estados:
            if str(estado) in i.transiciones.keys():
                del i.transiciones[str(estado)] #Eliminacion de transiciones del estado liminado

        for i in self.estados: 
            llavesTransicion = list(i.transiciones.keys())
            
            valoresTransicion = list(i.transiciones.values())
            nuevasTransiciones = {}
            
            for j in range(len(llavesTransicion)):
                if int(llavesTransicion[j]) > estado: #Actualiacion de las transiciones cuando se borra un estado
                    nuevasTransiciones[str(int(llavesTransicion[j])-1)] = valoresTransicion[j]
                else:
                    nuevasTransiciones[llavesTransicion[j]] = valoresTransicion[j]
                
            i.transiciones = nuevasTransiciones

class DrawWidget(QWidget): 
    def __init__(self, parent=None,botones=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 800) 
        self.automata = Automata()
        self.botones = botones 
        self.accion = None #Accion actual que se ejecuta
        self.estadoSeleccionado = None #Estado que ha sido seleccionado por el cursor

    def paintEvent(self, event): 
        data = self.automata.estados
        if len(data) > 0:
            painter = QPainter()
            painter.begin(self)
            painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
            
            for edge in data: 
                def dibujarTransicion(linea,valor=None,especial=False): #Funcion para dibujar transicoines
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

                    if valor != None:
                        if especial == False:
                            #Seccion para dibujar las letras de las transiciones

                            font = QFont('Arial', 10)
                            painter.setFont(font)
                            
                            # Calcula el angulo
                            angle = linea.angle()

                            if linea.x1() > linea.x2(): #En caso de que la orientación de la línea sea al revés
                                angle = 180 - angle

                            # Obtener el punto medio de la flecha
                            mid_point = linea.pointAt(0.5)

                            # Hacer un guardado del painter para alterarlo ahora y restaurarlo despues
                            painter.save()

                            painter.translate(mid_point)
                            painter.rotate(-angle)

                            # Calcula la altura total de las letras
                            total_height = len(valor) * (painter.fontMetrics().height()+15)

                            # Dibuja las letras
                            y = -total_height / 2
                            for letter in valor:
                                rect = painter.fontMetrics().boundingRect(letter)
                                x = -rect.width() / 2
                                painter.drawText(QPointF(x,y),letter)
                                y += rect.height()
                            
                            painter.restore() #Resturar el painter
                        else:
                                #En caso de que las letras tengan que dibujarse hacia abajo en vez de hacia arriba

                                # Configura la fuente
                                font = QFont('Arial', 10)
                                painter.setFont(font)

                                # Calcula el angulo
                                angle = linea.angle()

                                if linea.x1() > linea.x2(): #En caso de que los puntos estén invertidos
                                    angle = 180 - angle

                                # Encuentra el punto medio de la línea
                                mid_point = linea.pointAt(0.5)

                                # Guarda el estado actual del QPainter
                                painter.save()

                                # Ajustar el ángulo y la posición del QPainter
                                painter.translate(mid_point)
                                painter.rotate(-angle)

                                # Calcula la altura total de las letras
                                total_height = len(valor) * (painter.fontMetrics().height()-15)

                                y = -total_height / 2
                                for letter in valor:
                                    rect = painter.fontMetrics().boundingRect(letter)
                                    x = -rect.width() / 2
                                    y += rect.height() 
                                    painter.drawText(QPointF(x, y), letter)
                                
                                painter.restore() #Restaurar el estado del painter

                for numeroEstado in edge.transiciones.keys():
                    #Seccion de dibujado de transiciones
                    
                    estadoDestino = self.automata.estados[int(numeroEstado)]

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
                        #Dibujado de transiciones normales
                        dibujarTransicion(QLineF(edge.x,edge.y,estadoDestino.x,estadoDestino.y),edge.transiciones[numeroEstado])
                    

                if edge.transicionPropia != []:
                    #Dibujado de transiciones que llevan a un mismo estado, esto mediante una elipse
                    painter.drawEllipse(edge.x+20, edge.y, -40, -60)
                    
                    font = QFont('Arial', 10)
                    painter.setFont(font)
                    espacio = 0
                    for i in edge.transicionPropia:
                        painter.drawText(QPointF(edge.x-5,edge.y-70+espacio), i)
                        espacio-=painter.fontMetrics().height()
                
            font = QFont()
            font.setPointSize(16)
            painter.setFont(font)

            def dibujarEstado(estado): #Dibujado de estados
                painter.setBrush(QBrush(QColor(estado.bgColor), Qt.SolidPattern))
                painter.setPen(QPen(QColor(estado.color),2, Qt.SolidLine))
                vertex = {}
                vertex['x'] = estado.x #Posiciones
                vertex['y'] = estado.y
                radio = 30 #Radio del estado

                if estado == self.automata.estadoInicial:
                    #Dibujado del estado inicial
                    painter.drawLine(QLineF(vertex['x'], vertex['y'],vertex['x']-80, vertex['y']-40))
                    painter.drawLine(QLineF(vertex['x']-80, vertex['y']-40,vertex['x']-80, vertex['y']-40+80))
                    painter.drawLine(QLineF(vertex['x']-80, vertex['y']-40+80,vertex['x'], vertex['y']))


                if estado in self.automata.estadoFinal:
                    #Dibujado de estados finales
                    radio = 36
                    painter.drawEllipse(vertex['x']-radio, vertex['y']-radio,int(radio*2), int(radio*2))
                    radio = 30

                #Dibujado de estados normales
                painter.drawEllipse(vertex['x']-radio, vertex['y']-radio,radio*2, radio*2)
                
                painter.setPen(QPen(QColor(estado.textColor),3, Qt.SolidLine))
                painter.drawText(vertex['x']-11, vertex['y'] + 5, 'q' + str(estado.numeroEstado))

            for i in data:
                dibujarEstado(i)

            painter.end()

    def mousePressEvent(self, event): #Listener de acciones del mouse
        if event.button() == Qt.LeftButton:
            if self.accion == 'estados': #Colocar estados
                self.automata.estados.append(Estado(len(self.automata.estados),event.x(),event.y()))
                self.update()

            if self.accion == 'transiciones': #Hacer transiciones
                if len(self.automata.estados) >0:
                    if self.estadoSeleccionado == None: #Seleccionar el primer estado
                        self.estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                    else: #Seleccionar el segundo estado y concluir transicion
                        estadoDestino = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                        if estadoDestino != None:
                            if str(estadoDestino.numeroEstado) in self.estadoSeleccionado.transiciones.keys():        #En caso de que las transiciones ya existan
                                pass
                            else:
                                if estadoDestino == self.estadoSeleccionado:
                                    #En caso de que sean transiciones a si mismo
                                    if self.estadoSeleccionado.transicionPropia == []:
                                        textoDefault = 'λ'
                                        text, ok = QInputDialog.getText(self, 'Valores de transición', 'Ingrese los valores separados por un espacio', QLineEdit.Normal,textoDefault)
                                        if ok and len(text)>0:
                                            valores = list(set(text.split()))
                                            self.estadoSeleccionado.transicionPropia = valores

                                else:
                                    #Transicion normal
                                    textoDefault = 'λ'
                                    text, ok = QInputDialog.getText(self, 'Valores de transición', 'Ingrese los valores separados por un espacio', QLineEdit.Normal,textoDefault)
                                        
                                    if ok and len(text)>0:
                                        valores = list(set(text.split()))
                                        linea = QLineF(self.estadoSeleccionado.x,self.estadoSeleccionado.y, estadoDestino.x, estadoDestino.y)
                                        self.estadoSeleccionado.transiciones[str(estadoDestino.numeroEstado)] = valores
                            self.update()
                            self.estadoSeleccionado = None
                        else:
                            pass


            if self.accion == 'editarTransiciones': #Editar transiciones
                estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                if estadoSeleccionado != None: #En caso de que el usuario desee editar una transicion hacia si mismo
                    if estadoSeleccionado.transicionPropia != []:
                        textoDefault = ''
                        for i in estadoSeleccionado.transicionPropia:
                            textoDefault += i + ' '

                        text, ok = QInputDialog.getText(self,'Valores de transición', 'Ingrese los valores separados por un espacio', QLineEdit.Normal,textoDefault)
                        
                        if ok:
                            valores = list(set(text.split()))
                            estadoSeleccionado.transicionPropia = valores

                else:
                    #Editar transiciones normales
                    for estado in self.automata.estados: #
                        for numeroEstado in estado.transiciones.keys():
                            estadoDestino = self.automata.estados[int(numeroEstado)]

                            if str(estado.numeroEstado) in list(self.automata.estados[int(numeroEstado)].transiciones.keys()): #En caso de que las transiciones compartan estados
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
                                #Transiciones normales
                                line = QLineF(estado.x,estado.y,estadoDestino.x,estadoDestino.y)
                            

                            linea = copy.deepcopy(line)

                            contador = 0
                            while linea.length()>2: #Reduccion de la linea para asi concordar con el clic del cursor mediante su punto final.
                                contador+=1
                                if contador == 10000:
                                    break
                                distancia = math.sqrt((event.x() - linea.p2().x())**2 + (event.y() - linea.p2().y())**2)
                                if distancia < 10:
                                    #Obtencion de la linea en base a su distancia entre el punto y el cursor
                                    textoDefault = ''
                                    for i in estado.transiciones[numeroEstado]:
                                        textoDefault += i + ' '
                                    text, ok = QInputDialog.getText(self,'Valores de transición', 'Ingrese los valores separados por un espacio', QLineEdit.Normal,textoDefault)
            
                                    if ok:
                                        valores = list(set(text.split()))
                                        estado.transiciones[numeroEstado] = valores
                                    break

                                linea.setLength(linea.length()-5)
                self.update()

            if self.accion == 'moverEstados': 
                #Mover estado
                if len(self.automata.estados) > 0:
                    if self.estadoSeleccionado == None:
                        self.estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                        if self.estadoSeleccionado != None:
                            self.estadoSeleccionado.x = event.x()
                            self.estadoSeleccionado.y = event.y()
                            self.estadoSeleccionado.bgColor = qRgb(100,200,255)
                            self.update()
            
            if self.accion == 'eliminarEstados': 
                #Eliminar estados
                if len(self.automata.estados)>0:
                    estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                    
                    if estadoSeleccionado != None:
                        self.automata.eliminarEstado(estadoSeleccionado.numeroEstado)
                        self.update()

            #Eliminar transiciones utilizando el mismo proceso que editar transiciones
            if self.accion == 'eliminarTransiciones':
                estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
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

            #Marca un estado como inicial

            if self.accion == 'estadoInicial':
                estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                if estadoSeleccionado != None:
                    if self.automata.estadoInicial == estadoSeleccionado: #Deseleccionar un estado inicial
                        self.automata.estadoInicial = None
                    else:
                        self.automata.estadoInicial = estadoSeleccionado
                    self.update()

            if self.accion == 'estadosFinales': #Marcar o desmarcar un estado como final
                estadoSeleccionado = self.obtenerEstadoCercano(Estado(-1,event.x(),event.y()))
                if estadoSeleccionado != None:
                    flag = None

                    for i in range(len(self.automata.estadoFinal)):
                        if self.automata.estadoFinal[i] == estadoSeleccionado:
                            flag = i
                            break

                    if flag == None: #En caso de que no exista
                        self.automata.estadoFinal.append(estadoSeleccionado)
                    else: 
                        #En caso de que si exista
                        del self.automata.estadoFinal[flag]
                    self.update()     
                    

    def mouseMoveEvent(self, event): #Mover estados con el click presionado
        if self.accion == 'moverEstados':
            if self.estadoSeleccionado != None:
                self.estadoSeleccionado.x = event.x()
                self.estadoSeleccionado.y = event.y()
                self.update()

    def mouseReleaseEvent(self, event): #Liberar estado, restaurando su color original
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
        
        self.label = QLabel("Probar el automáta")
        
        self.btnDesarrolladores = QPushButton("Desarrolladores")
        
        self.rightLayout.addWidget(self.btnDesarrolladores)
        self.rightLayout.addWidget(self.label)
        
        
        self.btnProbar = QPushButton("Probar")
        self.btnXML = QPushButton("Generar XML")
        self.rightLayout.addWidget(self.btnXML)
        
        self.btnProbar.clicked.connect(self.probarAutomata)
        self.rightLayout.addWidget(self.btnProbar)
        self.table = QTableWidget()
        self.rightLayout.addWidget(self.table)
        self.table.setColumnCount(2)
        self.table.setRowCount(18)
        self.table.setHorizontalHeaderLabels(['Entrada', 'Aprobación'])

        #Creacion de la tabla de prueba
        for row in range(self.table.rowCount()):
            entrada_item = QTableWidgetItem('')
            self.table.setItem(row, 0, entrada_item)
            
            aprobacion_item = QTableWidgetItem('')
            self.table.setItem(row, 1, aprobacion_item)
        self.table.verticalHeader().setVisible(False)
        self.table.show()

        self.mainLayout.addLayout(self.leftLayout)
        self.mainLayout.addLayout(self.rightLayout)

        self.inputLayout = QHBoxLayout()
        self.cadenaLayout = QHBoxLayout()

        #Todos los botones
        self.btnEstados = QPushButton("Colocar estado")
        self.btnTransiciones = QPushButton("Transiciones")
        self.btnEliminarEstado = QPushButton("Eliminar estado")
        self.btnEditarTransicion = QPushButton("Editar transiciones")
        self.btnMoverEstado = QPushButton("Mover estado")
        self.btnEliminarTransicion = QPushButton("Eliminar transiciones")
        self.btnEstadoFinal = QPushButton("Alternar estados finales")
        self.btnEstadoInicial = QPushButton("Alternar estado inicial")

        self.btnXML.clicked.connect(self.generarXML)
        self.btnEstados.clicked.connect(self.accionEstados)
        self.btnTransiciones.clicked.connect(self.accionTransiciones)
        self.btnEliminarEstado.clicked.connect(self.accionEliminarEstado)
        self.btnEditarTransicion.clicked.connect(self.accionEditarTransicion)
        self.btnMoverEstado.clicked.connect(self.accionMoverEstado)
        self.btnEliminarTransicion.clicked.connect(self.accionEliminarTransicion)
        self.btnEstadoFinal.clicked.connect(self.accionEstadoFinal)
        self.btnEstadoInicial.clicked.connect(self.accionEstadoInicial)
        self.btnDesarrolladores.clicked.connect(self.desarrolladores)

        self.botones = [
            self.btnEstados,
            self.btnMoverEstado,
            self.btnEstadoInicial,
            self.btnEstadoFinal,
            self.btnEliminarEstado,
            self.btnTransiciones,
            self.btnEditarTransicion,
            self.btnEliminarTransicion
        ]

        self.drawWidget = DrawWidget(botones=self.botones)
        self.drawWidget.setStyleSheet("background-color: #d3d3d3;")  
        self.setStyleSheet("background-color: #d3d3d3;") 

        #hacer que los botones puedan mantenerse presionados
        for i in self.botones:
            self.inputLayout.addWidget(i)
            i.setCheckable(True)
        
        self.leftLayout.addLayout(self.inputLayout)
        self.leftLayout.addWidget(self.drawWidget)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle("PYFLAP")

    def desarrolladores(self): #Boton para visualizar los desarrolladores de la aplicacion
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Kency Marisol Saldaña Martínez\nOsiel Alejandro Ordoñez Cruz\nJonathan Canales Puga\nMauricio Hernández Cepeda\nJorge Jhovan Rodríguez Moreno")
            msg.setWindowTitle("Desarrolladores del proyecto:")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()

    def generarXML(self): #Funcion para generar el XML
        #Variables a utilizar
        automata = self.drawWidget.automata
        automata_estadoInicial = automata.estadoInicial # estado
        automata_estadoFinal = automata.estadoFinal # lista de estados finales
        automata_estados = automata.estados # lista de todos estados

        # Creación de la ventana de diálogo para seleccionar el archivo
        file_path, _ = QFileDialog.getSaveFileName(None, "Guardar archivo", "", "Archivos JFLAP (*.jff)")

        if file_path:
            #Creación del .jff
            with open(file_path, 'w') as file:
                file.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?><!--Created with JFLAP 7.1.-->\n')
                file.write('<structure>\n')
                file.write('<type>fa</type>\n')

                file.write('<automaton>\n')
                #Insercion de los estados en el .jff
                for estado in automata_estados:
                    file.write(f'<state id="{estado.numeroEstado}" name="q{estado.numeroEstado}">\n')
                    file.write(f'<x>{estado.x}</x>\n')
                    file.write(f'<y>{estado.y}</y>\n')
                    #Conficion de si el estado es inicial
                    if estado == automata_estadoInicial:
                        file.write(f'<initial/>\n')
                    #Recorrido de estados finales y condicion, si es que hay alguno
                    for final in automata_estadoFinal:
                        if estado == final:
                            file.write(f'<final/>\n')
                    
                    file.write('</state>\n')
                #Insercion de las transiciones de estado a estado
                for estado in automata_estados:
                    if estado.transiciones != {}:
                        for to, values in estado.transiciones.items():
                            for value in values:
                                file.write(f'<transition>\n')
                                file.write(f'<from>{estado.numeroEstado}</from>\n')
                                file.write(f'<to>{to}</to>\n')
                                #Condicion de si es que el simbolo es λ
                                if value != 'λ':
                                    file.write(f'<read>{value}</read>\n')
                                else:
                                    file.write(f'<read/>\n')
                                file.write(f'</transition>\n')
                    # Insercion de las transiciones propias o loops, si es que existen
                    if estado.transicionPropia != []:
                        for value in estado.transicionPropia:
                            file.write(f'<transition>\n')
                            file.write(f'<from>{estado.numeroEstado}</from>\n')
                            file.write(f'<to>{estado.numeroEstado}</to>\n')
                            if(value!='λ'):
                                file.write(f'<read>{value}</read>\n')
                            else:
                                file.write(f'<read/>\n')
                            file.write(f'</transition>\n')
                file.write('</automaton>\n')
                # Se cierra el .jff
                file.write('</structure>\n')

    #Funcion para probar el automata
    def probarAutomata(self):
        #Verificar si existe al menos un estado final y solo un estado inicial
        if self.drawWidget.automata.estadoInicial != None and len(self.drawWidget.automata.estadoFinal) > 0:
            num_rows = self.table.rowCount()

            elements = []

            #Obtener cada elemnto de la primer columna de la tabla
            for row in range(num_rows):
                item = self.table.item(row, 0)
                element = item.text()
                elements.append(element)
            
            resultados = []
            for i in elements: #Probar todas las cadenas ingresadas
                resultados.append(self.drawWidget.automata.probarCadena(i))

            for fila in range(self.table.rowCount()): #Colocar los resultados en la segunda columna e la tabla
                item = QTableWidgetItem(str(resultados[fila]))
                self.table.setItem(fila, 1, item)
        else:
            #En caso de que falta estado final o inicial
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Te falta agregar el estado inicial o algun estado final!")
            msg.setWindowTitle("Espera!")
            msg.setStandardButtons(QMessageBox.Ok)

            msg.exec_()

    #Funciones para cada boton
    def botonPresionado(self,numero):
        for i in self.botones:
            i.setChecked(False)

        self.botones[numero].setChecked(True)
        self.drawWidget.estadoSeleccionado = None

    def accionEstados(self):
        self.botonPresionado(0)
        self.drawWidget.accion = 'estados'

    def accionMoverEstado(self):
        self.botonPresionado(1)
        self.drawWidget.accion = 'moverEstados'

    def accionEstadoInicial(self):
        self.botonPresionado(2)
        self.drawWidget.accion = 'estadoInicial'

    def accionEstadoFinal(self):
        self.botonPresionado(3)
        self.drawWidget.accion = 'estadosFinales'

    def accionEliminarEstado(self):
        self.botonPresionado(4)
        self.drawWidget.accion = 'eliminarEstados'

    def accionTransiciones(self):
        self.botonPresionado(5)
        self.drawWidget.accion = 'transiciones'

    def accionEditarTransicion(self):
        self.botonPresionado(6)
        self.drawWidget.accion = 'editarTransiciones'

    def accionEliminarTransicion(self):
        self.botonPresionado(7)
        self.drawWidget.accion = 'eliminarTransiciones'

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())