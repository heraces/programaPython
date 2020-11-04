
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot

class OrdererSignals(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()
    
class Orderer(QRunnable):
    def __init__(self, datos, columna):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = OrdererSignals()
        self.datos = datos
        self.sortingColumn = columna

    @pyqtSlot()
    def run(self):
        for indice in range(len(self.datos)-1, 0, -1):
            for sorting in range(indice):
                if self.sortingColumn <= 7 and self.sortingColumn >= 4:  
                    if (isinstance(self.datos[sorting][self.sortingColumn], float) and (isinstance(self.datos[indice][self.sortingColumn], str)
                            or self.datos[sorting][self.sortingColumn] > self.datos[indice][self.sortingColumn])):
                        line = self.datos[indice]
                        self.datos[indice] = self.datos[sorting]
                        self.datos[sorting] = line

                else:
                    if str(self.datos[sorting][self.sortingColumn]) > str(self.datos[indice][self.sortingColumn]):
                        line = self.datos[indice]
                        self.datos[indice] = self.datos[sorting]
                        self.datos[sorting] = line

            if(indice%100 == 0):
                self.signals.progress.emit(100-int(indice/len(self.datos) * 100))
            
        self.signals.finished.emit()