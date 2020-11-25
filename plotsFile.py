
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize, QThreadPool, Qt
from threaded import GetTeams
from dobleSlider import DobleSlider

import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, self.axes = plt.subplots(figsize=(width, height))
        self.axes.set_xlabel("Draw %")
        self.axes.set_ylabel("Leagues")
        self.axes.invert_yaxis()
        super().__init__(fig)


class Plots(QMainWindow):
    def __init__(self):
        super().__init__()
        self.nonUselessLabel = QLabel("Porcentajes:   0-50%")
        self.margenDeEmpates = DobleSlider(1150, 35, 50, 0.5, self.nonUselessLabel)
        self.plot = QPushButton("Plot")
        self.clear = QPushButton("Clear")

        self.plot.clicked.connect(self.letsPlot)

        self.datos = []
        self.fig = MplCanvas()
        self.maxDatos = 15

        #threadpool
        self.threadpool = QThreadPool()

        #Layouts
        widget = QWidget()
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.nonUselessLabel)
        main_layout.addWidget(self.margenDeEmpates,stretch = 1)
        main_layout.addWidget(self.plot)
        main_layout.addWidget(self.fig, stretch = 10)
                
        widget.setLayout(main_layout)
        self.setMinimumSize(QSize(1200, 600))
        self.setCentralWidget(widget)


    def letsPlot(self):
        worker = GetTeams()
        worker.signals.data.connect(self.theseAreTheTeams)
        self.threadpool.start(worker)

    def theseAreTheTeams(self, rawData):

        if len(self.datos) <= 0:
            numbers = []
            names = []
            for row in rawData:
                num = row["HD"] + row["AD"]
                div = row["HW"] + row["HD"] + row["HL"] + row["AW"] + row["AD"] + row["AL"]
                if div != 0:
                    num = num / div * 100
                numbers.append(num)
                names.append(row["NAME"])

            self.datos.append(numbers)
            self.datos.append(names)

        for indice in range(len(self.datos[0])-1, 0, -1):
            for sorting in range(indice):
                if self.datos[0][indice] > self.datos[0][sorting]:
                    unoMas =[self.datos[0][indice], self.datos[1][indice]]
                    self.datos[0][indice] = self.datos[0][sorting]
                    self.datos[1][indice] = self.datos[1][sorting]
                    self.datos[0][sorting] = unoMas[0]
                    self.datos[1][sorting] = unoMas[1]

        self.fig.axes.cla()
        self.fig.axes.invert_yaxis()
        self.fig.axes.set_xlabel("Draw %")
        self.fig.axes.set_ylabel("Leagues")
        self.fig.axes.barh(self.datos[1][:self.maxDatos], self.datos[0][:self.maxDatos])
        self.fig.draw()