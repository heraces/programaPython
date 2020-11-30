import sys

from filters import Filters
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QTabWidget, QApplication, QStyle
from plotsFile import Plots
from predictions import Predictions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_DesktopIcon")))
        self.globalWidgets = Filters()
        self.predictions = Predictions()
        self.plotlWidgets = Plots()

        self.widget = QTabWidget()
        self.widget.setWindowTitle("Football stuff")
        self.widget.setTabPosition(QTabWidget.North)
        self.widget.setMovable(False)
        
        self.widget.addTab(self.globalWidgets, "Backtesting")
        self.widget.addTab(self.predictions, "Partidos futuros")
        self.widget.addTab(self.plotlWidgets, "Leagues Ratio")

        self.globalWidgets.filterValues.connect(self.predictions.copyingToPredictions)
        self.predictions.testingValues.connect(self.globalWidgets.copyingTofilters)

        self.widget.currentChanged.connect(self.justResize)

        self.setMinimumSize(QSize(1200, 700))
        self.setCentralWidget(self.widget)

    def justResize(self):
        if self.widget.currentIndex() == self.widget.indexOf(self.globalWidgets):
            self.globalWidgets.changeSize()
        elif self.widget.currentIndex() == self.widget.indexOf(self.predictions):
            self.predictions.changeSize()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()