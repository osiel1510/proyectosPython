import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout,QHBoxLayout, QPushButton,QDoubleSpinBox,QRadioButton,QLabel,QTabWidget,QButtonGroup,QDoubleSpinBox,QSpinBox
import numpy as np  
from PyQt5 import QtGui
from PyQt5.QtGui import *
import numpy as np

class HLayout(QHBoxLayout): #Layout que asigna widgets y layouts automaticamente
    def __init__(self,widgets = None, layouts = None):  
        super(HLayout, self).__init__()
        if widgets != None:
            for i in widgets:
                self.addWidget(i)
        if layouts !=  None:
            for i in layouts:
                self.addLayout(i)
        #self.setContentsMargins(0, 0, 0, 0)
        #self.setSpacing(0)

class BMILayout(QVBoxLayout): #Layout principal que contiene todos los elementos relacionados con el cálculo del BMI.
    def __init__(self,age,radio,height,weight):
        super(BMILayout, self).__init__()
        self.age = age
        self.radio = radio 
        self.height = height
        self.weight = weight
        self.addLayout(self.age)
        self.addLayout(self.radio)
        self.addLayout(self.height)
        self.addLayout(self.weight)
        self.minHealthyBMI = 18.5
        self.maxHealthyBMi = 25

    def getData(self,maleData,femaleData):
        return [self.getBMI(maleData,femaleData),self.getHealthyLimits(maleData,femaleData),self.getPonderalIndex()]  #Funcion para calcular y obtener toda la informacion necesaria
        
    def getPonderalIndex(self): #Funcion para obtener el ponderal index
        if(type(self.height) == type(self.age)):
            return str(round(self.weight.getInputText() / ((self.height.getInputText()/100)**3),1)) + " kg/m\u00b3"
        else:   
            return str(round((self.convertLbToKg(self.weight.getInputText()))/self.convertInchesToM(self.height.getInputText(),self.height.getInputText2())**3,1))  + " kg/m\u00b3"

    def getBMI(self,maleData,femaleData): #Funcion para calcular el BMI
        bmi = self.calculateBMI(self.weight.getInputText())
        age = self.age.getInputText()
        gender = self.radio.getSelectedRadio()
        file = {}
        if age < 20: #En caso de que sea menor de edad
            if gender == 'Male':
                file = maleData
            else:
                file = femaleData 
            data_by_age = file[age-1]   
            array = np.array(list(data_by_age.values()))
            difference_aray = np.absolute(array-bmi)
            index = difference_aray.argmin()
            return (bmi,list(data_by_age.keys())[index])
        else:
            return [bmi]
    
    def getHealthyLimits(self,maleData,femaleData): #Funcion para obtener los limites adecuados en base al peso y a la altura
        healthyLimits = []
        healthyBMIRange = []
        if self.age.getInputText() < 20:
            if self.radio.getSelectedRadio() == 'Male':
                file = maleData
            else:
                file = femaleData
            data_by_age = file[self.age.getInputText()-1]
            healthyLimits.append(self.getWeightByBMi(data_by_age['5']))
            healthyLimits.append(self.getWeightByBMi(data_by_age['85']))
            healthyBMIRange.append(str(round(data_by_age['5'],1)))
            healthyBMIRange.append(str(round(data_by_age ['85'],1)))
        else:
            healthyLimits.append(self.getWeightByBMi(18.5))
            healthyLimits.append(self.getWeightByBMi(25))
            healthyBMIRange.append('18.5')
            healthyBMIRange.append('25')
        
        if(type(self.height) == type(self.age)):
            healthyLimits.append('kg')
        else:
            healthyLimits.append('lbs')

        return [healthyLimits,healthyBMIRange]
    
    def getWeightByBMi(self,bmi): #Formula de bmi despejada para obtener el peso
        if(type(self.height) == type(self.age)):
            return str(round(bmi * ((self.height.getInputText()/100)**2),1))
        else:
            return str(round(self.convertMToInches((bmi * self.convertInchesToM(self.height.getInputText(),self.height.getInputText2())**2)),1))

    def getWeight(self):
        if(type(self.height) == type(self.age)):
            return self.weight.getInputText()
        else:
            return self.weight.getInputText()

    def convertLbToKg(self,lb):
        return lb * 0.453592

    def convertInchesToM(self,ft,inches):
        return ((ft*12)+inches)*0.0254
    
    def convertMToInches(self,meters):
        return meters*2.20462
    
    def convertKgToLB(self,kg):
        return kg * 2.20462 
    
    def calculateBMI(self,weight): #Formula para obtener el BMI
        if(type(self.height) == type(self.age)):
            bmi = weight / ((self.height.getInputText()/100) **2)
        else:
            bmi = 703*(weight / ((self.height.getInputText()*12 + self.height.getInputText2()) **2))
        return bmi

