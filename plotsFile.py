import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout
from PyQt5.QtCore import QSize
from  externDatabase import Database

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure

matplotlib.use("Qt5Agg")

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super().__init__(fig)


class Plots(QMainWindow):
    def __init__(self):
        super().__init__()
        self.listXLine = QLineEdit()
        self.listYLine = QLineEdit()
        self.plot = QPushButton("Plot")
        self.clear = QPushButton("Clear")
        self.listYViewer = QLineEdit()
        self.listXViewer = QLineEdit()
        self.listX = []
        self.listY = []

        self.listXViewer.setEnabled(False)
        self.listYViewer.setEnabled(False)
        
        self.listXLine.returnPressed.connect(self.addToListX)
        self.listYLine.returnPressed.connect(self.addToListY)
        self.plot.clicked.connect(self.letsPlot)
        self.clear.clicked.connect(self.vaciar)

        #database
        self.database = Database()


        widget = QWidget()
        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        #Layouts
        main_layout = QVBoxLayout()
        unLayout = QGridLayout()
        
        unLayout.addWidget(self.listXLine, 0, 0, 1,1)
        unLayout.addWidget(self.plot, 0, 1, 1, 1)
        unLayout.addWidget(self.listYLine,0, 2, 1, 1)
        unLayout.addWidget(self.listXViewer, 1, 0, 1, 1)
        unLayout.addWidget(self.listYViewer,1, 2, 1, 1)
        unLayout.addWidget(self.clear,1, 1, 1, 1)


        main_layout.addLayout(unLayout)
        main_layout.addWidget(self.sc)
                
        widget.setLayout(main_layout)
        self.setMinimumSize(QSize(850, 600))
        self.setCentralWidget(widget)

    def addToListX(self):
        try:
            self.listX.append(int(self.listXLine.text()))
            self.listXLine.clear()
            name = ""
            for item in self.listX:
                name += str(item) + ", "
            self.listXViewer.setText(name[:-2])
        except Exception:
            self.listXLine.clear()

    def addToListY(self):
        try:
            self.listY.append(int(self.listYLine.text()))
            self.listYLine.clear()
            name = ""
            for item in self.listY:
                name += str(item) + ", "
            self.listYViewer.setText(name[:-2])
        except Exception:
            self.listYLine.clear()

    def letsPlot(self):
        self.sc.axes.cla()
        if len(self.listY) > 0:
            listaY =[]
            for i in range(len(self.listY)):
                listaY.append(i)
            df = pd.DataFrame(self.listY, listaY)
            df.plot(ax = self.sc.axes)
            self.sc.draw()
        
        if len(self.listX) >0:
            listaX =[]
            for i in range(len(self.listX)):
                listaX.append(i)

            df = pd.DataFrame(self.listX, listaX)
            df.plot(ax = self.sc.axes)
            self.sc.draw()

    def vaciar(self):
        self.listX = []
        self.listY = []
        self.listXViewer.setText("")
        self.listYViewer.setText("")