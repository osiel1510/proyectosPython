from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
import sys
import math
import copy

#Desarrolladores
#Osiel Alejandro Ordoñez Cruz

class Node: #Clase de todos los nodos que conforman a la lista
    def __init__(self, data,x = None, y = None):
        self.data = data #Valor del nood
        self.next = None #Siguiente nodo
        self.color = qRgb(0,0,0) #Color del borde
        self.bgColor = qRgb(255,255,255) #Color del fondo
        self.textColor = qRgb(0,0,0) #Color del texto
        self.x = x #Posicion en x
        self.y = y #Posicion en y
        self.linea = None #Porcentaje de la linea que se le resta a la linea original
        self.lineaColor = None #Color de la linea provisional
        self.lineaExtra = False #Indicar si se usa una linea provisional
        self.lineaOriginalColor = qRgb(0,0,0) #Color de lal inea original

class LinkedList: #Clase de la lista
    def __init__(self):
        self.head = None #Nodo principal, el de la cabeza

    def restaurarColores(self): #Metodo para restaurar todos los colores a los por defecto
        nodoActual = self.head

        while nodoActual != None:
            nodoActual.color = qRgb(0,0,0)
            nodoActual.bgColor = qRgb(255,255,255)
            nodoActual.textColor = qRgb(0,0,0)
            nodoActual.lineaOriginalColor = qRgb(0,0,0)
            nodoActual.linea = None
            nodoActual.lineaColor = None
            nodoActual = nodoActual.next

    def addToHead(self, data=None,node=None): #Anadir a la cabeza
        new_node = None
        if data == None:
            new_node = node
        else:
            new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def getCola(self): #Obtener la cola
        list = self.traverse()
        return list[len(list)-1]

    def actualizarPosiciones(self): #Restaurar posiciones en base a la cantidad de nodos
        current = self.head
        temp = 30
        while current != None:
            current.x = temp 
            current.y = 100
            temp+=100
            current = current.next

    def add(self, data = None, node = None,nodoAnterior = None): #Anadir nodos
        new_node = None

        if data is None:
            new_node = node #Significa que se inserta un nodo ya existente
        else:
            new_node = Node(data) #Se crea un nuevo nodo con el data

        if nodoAnterior != None: #Se inserta en cierta posicion el nodo
            nodoSiguiente = nodoAnterior.next
            nodoAnterior.next = new_node
            new_node.next = nodoSiguiente
        else:
            if not self.head:
                self.head = new_node
                return

            current = self.head
            
            while current.next:
                current = current.next

            current.next = new_node

    def remove(self, data): #Remover nodo en base a su valor
        if not self.head:
            return

        if self.head.data == data:
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def traverse(self): #Obtener la lista de todos los nodos
        current = self.head
        list = []
        while current:
            list.append(current)
            current = current.next
        return list

