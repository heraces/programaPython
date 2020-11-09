import sys

from filters import Filters
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QApplication
from plotsFile import Plots

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        globalWidgets = Filters()
        plotlWidgets = Plots()
        widget = QTabWidget()
        widget.setWindowTitle("Football stuff")
        widget.setTabPosition(QTabWidget.North)
        widget.setMovable(False)
        
        widget.addTab(globalWidgets, "Backtesting")
        widget.addTab(plotlWidgets, "Plots")
        
        self.setMinimumSize(QSize(1200, 700))
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()