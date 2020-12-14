
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QHBoxLayout
from PyQt5.QtCore import QThreadPool
from threaded import GetTeams

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
        #widgets
        self.numberResuts = QLabel("Number of Resutls: ")
        self.plot = QPushButton("Plot")
        self.cant = QComboBox()
        self.cant.addItems(["5", "10", "15", "20", "35", "50"])
        self.cant.setItemData(0, 5)
        self.cant.setItemData(1, 10)
        self.cant.setItemData(2, 15)
        self.cant.setItemData(3, 20)
        self.cant.setItemData(4, 35)
        self.cant.setItemData(5, 50)

        #conections
        self.plot.clicked.connect(self.letsPlot)

        #otras variables
        self.datos = []
        self.fig = MplCanvas()

        #threadpool
        self.threadpool = QThreadPool()

        #Layouts
        widget = QWidget()
        top_layout = QHBoxLayout()
        main_layout = QVBoxLayout()

        top_layout.addStretch()
        top_layout.addWidget(self.numberResuts)
        top_layout.addWidget(self.cant)

        main_layout.addLayout(top_layout)
        main_layout.addWidget(self.plot)
        main_layout.addWidget(self.fig, stretch = 15)
                
        widget.setLayout(main_layout)
        self.setCentralWidget(widget)


    def letsPlot(self):
        worker = GetTeams()
        worker.signals.data.connect(self.theseAreTheLeagues)
        self.threadpool.start(worker)

    def theseAreTheLeagues(self, rawData):

        if len(self.datos) <= 0:
            numbers = []
            names = []
            for row in rawData:
                num = 0
                if row["LEAGUE_PLAYED"] != 0:
                    num = row["LEAGUE_DRAWS"] / row["LEAGUE_PLAYED"] * 100
                numbers.append(num)
                names.append(row["ID_LEAGUE"])

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
        self.fig.axes.barh(self.datos[1][:self.cant.itemData(self.cant.currentIndex())], self.datos[0][:self.cant.itemData(self.cant.currentIndex())])
        for p in self.fig.axes.patches:
            percentage = '{:.1f}%'.format(100 * p.get_width()/100)
            x = p.get_x() + p.get_width() + 0.02
            y = p.get_y() + p.get_height()/2
            self.fig.axes.annotate(percentage, (x, y))
        self.fig.draw()