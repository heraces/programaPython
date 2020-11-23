import pandas as pd
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt5.QtCore import QSize, QThreadPool, Qt
from  externDatabase import Database
from threaded import GetTeams
from dobleSlider import DobleSlider

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
        self.nonUselessLabel = QLabel("Porcentajes: 0-0%")
        self.margenDeEmpates = DobleSlider(1150, 35, 50, 1, self.nonUselessLabel)#esta feo, si
        self.plot = QPushButton("Plot")
        self.clear = QPushButton("Clear")

        self.plot.clicked.connect(self.letsPlot)

        #database
        self.database = Database()

        #threadpool
        self.threadpool = QThreadPool()

        self.sc = MplCanvas(self, width=5, height=4, dpi=100)
        self.sc.axes.plot([0, 1, 2, 3, 4], [10, 1, 20, 3, 40])

        #Layouts
        widget = QWidget()
        main_layout = QVBoxLayout()

        main_layout.addWidget(self.nonUselessLabel)
        main_layout.addWidget(self.margenDeEmpates)
        main_layout.addWidget(self.plot)
        main_layout.addWidget(self.sc)
                
        widget.setLayout(main_layout)
        self.setMinimumSize(QSize(1200, 600))
        self.setCentralWidget(widget)


    def letsPlot(self):
        worker = GetTeams()
        worker.signals.data.connect(self.theseAreTheTeams)
        self.threadpool.start(worker)

    def theseAreTheTeams(self, leagues):
        pass