class DrawWidget(QWidget): #Clase para dibujar todo
    def __init__(self, parent=None,botones=None):
        super().__init__(parent)
        self.setMinimumSize(1000, 400) 
        self.list = LinkedList() #Lista principal
        self.nodoActual = None #Nodo principal de la animacion
        self.faseNodo = -1 #Fase de la animacion
        self.numeroBuscado = None #Numero o posicion que se busca en la animacion
        self.extraNodes = None #Nodos extra con fines de animacion, pero que no forman parte de la lista
        self.botones = botones #Botones de la aplicacion
        self.animacionActiva = False #Indicar si existe una animacion en curso

    def insertarCola(self): #Insertar nodo en la cola
        number, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa el nùmero a ingresar")

        if ok:
            self.list.restaurarColores()
            self.numeroBuscado = number
            self.timer = QTimer(self)
            
            if len(self.list.traverse()) == 0:
                self.timer.timeout.connect(self.animarInsertarPrimerNodo) 
            else:
                self.timer.timeout.connect(self.animarInsertarCola)
                
            self.timer.start(180)

    def insertarCabeza(self): #Insertar nodo en la cabeza
        number, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa el nùmero a ingresar")

        if ok:
            self.list.restaurarColores()
            self.numeroBuscado = number
            self.timer = QTimer(self)
            
            if len(self.list.traverse()) == 0:
                self.timer.timeout.connect(self.animarInsertarPrimerNodo)
            else:
                self.timer.timeout.connect(self.animarInsertarCabeza)
                
            self.timer.start(180)

    def insertarEnPosicion(self): #Insertar en cierta posicion dada
        number, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa el nùmero a ingresar")

        if ok:
            position, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa la posiciòn en donde colocarlo")
            if ok:
                if position <= len(self.list.traverse()):
                    self.list.restaurarColores()
                    self.timer = QTimer(self)
                    
                    if position == 0:
                        if len(self.list.traverse()) == 0:
                            self.numeroBuscado = number
                            self.timer.timeout.connect(self.animarInsertarPrimerNodo)
                        else:
                            self.numeroBuscado = number
                            self.timer.timeout.connect(self.animarInsertarCabeza)
                    elif position == len(self.list.traverse()):
                        self.numeroBuscado = number
                        self.timer.timeout.connect(self.animarInsertarCola)
                    else:
                        self.numeroBuscado = [number,position]
                        self.timer.timeout.connect(self.animarInsertarEnPosicion)

                    self.timer.start(180)

                else:
                    pass
    
    def animarInsertarEnPosicion(self): #Animacion de insertar en posicion
        
        if self.nodoActual == None:
            self.animacionActiva = True
            self.nodoActual = self.list.head

        if self.faseNodo == 0 or self.faseNodo == -1:
            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)
            
            lista = self.list.traverse()
            for i in range (len(lista)):
                if lista[i] == self.nodoActual:
                    if i == self.numeroBuscado[1]:
                        self.faseNodo = 6
                        self.nodoActual.bgColor = qRgb(50,50,255)
                        self.nodoActual.textColor = qRgb(255,255,255)
                        self.nodoActual.color = qRgb(50,50,255)

        elif self.faseNodo == 1:

            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)

        elif self.faseNodo == 2:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 3:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 4:
            self.nodoActual.linea = 40 
        
        elif self.faseNodo == 5:
            self.nodoActual.linea = 20
            self.nodoActual = self.nodoActual.next
            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)
            self.nodoActual.color = qRgb(255,255,255)
            self.faseNodo = -1
        
        elif self.faseNodo == 7:
            nodoExtra = Node(self.numeroBuscado[0])
            nodoExtra.x = self.nodoActual.x
            nodoExtra.y = self.nodoActual.y + 150
            nodoExtra.bgColor = qRgb(50,200,50)
            nodoExtra.textColor = qRgb(255,255,255)
            nodoExtra.color = qRgb(50,200,50)

            nodoExtra2 = Node(0)
            nodoExtra2.x = self.nodoActual.x
            nodoExtra2.y = self.nodoActual.y + 50
            nodoExtra2.bgColor = qRgb(211,211,211)
            nodoExtra2.textColor = qRgb(211,211,211)
            nodoExtra2.color = qRgb(211,211,211)

            self.nodoActual = self.list.traverse()[self.numeroBuscado[1]-1]
            self.nodoActual.lineaOriginalColor = qRgb(211,211,211)
            self.nodoActual.lineaColor = qRgb(255,90,0)
            self.nodoActual.linea = 0
            self.nodoActual.lineaExtra = True
            self.extraNodes = []
            self.extraNodes.append(nodoExtra2)
            self.extraNodes.append(nodoExtra)
            
        elif self.faseNodo == 8 or self.faseNodo == 9:
            self.nodoActual.lineaColor = qRgb(255,90,0)
            self.extraNodes[0].y+=50
        
        elif self.faseNodo == 10:
            self.list.add(node=self.extraNodes[1],nodoAnterior=self.nodoActual)
            self.extraNodes = None
            self.nodoActual.lineaExtra = False
            self.nodoActual.linea = None
            self.nodoActual.lineaColor = None
            self.nodoActual.lineaOriginalColor = qRgb(255,90,0)
            self.nodoActual = self.nodoActual.next
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)
            self.nodoActual.lineaOriginalColor = qRgb(211,211,211)

        elif self.faseNodo == 11 or self.faseNodo == 12:
            self.nodoActual.linea-=20

        elif self.faseNodo == 13:
            self.nodoActual.linea= None
            self.nodoActual.lineaOriginalColor = qRgb(50,200,50)

        elif self.faseNodo == 14 or self.faseNodo == 15:
            siguiente = self.nodoActual.next
            while siguiente != None:
                siguiente.x += 50
                siguiente = siguiente.next
        
        elif self.faseNodo == 16 or self.faseNodo == 17:
            self.nodoActual.y-=50

        elif self.faseNodo == 18:
            self.nodoActual.y-=50
            self.list.restaurarColores()
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.extraNodes = None
            self.animacionActiva = False

        if self.faseNodo >= -1 and self.faseNodo <= 4:
            self.faseNodo+=1

        if self.faseNodo >= 6 and self.faseNodo <= 18:
            self.faseNodo+=1

        self.update()
        
    def animarInsertarPrimerNodo(self): #Animacion para insertar en el primer nodo

        if self.faseNodo == 0 or self.faseNodo == -1:
            self.animactionActiva = True
            nodo = Node(self.numeroBuscado)
            nodo.y = 100
            nodo.x = 30
            nodo.bgColor = qRgb(255,90,0)
            nodo.textColor = qRgb(255,255,255)
            nodo.color = qRgb(255,90,0)
            self.list.add(node=nodo)
            self.nodoActual = nodo
            self.faseNodo = 1
        
        elif self.faseNodo == 1:
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.extraNodes = None
            self.animacionActiva = False
        self.update()

    def animarInsertarCabeza(self): #Animacion para insertar nuevo nodo en la cabeza
        if self.faseNodo == 0:
            self.animacionActiva = True
            nodo = Node(self.numeroBuscado)
            nodo.y = 200
            nodo.x = self.list.head.x
            nodo.bgColor = qRgb(255,90,0)
            nodo.textColor = qRgb(255,255,255)
            nodo.color = qRgb(255,90,0)
            self.nodoActual = nodo
            self.extraNodes = [self.list.head]
            self.list.addToHead(node=nodo)
            self.nodoActual.lineaOriginalColor = qRgb(211,211,211)

        elif self.faseNodo == 1:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)
            
        elif self.faseNodo == 2:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 3:
            self.nodoActual.linea = 40
        
        elif self.faseNodo == 4:
            self.nodoActual.linea = 20

        elif self.faseNodo == 5:
            self.list.restaurarColores()
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)
        
        elif self.faseNodo == 6 or self.faseNodo == 7:
            lista = self.list.traverse()
            for i in range(1,len(lista)):
                lista[i].x += 50
        
        elif self.faseNodo == 8:
            self.nodoActual.y-=50

        elif self.faseNodo == 9:
            self.nodoActual.y-=50
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.extraNodes = None
            self.animacionActiva = False
        if self.faseNodo >= -1 and self.faseNodo <= 8:
            self.faseNodo+=1

        self.update()

    def animarInsertarCola(self): #Animacion para insertar nuevo nodo en la cola
        if self.faseNodo == 0 or self.faseNodo == -1:
            self.animacionActiva = True
            nodo = Node(self.numeroBuscado)
            nodo.y = 100
            nodo.x = self.list.getCola().x + 100
            nodo.bgColor = qRgb(255,90,0)
            nodo.textColor = qRgb(255,255,255)
            nodo.color = qRgb(255,90,0)
            self.extraNodes = [ ]
            self.extraNodes.append(nodo)

        if self.faseNodo == 1:
            self.nodoActual = self.list.getCola()
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)

        elif self.faseNodo == 3:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 4:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 5:
            self.nodoActual.linea = 40
        
        elif self.faseNodo == 6:
            self.nodoActual.linea = 20

        elif self.faseNodo == 7:
            self.nodoActual.linea = 0

        elif self.faseNodo == 9:
            self.list.restaurarColores()
            self.list.add(node=self.extraNodes[0])
            self.nodoActual = self.list.getCola()
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.extraNodes = None
            self.animacionActiva = False

        if self.faseNodo >= -1 and self.faseNodo <= 8:
            self.faseNodo+=1

        self.update()

    def search(self): #Busqueda de un valor dentro de la lista
        number, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa el nùmero a ingresar")

        if ok:
            self.list.restaurarColores()
            self.numeroBuscado = number
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.animarBusqueda)
            self.timer.start(180)

    def animarBusqueda(self): #Animacion de busqueda
        if self.nodoActual == None:
            self.animacionActiva = True
            self.nodoActual = self.list.head

        if self.faseNodo == 0 or self.faseNodo == -1:
            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)
            if self.numeroBuscado == self.nodoActual.data:
                self.faseNodo = 7

        elif self.faseNodo == 1:

            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)

        elif self.faseNodo == 2:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 3:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 4:
            self.nodoActual.linea = 40 
        
        
        elif self.faseNodo == 5:
            self.nodoActual.linea = 20

        elif self.faseNodo == 6:
            self.nodoActual.linea = 0

            if self.nodoActual.next != None:
                self.nodoActual = self.nodoActual.next
                self.faseNodo = -1
            else:          
                self.animacionActiva = False
                self.timer.stop()
                self.faseNodo = -1
                self.nodoActual = None
                self.numeroBuscado = None
        
        elif self.faseNodo == 7:
            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.animacionActiva = False


        if self.faseNodo >= -1 and self.faseNodo <= 5:
            self.faseNodo+=1
        self.update()

    def removerCabeza(self): #Remover la cabeza de la lista
        if len(self.list.traverse()) > 1:
            self.list.restaurarColores()
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.animarBorradoCabeza)
            self.timer.start(180)
        elif len(self.list.traverse()) > 0:
            self.list.remove(self.list.head.data)
            self.update()

    def animarBorradoCabeza(self): #Animacion de eliminado de la cabeza
        if self.nodoActual == None:
            self.animacionActiva = True
            self.nodoActual = self.list.head

        if self.faseNodo == 0 or self.faseNodo == -1:
            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)

        elif self.faseNodo == 1:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 2 or self.faseNodo == 3 or self.faseNodo == 4:
            self.nodoActual.linea -=20

        elif self.faseNodo == 5:
            self.nodoActual.linea = None
            self.nodoActual.lineaOriginalColor = qRgb(50,200,50)
            self.nodoActual.next.bgColor = qRgb(50,200,50)
            self.nodoActual.next.textColor = qRgb(255,255,255)
            self.nodoActual.next.color = qRgb(50,200,50)      

        elif self.faseNodo == 6:
            data = self.nodoActual.data 
            self.nodoActual = None
            self.list.remove(data)
            siguiente = self.list.head
            while siguiente != None:
                siguiente.x-=50
                siguiente = siguiente.next
        
        elif self.faseNodo == 7:
            self.list.actualizarPosiciones()
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.animacionActiva = False
            self.numeroBuscado = None

        if self.faseNodo >= -1 and self.faseNodo <= 6:
            self.faseNodo+=1
        self.update()

    def removerCola(self): #Remover cola de la lista
        self.list.restaurarColores()
        self.timer = QTimer(self)
        if len(self.list.traverse()) >1:
            self.timer.timeout.connect(self.animarBorrarCola)
            self.timer.start(120)
        else:
            self.list.remove(self.list.head.data)
            self.update()

    def animarBorrarCola(self): #Animacion de eliminado de cola
        if self.nodoActual == None:
            self.animacionActiva = True
            self.nodoActual = self.list.head

        if self.faseNodo == 0 or self.faseNodo == -1:

            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)


            nodo = self.list.head
            
            while nodo != None:
                nodo.linea = None
                nodo.lineacolor = None
                nodo.lineaOriginalColor = qRgb(0,0,0)
                nodo = nodo.next

            if self.nodoActual.next != None:
                self.nodoActual.next.bgColor = qRgb(50,200,50)
                self.nodoActual.next.textColor = qRgb(255,255,255)
                self.nodoActual.next.color = qRgb(50,200,50)
            else:
                self.nodoActual.bgColor = qRgb(50,200,50)
                self.nodoActual.textColor = qRgb(255,255,255)
                self.nodoActual.color = qRgb(50,200,50)

            if self.numeroBuscado == self.nodoActual.data:
                self.faseNodo = 7

        elif self.faseNodo == 1:

            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)

            if self.nodoActual.next == None:
                self.nodoActual.bgColor = qRgb(50,200,50)
                self.nodoActual.textColor = qRgb(255,255,255)
                self.nodoActual.color = qRgb(50,200,50)

        elif self.faseNodo == 2:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 3:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 4:
            self.nodoActual.linea = 40 
        
        
        elif self.faseNodo == 5:
            self.nodoActual.linea = 20
            self.nodoActual.lineaColor = qRgb(50,200,50)
            self.nodoActual.lineaOriginalColor = qRgb(50,200,50)

        elif self.faseNodo == 6:
            self.nodoActual.linea = 0
            if self.nodoActual.next != None:
                self.nodoActual = self.nodoActual.next
                self.faseNodo = -1
            else:
                self.faseNodo = 8
                lista = self.list.traverse()
                self.nodoActual = lista[len(lista)-2]
                nodoExtra = lista[len(lista)-1]
                
                self.extraNodes = []
                self.extraNodes.append(nodoExtra)
                self.nodoActual.lineaColor = qRgb(0,0,0)
                self.nodoActual.lineaOriginalColor = qRgb(211,211,211)
                self.nodoActual.linea = 0
        
        elif self.faseNodo == 9 or self.faseNodo == 10 or self.faseNodo == 11 or self.faseNodo == 12:
            self.nodoActual.linea +=20

        elif self.faseNodo == 13:
            self.list.remove(self.nodoActual.next.data)
            self.list.restaurarColores()
            self.list.actualizarPosiciones()
            self.nodoActual.bgColor = qRgb(50,200,50)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(50,200,50)
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None         
            self.extraNodes = None
            self.animacionActiva = False

        if self.faseNodo >= -1 and self.faseNodo <= 5:
            self.faseNodo+=1

        if self.faseNodo >= 7:
            self.faseNodo+=1

        self.update()

    def removerPorPosicion(self): #Remover por posicion 
        position, ok = QInputDialog.getInt(None, "Ingresar datos", "Ingresa la posiciòn a eliminar")

        if ok:
            if position < len(self.list.traverse()):
                self.list.restaurarColores()
                self.timer = QTimer(self)
                
                if position == 0:
                    if len(self.list.traverse()) == 1:
                        self.list.remove(self.list.head.data)
                        self.update()
                    else:
                        self.timer.timeout.connect(self.animarBorradoCabeza)
                elif position == len(self.list.traverse())-1:
                    self.timer.timeout.connect(self.animarBorrarCola)
                else:
                    self.numeroBuscado = position
                    self.timer.timeout.connect(self.animarBorrarPorPosicion)

                self.timer.start(180)

            else:
                pass
    
    def animarBorrarPorPosicion(self): #Animacion de borrdo por posicion
        if self.nodoActual == None:
            self.animacionActiva = True
            self.nodoActual = self.list.head

        if self.faseNodo == 0 or self.faseNodo == -1:
            self.nodoActual.bgColor = qRgb(255,90,0)
            self.nodoActual.textColor = qRgb(255,255,255)
            self.nodoActual.color = qRgb(255,90,0)
            
            lista = self.list.traverse()
            for i in range (len(lista)):
                if lista[i] == self.nodoActual:
                    if i == self.numeroBuscado:
                        self.faseNodo = 6
                        self.list.traverse()[i-1].bgColor = qRgb(255,90,0)
                        self.list.traverse()[i-1].textColor = qRgb(255,255,255)
                        self.list.traverse()[i-1].color = qRgb(255,90,0)
                        self.nodoActual.bgColor = qRgb(255,50,50)
                        self.nodoActual.textColor = qRgb(255,255,255)
                        self.nodoActual.color = qRgb(255,50,50)
                        self.nodoActual.next.bgColor = qRgb(50,200,50)
                        self.nodoActual.next.textColor = qRgb(255,255,255)
                        self.nodoActual.next.color = qRgb(50,200,50)

        elif self.faseNodo == 1:

            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)

        elif self.faseNodo == 2:
            self.nodoActual.linea = 80
            self.nodoActual.lineaColor = qRgb(255,90,0)

        elif self.faseNodo == 3:
            self.nodoActual.linea = 60
        
        elif self.faseNodo == 4:
            self.nodoActual.linea = 40 
        
        elif self.faseNodo == 5:
            self.nodoActual.linea = 20
            self.nodoActual = self.nodoActual.next
            self.nodoActual.bgColor = qRgb(255,255,255)
            self.nodoActual.textColor = qRgb(255,90,0)
            self.nodoActual.color = qRgb(255,255,255)
            self.faseNodo = -1
        
        elif self.faseNodo == 7:
            salir = False
            nodo = self.list.head
            while salir == False:
                if nodo.next == self.nodoActual:
                    salir = True
                    self.nodoActual = nodo
                else:
                    nodo = nodo.next     
            
            nodoExterno = copy.deepcopy(self.nodoActual.next.next)
            self.extraNodes = [nodoExterno]
            self.nodoActual.lineaExtra = True
            self.nodoActual.lineaOriginalColor = qRgb(211,211,211)
            self.nodoActual.lineaColor = qRgb(255,90,0)
            self.nodoActual.linea = 50
            
        elif self.faseNodo == 8 or self.faseNodo == 9:
            self.nodoActual.next.y+=50

        elif self.faseNodo == 10 or self.faseNodo == 11:
            self.nodoActual.linea -=20
            
        elif self.faseNodo == 12:
            self.extraNodes = None
            self.list.remove(self.nodoActual.next.data)
            self.nodoActual.linea = None
            self.nodoActual.lineaExtra = False
            self.nodoActual.lineaColor = None
            self.nodoActual.lineaOriginalColor = qRgb(0,0,0)

        elif self.faseNodo == 13:
            nodo = self.nodoActual.next

            while True:
                nodo.x -=50
                nodo = nodo.next
                if nodo == None:
                    break

        elif self.faseNodo == 14:
            nodo = self.nodoActual.next
            while True:
                nodo.x -=50
                nodo = nodo.next
                if nodo == None:
                    break
                
            self.timer.stop()
            self.faseNodo = -1
            self.nodoActual = None
            self.numeroBuscado = None
            self.animacionActiva = False

        if self.faseNodo >= -1 and self.faseNodo <= 4:
            self.faseNodo+=1

        if self.faseNodo >= 6 and self.faseNodo <= 14:
            self.faseNodo+=1

        self.update()

    def paintEvent(self, event): #Funcion paintevent que se llama al hacer update()
        if self.animacionActiva == True: #Activar o desactivar los botones, para prevenir 
            for i in self.botones:       #Que el usuario accione animaciones mientras ocurre
                i.setEnabled(False)      #Una animacion
        else:
            for i in self.botones:
                i.setEnabled(True)

        if len(self.list.traverse()) > 0:
            painter = QPainter()
            painter.begin(self)
            data = self.list.traverse()
            painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
            
            for edge in data: #Dibujar las aristas
                if edge.next != None:
                    u = {} #Origen
                    u['x'] = edge.x 
                    u['y'] = edge.y
                    v = {} #Destino
                    v['x'] = edge.next.x
                    v['y'] = edge.next.y

                    #Automaticamente siempre se hara una arista entre un nodo y su siguiente nodo

                    line = QLineF(u['x'], u['y'], v['x'], v['y']) 
                    line.setLength(line.length() - 22) #Reduccion de la arista para que se
                                                        #Pued visualizar la flecha

                    if edge.linea != None and edge.lineaExtra == False: #Dibujado de linea reducida
                        painter.setPen(QPen(QColor(edge.lineaOriginalColor),3, Qt.SolidLine))
                        painter.drawLine(line)
                        line2 = copy.deepcopy(line)
                        line2.setLength(line.length() - (line.length()*(edge.linea/100)))
                        painter.setPen(QPen(QColor(edge.lineaColor),3, Qt.SolidLine))
                        painter.drawLine(line2)
                        painter.setPen(QPen(QColor(edge.lineaOriginalColor),3, Qt.SolidLine))
                    else :
                        painter.setPen(QPen(QColor(edge.lineaOriginalColor),3, Qt.SolidLine))
                        painter.drawLine(line)
                    arrow_size = 10

                    angle = math.atan2(v['y'] - u['y'], v['x'] - u['x'])

                    p1 = QPointF(int(line.x2() - arrow_size * math.cos(angle - math.pi / 6)),int(line.y2() - arrow_size * math.sin(angle - math.pi / 6)))                
                    p2 = QPointF(int(line.x2() - arrow_size * math.cos(angle + math.pi / 6)),int(line.y2() - arrow_size * math.sin(angle + math.pi / 6)))
                    
                    painter.drawLine(QLineF(line.x2(), line.y2(), p1.x(), p1.y()))
                    painter.drawLine(QLineF(line.x2(), line.y2(), p2.x(), p2.y()))

                if edge == self.nodoActual and edge.linea != None and self.extraNodes != None:
                    #Funcion para dibujar aristas entre el nodo actual y los nodos extra
                    u = {}
                    u['x'] = edge.x
                    u['y'] = edge.y
                    v = {}
                    v['x'] = self.extraNodes[0].x
                    v['y'] = self.extraNodes[0].y

                    line = QLineF(u['x'], u['y'], v['x'], v['y']) 
                    line.setLength(line.length() - 22)

                    if edge.linea != None:
                        line2 = copy.deepcopy(line)
                        line2.setLength(line.length() - (line.length()*(edge.linea/100)))
                        painter.setPen(QPen(QColor(edge.lineaColor),3, Qt.SolidLine))
                        painter.drawLine(line2)
                        painter.setPen(QPen(QColor(qRgb(0,0,0)),3, Qt.SolidLine))
                    
            font = QFont()
            font.setPointSize(16)
            painter.setFont(font)

            def dibujarVertex(vertexx): #Dibujado de vertices
                painter.setBrush(QBrush(QColor(vertexx.bgColor), Qt.SolidPattern))
                painter.setPen(QPen(QColor(vertexx.color),3, Qt.SolidLine))
                
                vertex = {}
                vertex['x'] = vertexx.x
                vertex['y'] = vertexx.y
                painter.drawEllipse(vertex['x'] - 25, vertex['y'] - 25, 40, 40) 

                
                painter.setPen(QPen(QColor(vertexx.textColor),3, Qt.SolidLine))

                if vertexx.data > 9:
                    painter.drawText(vertex['x']-15, vertex['y'] + 5, str(vertexx.data))
                else:
                    painter.drawText(vertex['x']-11, vertex['y'] + 5, str(vertexx.data))
                
                
                painter.setPen(QPen(QColor(qRgb(255,0,0)),3, Qt.SolidLine))

            for i in data:
                dibujarVertex(i)

            if len(data) < 2: #DIbujado para indicar cual elemento es la cabeza y cual la cla
                painter.drawText(self.list.head.x-28, self.list.head.y + 33, str('head'))
                painter.drawText(self.list.head.x-20, self.list.head.y + 55, str('tail'))
            else:
                painter.drawText(self.list.head.x-28, self.list.head.y + 33, str('head'))
                painter.drawText(self.list.getCola().x-20, self.list.getCola().y + 33, str('tail'))

            if self.extraNodes != None: #Dibujado de los nodos extra
                for i in self.extraNodes:
                    dibujarVertex(i)
                    
            painter.end()