class VLayout(QVBoxLayout): #Layout vertical que asigna automaticamente widgets y layouts
    def __init__(self,widgets = None, layouts = None):
        super(VLayout, self).__init__()
        if widgets != None:
            for i in widgets:
                self.addWidget(i)
        if layouts !=  None:
            for i in layouts:
                self.addLayout(i)
        #self.setContentsMargins(0, 0, 0, 0)
        #self.setSpacing(0)
class HLayoutRadio(QHBoxLayout): #Layout que contiene dos radio buttons
    def __init__(self,title,firstRadio,secondRadio):
        super(HLayoutRadio, self).__init__()
        self.title = QLabel(title)
        self.firstRadio = QRadioButton(firstRadio)
        self.secondRadio = QRadioButton(secondRadio)
        buttonGroup = QButtonGroup()
        self.addWidget(self.title)
        self.addWidget(self.firstRadio)
        self.addWidget(self.secondRadio)
        buttonGroup.addButton(self.firstRadio)
        self.firstRadio.setChecked(True)
        buttonGroup.addButton(self.secondRadio)
        self.firstRadio.toggled.connect(self.checkRadioButton)
        self.secondRadio.toggled.connect(self.checkRadioButton)
        self.selectedRadio = self.firstRadio
        
    def checkRadioButton(self):
        if(self.firstRadio.isChecked()):
            self.selectedRadio = self.firstRadio
        else:
            self.selectedRadio = self.secondRadio

    def getSelectedRadio(self):
        return self.selectedRadio.text()

class Tab(QTabWidget): #Clase de las pestañas de las diferentes interfaces
    def __init__(self):
        super(Tab, self).__init__()
        self.usUnitsTab = QWidget()
        self.metricUnitsTab = QWidget()
        self.activeIndex = 0

        self.addTab(self.usUnitsTab,"US Units")
        self.addTab(self.metricUnitsTab,"Metric Units")
        self.tabBarClicked.connect(self.handle_tabbar_clicked)

        self.tab1UI()
        self.tab2UI()

    def tab1UI(self): #Interfaz de unidades metricas
        ageLayout = HLayoutInput('Age','Ages 2 - 120','int')
        ageLayout.setInputText(25)
        genderLayout = HLayoutRadio('Gender','Male','Female')
        weightLayout = HLayoutInput('Weight','kg','double')
        weightLayout.setInputText(65)
        heightLayout = HLayoutInput('Height','cm','double')
        heightLayout.setInputText(180)
        self.metricUnitsLayout = BMILayout(ageLayout,genderLayout,heightLayout,weightLayout)
        self.setTabText(0,"Metric Units")
        self.metricUnitsTab.setLayout(self.metricUnitsLayout)

    def tab2UI(self): #Interfaz de uniades de estados unidos
        heightLayout = HLayoutDoubleInput('Height','feet','inches','double')    
        heightLayout.setInputText(5)
        heightLayout.setInputText2(10)
        ageLayout = HLayoutInput('Age','Ages 2 - 120','int')
        ageLayout.setInputText(25)
        genderLayout = HLayoutRadio('Gender','Male','Female')
        weightLayout = HLayoutInput('Weight','pounds','double')
        weightLayout.setInputText(160)
        self.usUnitsLayout = BMILayout(ageLayout,genderLayout,heightLayout,weightLayout)
        self.setTabText(0,"US Units")
        self.usUnitsTab.setLayout(self.usUnitsLayout)

    def handle_tabbar_clicked(self, index):
        self.activeIndex = index #Obtener cual pestaña esta visible

    def calculateData(self,maleData,femaleData): #Obtener la informacion de las tabs
        if self.activeIndex == 0:
            return self.usUnitsLayout.getData(maleData,femaleData)
        else:
            return self.metricUnitsLayout.getData(maleData,femaleData)  
        
    def getWeight(self):
        if self.activeIndex == 0:
            return self.usUnitsLayout.getWeight()
        else:
            return self.metricUnitsLayout.getWeight()

