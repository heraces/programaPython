
from PyQt5 import QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout
from PyQt5.QtGui import QPainter, QBrush, QPen
from PyQt5.QtCore import Qt, pyqtSlot
import sys
 
 
class DobleSlider(QWidget):
    def __init__(self, width, height, rango, interval):
        super().__init__()

        #tamaño del canas
        self.width = width
        self.height = height 
        self.range = rango
        self.interval = interval
        self.visualInterval = width/(rango/interval)

        print(self.visualInterval)
        #medidas del handle
        self.handleWidth = self.width/50
        self.handleHeight = self.height

        #pos del handler de la izquierda
        self.leftTop = 0
        self.leftLeft = 0

        #pos del handler de la derecha
        self.rigthTop = 0
        self.rigthLeft = self.width/100*98

        #letsumove
        self.letsuMove = False
        self.eselleft = False
        self.eselRigth = False

        #esto no se borra
        layout = QVBoxLayout()
        self.setLayout(layout)
        
 
    def paintEvent(self, e):
        #creamos el painter
        painter = QPainter(self)
        painter.setPen(QPen(Qt.gray, 1, Qt.SolidLine))
        painter.setBrush(QBrush(Qt.gray, Qt.SolidPattern))
        #pintamos en guion/rallita/rail
        painter.drawRect(self.width/100, self.height/5*2, self.width/100*99, self.height/5)
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
            

    def mouseReleaseEvent(self, event):
            self.letsuMove = False
            self.eselleft = False
            self.eselRigth = False

    def mouseMoveEvent(self, event): 
        if event.buttons() == Qt.LeftButton and self.letsuMove:
            if self.eselleft and event.x() >= 0 and event.x() + self.handleWidth < self.rigthLeft:
                self.leftLeft = event.x()
                return

            elif self.eselRigth and event.x() > self.rigthLeft + self.handleWidth and event.x() <= self.width-self.width/100*98: 
                self.rigthLeft = event.x()
                return

            self.paintEvent(self)
  