class MainWindow(QWidget): #Clase principal
    def __init__(self, parent=None): 
        QWidget.__init__(self, parent)
        #Tamaño máximo de la ventana
        self.setFixedSize(1000,400)

        self.mainLayout = QVBoxLayout()
        self.inputLayout = QHBoxLayout()#Layout para ingresar datos y botones

        #Todos los botones
        self.btnPush = QPushButton("Insertar en cola")
        self.btnPushHead = QPushButton("Insertar en cabeza")
        self.btnPushOriginal = QPushButton("Insertar segùn posiciòn")
        self.btnSearch = QPushButton("Buscar")
        self.btnRemoverCabeza = QPushButton("Remover cabeza")
        self.btnRemoverCola = QPushButton("Remover cola")
        self.btnRemoverPorPosicion = QPushButton("Remover por posiciòn")

        botones = [
            self.btnPush,
            self.btnPushHead,
            self.btnPushOriginal,
            self.btnSearch,
            self.btnRemoverCabeza,
            self.btnRemoverCola,
            self.btnRemoverPorPosicion,
        ]

        self.drawWidget = DrawWidget(botones=botones) #Widget para mostrar los dibujos
        self.drawWidget.setStyleSheet("background-color: #d3d3d3;")  # Cambiar el color del fondo
        self.setStyleSheet("background-color: #d3d3d3;") #Cambiar el color del fondo
        
        #Acciones de los botones
        self.btnRemoverCabeza.clicked.connect(self.drawWidget.removerCabeza)
        self.btnPush.clicked.connect(self.drawWidget.insertarCola)
        self.btnSearch.clicked.connect(self.drawWidget.search)
        self.btnPushOriginal.clicked.connect(self.drawWidget.insertarEnPosicion)
        self.btnPushHead.clicked.connect(self.drawWidget.insertarCabeza)
        self.btnRemoverCola.clicked.connect(self.drawWidget.removerCola)
        self.btnRemoverPorPosicion.clicked.connect(self.drawWidget.removerPorPosicion)

        for i in botones:
            self.inputLayout.addWidget(i)
        
        self.mainLayout.addLayout(self.inputLayout)
        self.mainLayout.addWidget(self.drawWidget)
        
        self.setLayout(self.mainLayout)
        self.setWindowTitle("Lista enlazada")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    form = MainWindow()
    form.show()
    sys.exit(app.exec_())