class NoZeroQDoubleSpinBox(QDoubleSpinBox): #QDoubleSpinBox con limites predefinidos
    def __init__(self,stylesheet):
        super(NoZeroQDoubleSpinBox, self).__init__()
        self.setStyleSheet(stylesheet)
        self.setButtonSymbols(2)
        self.setMinimum(0.1)
        self.setMaximum(999999)
        self.setDecimals(1)

class MinMaxQIntegerSpinBox(QSpinBox): #QSpinBox con limites predefinidos
    def __init__(self,stylesheet,min,max):
        super(MinMaxQIntegerSpinBox, self).__init__()
        self.setStyleSheet(stylesheet)
        self.setButtonSymbols(2)
        self.setMinimum(min)
        self.setMaximum(max)

class HLayoutInput(QHBoxLayout): #QHBoxLayout que contiene un label, un hint y un qspinbox
    def __init__(self,title,hint,type):
        super(HLayoutInput,self).__init__()
        self.title = QLabel(title)
        self.hint = QLabel(hint)
        self.type = None
        if type == 'double':
            self.input = NoZeroQDoubleSpinBox("QDoubleSpinBox{background: rgb(255,255,255)}")
        else:
            self.input = MinMaxQIntegerSpinBox("QSpinBox{background: rgb(255,255,255)}",2,120)
        self.addWidget(self.title)
        self.addWidget(self.input)
        self.addWidget(self.hint)

    def getInputText(self):
        return self.input.value()

    def setInputText(self, text):
        self.input.setValue(text)

