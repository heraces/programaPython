
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt
 
 
class DobleSlider(QWidget):
    def __init__(self, width, height, start, end, interval, Label):
        super().__init__()

        #tamaño del canvas
        self.width = width
        self.height = height 

        #medidas del handle, rango y tal
        self.handleWidth = self.width/50
        self.handleHeight = self.height
        self.start = start
        self.range = end - start 
        self.interval = interval
        self.visualInterval = (self.width-self.handleWidth)/(self.range/self.interval)
        self.threshold = 0.2
        self.label = Label
        self.text = self.label.text()

        #pos del handler de la izquierda
        self.leftTop = 0
        self.leftLeft = 0
        self.leftPos = 0

        #pos del handler de la derecha
        self.rigthTop = 0
        self.rightPos = self.range/self.interval
        self.rigthLeft = self.rightPos * self.visualInterval

        #letsumove
        self.letsuMove = False
        self.eselleft = False
        self.eselRigth = False
        self.initPos = 0

        #editamos el texto al iniciar
        self.editText()

        #esto no se borra
        layout = QVBoxLayout()
        self.setLayout(layout)
        
 
    def paintEvent(self, e):
        #creamos el painter
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        #pintamos el guion/rallita/rail
        painter.drawRect(0, self.height/5*2, self.width, self.height/5)
        #cambiamos el color
        painter.setPen(QPen(Qt.blue, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.blue, Qt.SolidPattern))
        #pintamos anbos handlers
        painter.drawRect(self.leftLeft,  self.leftTop, self.handleWidth, self.handleHeight)
        painter.drawRect(self.rigthLeft,  self.rigthTop, self.handleWidth, self.handleHeight)

        painter.end()
        self.update()

    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton:
            #los mouse event me da pereza explicarlos
            if event.x() < self.leftLeft +self.handleWidth and self.leftLeft < event.x():
                self.eselleft = True
                self.letsuMove = True 
                return

            elif event.x() < self.rigthLeft + self.handleWidth and self.rigthLeft < event.x():
                self.eselRigth = True
                self.letsuMove = True 
                return

            self.initPos = event.x()
            

    def mouseReleaseEvent(self, event):
            self.letsuMove = False
            if self.eselleft:
                if event.x() - self.handleWidth/2 < 0:
                    self.leftPos = 0
                elif event.x() + self.handleWidth/2 > self.rigthLeft:
                    self.leftPos = self.rightPos - 1
                else:
                    self.leftPos = int(abs(self.initPos-event.x() - self.handleWidth/2)/self.visualInterval)
                self.leftLeft = self.leftPos * self.visualInterval
                self.eselleft = False
            elif self.eselRigth:
                if event.x() + self.handleWidth/2 >= self.width:
                    self.rightPos = self.range/self.interval
                elif event.x() - self.handleWidth/2 < self.leftLeft +self.handleWidth:
                    self.rightPos = self.leftPos + 1
                else:
                    self.rightPos = int(abs(self.initPos-event.x() - self.handleWidth/2)/self.visualInterval)
                self.rigthLeft = self.rightPos * self.visualInterval
                self.eselRigth = False

            self.initPos = 0
            self.editText()

    def mouseMoveEvent(self, event): 
        if event.buttons() == Qt.LeftButton and self.letsuMove:
            if self.eselleft and event.x()-self.handleWidth/2 >= 0 and event.x() + self.handleWidth/2 < self.rigthLeft:
                self.leftLeft = event.x()-self.handleWidth/2
                return

            elif self.eselRigth and event.x() - self.handleWidth/2 > self.leftLeft + self.handleWidth and event.x() + self.handleWidth/2 <= self.width: 
                self.rigthLeft = event.x()-self.handleWidth/2
                return

    # getters and setters de muchos tipos
    def getBigerThanHandler(self):
        return round(self.start + (self.leftPos * self.interval),3)

    def getLessThanHandler(self):
        return round(self.start + (self.rightPos * self.interval),3)


    def setBigerThanHandler(self, aux):
        if aux-self.start <= self.range:
            self.leftPos = int((aux-self.start)/ self.interval)
            self.leftLeft = self.leftPos * self.visualInterval
            self.editText()

    def setLessThanHandler(self, aux):
        if aux-self.start <= self.range:
            self.rightPos = int((aux-self.start) / self.interval)
            self.rigthLeft = self.rightPos * self.visualInterval
            self.editText()
    
    def values(self):
        return [self.start + self.leftPos * self.interval, self.start + self.rightPos * self.interval]

    def valuesToString(self):
        return str(round(self.start + (self.leftPos * self.interval),1)) + "-" + str(round(self.start + (self.rightPos * self.interval),1))

    def isMaxLessHandler(self):
        return self.range/self.interval <= self.rightPos

    def isLowest(self):
        return self.leftPos <= 0

    def reset(self):
        self.leftPos = 0
        self.rightPos = self.range/self.interval
        self.leftLeft = 0        
        self.rigthLeft = self.rightPos * self.visualInterval
        self.editText()

    def editText(self):
        aux = ""
        numero = 0
        while self.text[numero] != " ": # recorremos la cadena de texto del label hasta encontrar un espacio
            aux += self.text[numero]
            numero+=1

        result = self.valuesToString()
        if self.text[-1] == "%":
            result += "%"
        while len(aux) + len(result) < len(self.text): # ajustamos el resto de espacios
            aux += " "

        self.label.setText(aux + result)#añadimos el resultado al label

    def resizeWidth(self, width, height): #resize width para cuando quieres cambiar el width y el height
        self.width = width
        self.height = height
        self.handleWidth = self.width/50
        self.handleHeight = self.height
        self.visualInterval = (self.width-self.handleWidth)/(self.range/self.interval)
        self.rigthLeft = self.leftPos * self.visualInterval
        self.rigthLeft = self.rightPos * self.visualInterval