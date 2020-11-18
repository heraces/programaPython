from PyQt5.QtCore import QSize, Qt, pyqtSignal, QThreadPool
from PyQt5.QtWidgets import (QLabel, QPushButton, QStyle, QProgressBar, QMessageBox,
                             QMainWindow, QSlider, QWidget, QTableView, 
                             QVBoxLayout, QCheckBox, QHBoxLayout, QGridLayout)
                                                          
from PyQt5.QtGui import QIcon
from threaded import Orderer, ChargeDatabase
from localDatabase import SaveDialog
import pandas as pd
from dobleSlider import DobleSlider

class Predictions(QMainWindow):
    testingValues = pyqtSignal(list)
    def __init__(self):
        super().__init__()
        
        self.setStyleSheet("background-color: rgb(240,190,200)")

        #creates widgets
        globalWidgets = QWidget()
        globalWidgets.setWindowTitle("Backtesting")

        #widgets layout1
        self.filtros = QLabel("Filtros")
        self.filtros.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.pghd        = QLabel("PGHD:        0%")
        self.pgad        = QLabel("PGAD:        0%")
        self.phd         = QLabel("PHD:         0%")
        self.pad         = QLabel("PAD:         0%")
        self.ppghome     = QLabel("PPGHome:      0")
        self.ppgaway     = QLabel("PPGAway:      0")
        self.tgpg        = QLabel("TGPG:       0-5")
        self.pjhome      = QLabel("PJHome:       0")
        self.pjaway      = QLabel("PJAway:       0")
        self.rempate     = QLabel("REmpate:      0")
        self.odd1        = QLabel("ODD1:       0-10")
        self.odd2        = QLabel("ODD2:       0-10")
        self.odd_under25 = QLabel("UNDER25:    0-10")

        self.aplicar = QPushButton("Aplicar")
        self.save = QPushButton("Save/Load")
        self.save.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))
        self.binding = QPushButton("Copy to baktesting")
        self.binding.setIcon(self.style().standardIcon(getattr(QStyle, "SP_CommandLink")))
        self.reset = QPushButton("Reset")

        self.ptajeBarPGHD = QSlider(Qt.Horizontal)
        self.ptajeBarPGAD = QSlider(Qt.Horizontal)
        self.ptajeBarPHD = QSlider(Qt.Horizontal)
        self.ptajeBarPAD = QSlider(Qt.Horizontal)
        self.ptajeBarPPGHome = QSlider(Qt.Horizontal)
        self.ptajeBarPPGAway = QSlider(Qt.Horizontal)
        self.ptajeBarTGPG = DobleSlider(380, 20, 5, 0.2, self.tgpg)
        self.ptajeBarPJHome = QSlider(Qt.Horizontal)
        self.ptajeBarPJAway = QSlider(Qt.Horizontal)
        self.ptajeBarRempate = QSlider(Qt.Horizontal)
        self.ptajeBarODD1 = DobleSlider(380, 20, 10, 0.2, self.odd1)
        self.ptajeBarODD2 = DobleSlider(380, 20, 10, 0.2, self.odd2)
        self.ptajeBarUNDER25 = DobleSlider(380, 20, 10, 0.2, self.odd_under25)

        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.progressBar.setFixedWidth(100)

        self.ptajeBarPGHD.setRange(0, 100)
        self.ptajeBarPGAD.setRange(0, 100)
        self.ptajeBarPHD.setRange(0, 100)
        self.ptajeBarPAD.setRange(0, 100)
        self.ptajeBarPPGHome.setRange(0, 10)
        self.ptajeBarPPGAway.setRange(0, 10)
        self.ptajeBarPJAway.setRange(0, 50)
        self.ptajeBarPJHome.setRange(0, 50)
        self.ptajeBarRempate.setRange(0, 10)

        #widgets layout2
        self.resultados = QLabel("Resultados")
        self.resultados.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ptajeEmpates = QLabel("% de Empates")
        self.empates = QLabel("0 Empates")
        self.partidos = QLabel("0 Partidos")
        self.empatesNum = 0
        
        self.loadData = QPushButton("Load Data")

        #Tabla
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.setStyleSheet("background-color: rgb(255,235,230)")

        #databases y tal
        self.datos =[]
        self.currentDatos = self.datos
        self.listadeEmpates = []
        self.headers = ["Date", "Time", "Home team", "Away team", "PGHD", "PGAD", "PHD", "PAD",
             "Resultado", "TGPG", "PPGHome", "PPGAway", "PJHome", "PJAway", "REmpate", "ODD1", "ODD2", "ODD UNDER 25"]

        #threads
        self.threadpool = QThreadPool()

        #conectores
        self.ptajeBarPGHD.valueChanged.connect(self.actualizarPGHD)
        self.ptajeBarPGAD.valueChanged.connect(self.actualizarPGAD)
        self.ptajeBarPHD.valueChanged.connect(self.actualizarPHD)
        self.ptajeBarPAD.valueChanged.connect(self.actualizarPAD)
        self.ptajeBarPPGAway.valueChanged.connect(self.actualizarPPGAway)
        self.ptajeBarPPGHome.valueChanged.connect(self.actualizarPPGHome)
        self.ptajeBarPJAway.valueChanged.connect(self.actualizarPJAway)
        self.ptajeBarPJHome.valueChanged.connect(self.actualizarPJHome)
        self.ptajeBarRempate.valueChanged.connect(self.actualizarRempate)

        self.save.clicked.connect(self.guardarSetts)
        self.binding.clicked.connect(self.conectarConTablaAnterior)
        self.table.horizontalHeader().sectionClicked.connect(self.sortTable)
        self.loadData.clicked.connect(self.loadDatabase)
        self.aplicar.clicked.connect(self.aplicarResultado)
        self.reset.clicked.connect(self.resetThigs)

        #create layouts
        layout = QVBoxLayout()
        topLayout = QGridLayout()
        midLayout = QGridLayout()
        
        topLayout.addWidget(self.filtros, 0, 0, 1, 1)
        topLayout.addWidget(self.pghd, 1, 0, 1, 1)
        topLayout.addWidget(self.pgad, 2, 0, 1, 1)
        topLayout.addWidget(self.phd, 1, 2, 1, 1)
        topLayout.addWidget(self.pad, 2, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPGHD, 1, 1, 1, 1)
        topLayout.addWidget(self.ptajeBarPGAD, 2, 1, 1, 1)
        topLayout.addWidget(self.ptajeBarPHD, 1, 3, 1, 1)
        topLayout.addWidget(self.ptajeBarPAD, 2, 3, 1, 1)
        topLayout.addWidget(self.progressBar, 1, 4, 1, 1)
        topLayout.addWidget(self.aplicar, 4, 4, 1, 1)
        topLayout.addWidget(self.save, 6, 4, 1, 1)
        topLayout.addWidget(self.binding, 0, 4, 1, 1)
        topLayout.addWidget(self.tgpg, 3, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarTGPG, 3, 1, 1, 1)
        topLayout.addWidget(self.ppghome, 4, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarPPGHome, 4, 1, 1, 1)
        topLayout.addWidget(self.ppgaway, 5, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarPPGAway, 5, 1, 1, 1)
        topLayout.addWidget(self.pjhome, 4, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPJHome, 4, 3, 1, 1)
        topLayout.addWidget(self.pjaway, 5, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPJAway, 5, 3, 1, 1)
        topLayout.addWidget(self.rempate, 6, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarRempate, 6, 1, 1, 1)
        topLayout.addWidget(self.odd1, 7, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarODD1, 7, 1, 1, 1)
        topLayout.addWidget(self.odd2, 7, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarODD2, 7, 3, 1, 1)
        topLayout.addWidget(self.odd_under25, 8, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarUNDER25, 8, 1, 1, 1)
        topLayout.addWidget(self.reset, 8, 4, 1, 1)

        midLayout.addWidget(self.resultados, 0, 0, 1, 1)
        midLayout.addWidget(self.ptajeEmpates, 1, 0, 1, 1)
        midLayout.addWidget(self.empates, 1, 1, 1, 1)
        midLayout.addWidget(self.partidos, 2, 1, 1, 1)

        layout.addLayout(topLayout)
        layout.addLayout(midLayout)
        layout.addWidget(self.loadData)
        layout.addWidget(self.table)
        globalWidgets.setLayout(layout)
        
        self.setMinimumSize(QSize(1200, 600))
        self.setCentralWidget(globalWidgets)


    def actualizarPGHD(self):
        self.pghd.setText("PGHD:  {}%".format(self.ptajeBarPGHD.value()))
    
    def actualizarPGAD(self):
        self.pgad.setText("PGAD:  {}%".format(self.ptajeBarPGAD.value()))

    def actualizarPHD(self):
        self.phd.setText("PHD:   {}%".format(self.ptajeBarPHD.value()))

    def actualizarPAD(self):
        self.pad.setText("PAD:   {}%".format(self.ptajeBarPAD.value()))

    def actualizarPPGHome(self):
        if self.ptajeBarPPGHome.value() >= 10:
            self.ppghome.setText("PPGHome:   {}+".format(self.ptajeBarPPGHome.value()))
        else:
            self.ppghome.setText("PPGHome:   {}".format(self.ptajeBarPPGHome.value()))
    
    def actualizarPPGAway(self):
        if self.ptajeBarPPGAway.value() >= 10:
            self.ppgaway.setText("PPGAway:   {}+".format(self.ptajeBarPPGAway.value()))
        else:
            self.ppgaway.setText("PPGAway:   {}".format(self.ptajeBarPPGAway.value()))

        
    def actualizarPJHome(self):
        if self.ptajeBarPJHome.value() >= 50:
            self.pjhome.setText("PJHome:   {}+".format(self.ptajeBarPJHome.value()))
        else:
            self.pjhome.setText("PJHome:   {}".format(self.ptajeBarPJHome.value()))
    
    def actualizarPJAway(self):
        if self.ptajeBarPJAway.value() >= 50:
            self.pjaway.setText("PJAway:   {}+".format(self.ptajeBarPJAway.value()))
        else:
            self.pjaway.setText("PJAway:   {}".format(self.ptajeBarPJAway.value()))
    
    def actualizarRempate(self):
        if self.ptajeBarRempate.value() >= 10:
            self.rempate.setText("Rempate:   {}+".format(self.ptajeBarRempate.value()))
        else:
            self.rempate.setText("Rempate:   {}".format(self.ptajeBarRempate.value()))


    def sortTable(self, sortingColumn):
        self.progressBar.setValue(0)
        self.progressBar.show()
        worker = Orderer(self.currentDatos, sortingColumn)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.finished.connect(self.endBar)
        self.threadpool.start(worker)

    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def endBar(self):
        self.progressBar.hide()
        self.getActualEmpates()
        self.data = pd.DataFrame(self.currentDatos, columns= self.headers) 
        self.getActualEmpates()

    def guardarSetts(self):
        dlg = SaveDialog(self)
        dlg.setWindowTitle("Save/Load profile")
        dlg.exec_()


    def copyingToPredictions(self, esta):
        self.ptajeBarPGHD.setValue(esta[0])
        self.ptajeBarPGAD.setValue(esta[1])
        self.ptajeBarPHD.setValue(esta[2])
        self.ptajeBarPAD.setValue(esta[3])
        self.ptajeBarPPGHome.setValue(esta[4])
        self.ptajeBarPPGAway.setValue(esta[5])
        self.ptajeBarTGPG.setBigerThanHandler(esta[6][0])
        self.ptajeBarTGPG.setLessThanHandler(esta[6][1])
        self.ptajeBarPJHome.setValue(esta[7])
        self.ptajeBarPJAway.setValue(esta[8])
        self.ptajeBarRempate.setValue(esta[9])
        self.ptajeBarODD1.setBigerThanHandler(esta[10][0])
        self.ptajeBarODD1.setLessThanHandler(esta[10][1])
        self.ptajeBarODD2.setBigerThanHandler(esta[11][0])
        self.ptajeBarODD2.setLessThanHandler(esta[11][1])
        self.ptajeBarUNDER25.setBigerThanHandler(esta[12][0])
        self.ptajeBarUNDER25.setLessThanHandler(esta[12][1])

    def conectarConTablaAnterior(self):
        data = [self.ptajeBarPGHD.value(),
                        self.ptajeBarPGAD.value(),
                        self.ptajeBarPHD.value(),
                        self.ptajeBarPAD.value(),
                        self.ptajeBarPPGHome.value(),
                        self.ptajeBarPPGAway.value(),
                        self.ptajeBarTGPG.values(),
                        self.ptajeBarPJHome.value(),
                        self.ptajeBarPJAway.value(),
                        self.ptajeBarRempate.value(),
                        self.ptajeBarODD1.values(),
                        self.ptajeBarODD2.values(),
                        self.ptajeBarUNDER25.values()
                        ]
        self.testingValues.emit(data)

    def getActualEmpates(self): 
        self.empatesNum = 0
        self.listadeEmpates = []
        for currentDato in self.currentDatos:
            if currentDato[8] != "N/D":
                string1 = ""
                resultado = currentDato[8]
                indice = 0
                while indice < len(resultado) and resultado[indice] != "-":
                    string1 = string1 + resultado[indice]
                    indice+=1

                if indice < len(resultado) and string1[:-1] == resultado[indice+2:]:
                    self.empatesNum +=1
                    self.listadeEmpates.append(1)
                else:
                    self.listadeEmpates.append(2)
            
            else:
                self.listadeEmpates.append(0)

        self.empates.setText(str(self.empatesNum) + " Empates")
        if(len(self.currentDatos) != 0):
            self.ptajeEmpates.setText(str(round(self.empatesNum/len(self.currentDatos) * 100, 2)) + "% de Empates")

            
    def loadDatabase(self):
        self.loadData.setText("Loading...")
        self.progressBar.show()

        worker = ChargeDatabase("""SELECT ID_HOME, ID_AWAY, DATE, TIME, FTHG, FTAG, ODDS_1, ODDS_2, ODDS_UNDER25FT, 
                        HW, HD, HL, AW, AD, AL, GOALSGH, GOALSGA, GOALCGH, GOALCGA, REH, REA, REHH, REAA, HHW, HHD, HHL, AAW, AAL, AAD FROM FIXTURES WHERE FTHG = -1 or FTAG = -1""")
        worker.signals.progress.connect(self.update_progress)
        worker.signals.data.connect(self.loadedData)
        self.threadpool.start(worker)


    def loadedData(self, data):
        self.datos = data
        self.currentDatos = self.datos
        self.getActualEmpates()
        self.data = pd.DataFrame(self.currentDatos, columns= self.headers) 
        self.partidos.setText(str(len(self.currentDatos))+ "Partidos")

        self.progressBar.hide()
        self.loadData.setText("Load data")



        
    def aplicarResultado(self):
        if(len(self.datos) > 0):
            self.currentDatos = []
            isIn = True
            self.progressBar.setValue(0)
            self.progressBar.show()
            contador = 0
            for elemento in self.datos:
                contador+= 100
                isIn = True
                if not(self.ptajeBarPGHD.value() <= 0 or (isinstance(elemento[4], float) and elemento[4] >= self.ptajeBarPGHD.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPGAD.value() <= 0 or (isinstance(elemento[5], float) and elemento[5] >= self.ptajeBarPGAD.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPHD.value() <= 0 or (isinstance(elemento[6], float) and elemento[6] >= self.ptajeBarPHD.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPAD.value() <= 0 or (isinstance(elemento[7], float) and elemento[7] >= self.ptajeBarPAD.value())):
                    isIn = False

                if isIn and not(self.ptajeBarTGPG.value() <= 0 or (isinstance(elemento[9], float) and elemento[9] >= self.ptajeBarTGPG.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPPGHome.value() <= 0 or (isinstance(elemento[10], float) and elemento[10] >= self.ptajeBarPPGHome.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPPGAway.value() <= 0 or (isinstance(elemento[11], float) and elemento[11] >= self.ptajeBarPPGAway.value())):
                    isIn = False

                if isIn and not(self.ptajeBarPJHome.value() <= 0 or elemento[12] >= self.ptajeBarPJHome.value()):
                    isIn = False

                if isIn and not(self.ptajeBarPJAway.value() <= 0 or elemento[13] >= self.ptajeBarPJAway.value()):
                    isIn = False  
                
                if isIn and not(self.ptajeBarRempate.value() <= 0 or elemento[14] >= self.ptajeBarRempate.value()):
                    isIn = False

                if isIn and not(self.ptajeBarODD1.value() <= 0 or elemento[15] >= self.ptajeBarODD1.value()):
                    isIn = False

                if isIn and not(self.ptajeBarODD2.value() <= 0 or elemento[16] >= self.ptajeBarODD2.value()):
                    isIn = False  
                
                if isIn and not(self.ptajeBarUNDER25.value() <= 0 or elemento[17] >= self.ptajeBarUNDER25.value()):
                    isIn = False
                
                if  isIn:
                    self.currentDatos.append(elemento)
                
                if(contador%1500 == 0):
                    self.progressBar.setValue(contador/len(self.datos))
                
            self.progressBar.hide()
            self.getActualEmpates()
            self.partidos.setText(str(len(self.currentDatos)) + " Partidos")
            self.data = pd.DataFrame(self.currentDatos, columns= self.headers) 
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Try to load the database")
            msg.setWindowTitle("Database empty")
            msg.exec_()


    def resetThigs(self):
        self.ptajeBarPGHD.setValue(0)
        self.ptajeBarPGAD.setValue(0)
        self.ptajeBarPHD.setValue(0)
        self.ptajeBarPAD.setValue(0)
        self.ptajeBarPPGHome.setValue(0)
        self.ptajeBarPPGAway.setValue(0)
        self.ptajeBarTGPG.reset()
        self.ptajeBarPJHome.setValue(0)
        self.ptajeBarPJAway.setValue(0)
        self.ptajeBarRempate.setValue(0)
        self.ptajeBarODD1.reset()
        self.ptajeBarODD2.reset()
        self.ptajeBarUNDER25.reset()