class HLayoutDoubleInput(HLayoutInput): #Subclase para cuando son dos hints y dos inputs
    def __init__(self,title,hint,hint2,type):
        super(HLayoutDoubleInput,self).__init__(title,hint,type)
        self.input2 = None
        if type == 'double':
            self.input2 = NoZeroQDoubleSpinBox("QDoubleSpinBox{background: rgb(255,255,255)}")
        else:
            self.input2 = MinMaxQIntegerSpinBox("QSpinBox{background: rgb(255, 255,255)}",0,9999)
        self.hint2 = QLabel(hint2)
        self.addWidget(self.input2)
        self.addWidget(self.hint2)

    def getInputText2(self):
        return self.input2.value()
    
    def setInputText2(self,text):
        self.input2.setValue(text)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("BMI Calculator")
        self.setStyleSheet("background-color: #e6e6e6")
        self.setFixedSize(800,400)        

        self.maleData = self.readData('maleData.txt')
        self.femaleData = self.readData('femaleData.txt')

        self.bmiChart = QLabel()
        
        #Categorias par el BMI
        self.categoryAdults = [[15.9,16.9,18.4,25,29.9,34.9,40.9,40.1],['Severe Thinness','Moderate Thinness','Mild Thinness','Normal','Overweight','Obese class l','Obese class ll','Obese class lll'],['#ff0000','#ff6666','#cccc00','#009933','#cccc00','#ff6666','#ff0000','#cc0000']]
        self.categoryChilds = [[4.9,85,95,95.1],['Underweight','Healthy Weight','At risk of overweight','Overweight'],['#ff9900','#009933','#cccc00','#ff0000']]
        
        self.tab = Tab()
        self.bmiTitle = QLabel("")
        self.bmiTitle.setStyleSheet("QLabel {font-size: 15px;}")

        self.bmiDetailsLabel = QLabel("Healthy BMI range:\nHealthy weight for the height:\nPonderal index:")
        self.bmiDetailsLabel.setStyleSheet("QLabel {font-size: 15px;}")

        self.calculate = QPushButton("Calculate")
        self.calculate.released.connect(self.setBMI)

        self.leftPanel = QWidget()
        self.leftPanel.setLayout(VLayout([self.tab,self.calculate]))
        self.leftPanel.setFixedSize(300,250)

        self.labelResultado = QLabel("  Result")
        self.labelResultado.setStyleSheet("font-weight: bold;background-color: rgb(51, 153, 51); font-size: 20px; color: white")
        self.labelResultado.setFixedWidth(600)
        self.labelResultado.setFixedHeight(35)
        self.infoLayout = VLayout(widgets = [self.labelResultado,self.bmiTitle,self.bmiChart,self.bmiDetailsLabel])
        self.rightPanel = QWidget()
        self.rightPanel.setLayout(self.infoLayout)

        self.mainWidget = QWidget()

        self.mainLayout = HLayout([self.leftPanel,self.rightPanel])
        self.mainWidget.setLayout(self.mainLayout)
        self.setCentralWidget(self.mainWidget)

        self.tab.tabBarClicked.connect(self.setBMI)
        self.setBMI()

    def drawBMIAdults(self,bmi): #Funcion para dibujar la barra y la linea en base al BMI
        self.bmiChart.setPixmap(QPixmap('barAdults.png'))
        painter = QtGui.QPainter(self.bmiChart.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor('gray'))
        painter.setPen(pen)
        font = QtGui.QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(20)
        painter.setFont(font)
        point = self.getPoint(180+((bmi-13.6)*6),[202,190],102) #Calculo para obtener la posicion de la linea en base al BMI
        painter.drawLine(202,190,point[0],point[1])
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        painter.drawText(160,150, 'BMI')
        painter.drawText(160,180, str(bmi))
        painter.end()

    def drawBMIChilds(self,bmi,percentile): #Funcion para dibujar la barra y la linea de la categoria de menores de edad
        percentile = int(percentile)
        self.bmiChart.setPixmap(QPixmap('barChilds.png'))
        painter = QtGui.QPainter(self.bmiChart.pixmap())
        pen = QtGui.QPen()
        pen.setWidth(3)
        pen.setColor(QtGui.QColor('gray'))
        painter.setPen(pen)
        font = QtGui.QFont()
        font.setFamily('Times')
        font.setBold(True)
        font.setPointSize(20)
        painter.setFont(font)
        degrees = None #Grados en base a porcentaje
        if percentile == 3:
            degrees = 180
        elif percentile == 5:
            degrees = 185
        elif percentile == 10:
            degrees = 195
        elif percentile == 25:
            degrees = 220
        elif percentile == 50:
            degrees = 270
        elif percentile == 75:
            degrees = 310
        elif percentile == 85:
            degrees = 335
        elif percentile == 90:
            degrees = 345
        elif percentile == 95:
            degrees = 355
        elif percentile == 97:
            degrees = 359

        point = self.getPoint(degrees,[202,190],102)
        painter.drawLine(202,190,point[0],point[1])
        pen.setColor(QtGui.QColor('black'))
        painter.setPen(pen)
        painter.drawText(160,150, 'BMI')
        painter.drawText(160,180, str(bmi))
        painter.end()

    def getPoint(self,degrees,origin,radius): #Formula para obtener un punto de una circunferencia
        x = radius * np.cos(degrees*0.0174533) + origin[0]
        y = radius * np.sin(degrees*0.0174533) + origin[1]
        return [round(x),round(y)]

    def readData(self,path): #Funcion para leer los porcentajes del BMI de menores de edad
        with open(path) as f:
            data = []
            while True:
                line = f.readline()
                if not line:
                    break
                data.append(line.strip())
        
        orderedData = []
        dictionary = {}
        percentiles = ('3','5','10','25','50','75','85','90','95','97')
        i = 0
        for x in data:
            dictionary[percentiles[i]] = float(x)
            if i == 9:
                i = 0
                orderedData.append(dictionary.copy())
                dictionary = {}
            else:
                i+=1
        return orderedData

    def setBMI(self): #Funcion para asignar todos los datos en los labels y pixmap
        data = self.tab.calculateData(self.maleData,self.femaleData)
        bmi = data[0]
        healthyRange = data[1][0]
        healthyBMIRange = data[1][1]
        texto = ''
        self.bmiTitle.setText('<b> BMI: '+str(round(bmi[0],1)) + ' kg/m\u00b2 </b>')
        category = None
        color = None

        if(len(bmi)>1):
            self.drawBMIChilds(round(bmi[0],1),bmi[1])
            self.bmiChart.setVisible(True)  
            for i in range(len(self.categoryChilds[0])):
                if float(bmi[1]) <= self.categoryChilds[0][i]:
                    category = self.categoryChilds[1][i]
                    color = self.categoryChilds[2][i]
                    break
            if category == None:
                category = self.categoryChilds[1][len(self.categoryChilds[1])-1] 
                color = self.categoryChilds[2][len(self.categoryChilds[2])-1] 
            self.bmiTitle.setText(self.bmiTitle.text() + ' (' + bmi[1] + '%, <b> <font color="' + color+ '">' + category +'</font> </b>)')
        else:
            if bmi[0] > 13.6 and bmi[0] < 44:
                self.drawBMIAdults(round(bmi[0],1))
                self.bmiChart.setVisible(True)
            else:
                self.bmiChart.setVisible(False)
            for i in range(len(self.categoryAdults[0])):
                if float(bmi[0]) <= self.categoryAdults[0][i]:
                    category = self.categoryAdults[1][i]
                    color = self.categoryAdults[2][i]
                    break
            if category == None:
               category = self.categoryAdults[1][len(self.categoryAdults[1])-1] 
               color = self.categoryAdults[2][len(self.categoryAdults[2])-1] 
            self.bmiTitle.setText(self.bmiTitle.text() + ' (' + '<b> <font color="' + color+ '">' + category +'</font> </b>)')

        texto = texto + ' \nHealthy BMI range: ' + healthyBMIRange[0] +'kg/m\u00b2 - ' + healthyBMIRange[1] + 'kg/m\u00b2'
        texto = texto + ' \nHealthy weight for the height: ' + str(healthyRange[0]) + ' ' + str(healthyRange[2]) + ' - ' + str(healthyRange[1]) + healthyRange[2]
        if self.tab.getWeight() < float(healthyRange[0]):
            texto = texto + '\nGain ' + str(round(float(healthyRange[0]) - self.tab.getWeight(),1)) + ' ' + healthyRange[2] + ' to reach a bmi of ' + healthyBMIRange[0] + 'kg/m\u00b2'
        elif self.tab.getWeight() > float(healthyRange[1]): 
            texto = texto + '\nLose ' + str(round(self.tab.getWeight() - float(healthyRange[1]),1)) + ' ' + healthyRange[2] + ' to reach a bmi of ' + healthyBMIRange[1] + 'kg/m\u00b2'
        texto = texto + '\nPonderal index: ' + data[2]
        self.bmiDetailsLabel.setText(texto)

app = QApplication(sys.argv)

window = MainWindow()
window.show()

app.exec()