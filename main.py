import sys

from filters import Filters
from PyQt5.QtCore import QSize, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QWidget, QTabWidget, QApplication, QStyle
from plotsFile import Plots
from predictions import Predictions

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_DesktopIcon")))
        globalWidgets = Filters()
        predictions = Predictions()
        plotlWidgets = Plots()

        widget = QTabWidget()
        widget.setWindowTitle("Football stuff")
        widget.setTabPosition(QTabWidget.North)
        widget.setMovable(False)
        
        widget.addTab(globalWidgets, "Backtesting")
        widget.addTab(predictions, "Partidos futuros")
        widget.addTab(plotlWidgets, "Plots")

        globalWidgets.filterValues.connect(predictions.copyingToPredictions)
        predictions.testingValues.connect(globalWidgets.copyingTofilters)

        self.setMinimumSize(QSize(1200, 700))
        self.setCentralWidget(widget)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()