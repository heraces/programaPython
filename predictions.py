from PyQt5.QtCore import Qt, pyqtSignal, QThreadPool, QDate, QSize
from PyQt5.QtWidgets import (QLabel, QPushButton, QStyle, QProgressBar, QMessageBox, QHBoxLayout, QListWidget,
                             QMainWindow, QSlider, QWidget, QVBoxLayout, QGridLayout, QDateEdit)
                                                          
from PyQt5.QtGui import QColor
from threaded import Orderer, ChargeDatabase
from localDatabase import SaveDialog
from dobleSlider import DobleSlider
from leaguesDialog import LeaguesDialog
from maTable import CustomTableWidget
import time
from datetime import datetime, timedelta, date
import webbrowser

class Predictions(QMainWindow):
    testingValues = pyqtSignal(list)

    sfecha = (datetime.today()+timedelta(days=1)).strftime('%Y%m%d')
    chargestring = f"""SELECT ID_HOME, ID_AWAY, DATE, TIME, FTHG, FTAG, ODDS_1, ODDS_2, ODDS_UNDER25FT, 
                        HW, HD, HL, AW, AD, AL, GOALSGH, GOALSGA, GOALCGH, GOALCGA, REH, REA, REHH, REAA, HHW, HHD, HHL, 
                        AAW, AAL, AAD, ID_LEAGUE, ID FROM FIXTURES WHERE FTHG = -1 and FTAG = -1 and DATE >={sfecha} ORDER BY DATE, TIME"""

    style1 =  """QProgressBar {border-style: outset;
                           border-width: 2px;
                           border-color: #74c8ff;
                           border-radius: 9px;
                           border-width: 2px;
                           font-weight: bold;
                           color: black;}
                           QProgressBar::chunk:horizontal{ background: rgb(20,220,100);
                           border-radius: 9px;}"""    
                           
    #tamaño maximo de cada progressbar
    max_list = [0,0,0,0,0, 100, 100, 100, 100, 5, 3, 3, 50, 50, 10, 10, 10, 10, 10, 10, 10, 10]

    def __init__(self):
        super().__init__()

        #creates widgets
        predictions = QWidget()

        #widgets layout1
        #labels
        self.filtros = QLabel("Filtros")
        self.filtros.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.filterProfile = QLabel("-")
        self.filterProfile.setStyleSheet("font-size: 15px; font-weight: bold; color: gray")
        self.pghd        = QLabel("PGHD:          0%")
        self.pgad        = QLabel("PGAD:          0%")
        self.phd         = QLabel("PHD:           0%")
        self.pad         = QLabel("PAD:           0%")
        self.ppghome     = QLabel("PPGHome:  0.0-3.0")
        self.ppgaway     = QLabel("PPGAway:  0.0-3.0")
        self.tgpg        = QLabel("TGPG:     0.0-5.0")
        self.pjhome      = QLabel("PJHome:         0")
        self.pjaway      = QLabel("PJAway:         0")
        self.rempate     = QLabel("REmpate:        0")
        self.odd1        = QLabel("ODD1:    0.0-10.0")
        self.odd2        = QLabel("ODD2:    0.0-10.0")
        self.odd_under25 = QLabel("UNDER25: 0.0-10.0")

        #buttons
        self.aplicar = QPushButton("Aplicar")
        self.save = QPushButton("Save/Load")
        self.save.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))
        self.binding = QPushButton("Copy to baktesting")
        self.binding.setIcon(self.style().standardIcon(getattr(QStyle, "SP_CommandLink")))
        self.reset = QPushButton("Reset")
        self.setleagues = QPushButton("Arrange leagues")

        #ptajes
        self.ptajeBarPGHD = QSlider(Qt.Horizontal)
        self.ptajeBarPGAD = QSlider(Qt.Horizontal)
        self.ptajeBarPHD = QSlider(Qt.Horizontal)
        self.ptajeBarPAD = QSlider(Qt.Horizontal)
        self.ptajeBarPPGHome = DobleSlider(380, 20, 0, 3, 0.1, self.ppghome)
        self.ptajeBarPPGAway =DobleSlider(380, 20, 0, 3, 0.1, self.ppgaway)
        self.ptajeBarTGPG = DobleSlider(380, 20, 0, 5, 0.2, self.tgpg)
        self.ptajeBarPJHome = QSlider(Qt.Horizontal)
        self.ptajeBarPJAway = QSlider(Qt.Horizontal)
        self.ptajeBarRempate = QSlider(Qt.Horizontal)
        self.ptajeBarODD1 = DobleSlider(380, 20, 0, 10, 0.2, self.odd1)
        self.ptajeBarODD2 = DobleSlider(380, 20, 0, 10, 0.2, self.odd2)
        self.ptajeBarUNDER25 = DobleSlider(380, 20, 0, 10, 0.2, self.odd_under25)

        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.progressBar.setFixedWidth(100)

        self.ptajeBarPGHD.setRange(0, 100)
        self.ptajeBarPGAD.setRange(0, 100)
        self.ptajeBarPHD.setRange(0, 100)
        self.ptajeBarPAD.setRange(0, 100)
        self.ptajeBarPJAway.setRange(0, 50)
        self.ptajeBarPJHome.setRange(0, 50)
        self.ptajeBarRempate.setRange(0, 10)

        #fechas
        self.labelFrom = QLabel("Dates from: ")
        self.startDate = QDateEdit()
        self.startDate.setCalendarPopup(True)
        self.startDate.setMinimumDate(QDate(2010,1,1))
        self.startDate.setMaximumDate(QDate(2030,12,31))
        self.labelTo = QLabel("to: ")
        self.labelTo.setAlignment(Qt.AlignHCenter)
        self.endDate = QDateEdit()
        self.endDate.setCalendarPopup(True)
        self.endDate.setMinimumDate(QDate(2010,1,1))
        self.endDate.setMaximumDate(QDate(2030,12,31))

        #widgets layout2
        self.resultados = QLabel("Resultados")
        self.resultados.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ptajeEmpates = QLabel("% de Empates")
        self.empates = QLabel("0 Empates")
        self.partidos = QLabel("0 Partidos")
        self.empatesNum = 0
        
        self.usedLeagues = QListWidget()
        self.usedLeagues.setMaximumSize(QSize(400,50))
        self.usedLeagues.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        #Tabla
        self.loadData = QPushButton("Load Data")
        self.table = CustomTableWidget()
        self.table.progress.connect(self.update_progress)

        #databases y tal
        self.datos =[]
        self.currentDatos = self.datos
        self.listadeEmpates = []
        self.leagues = []
        self.activeLeagues =[]

        #threads
        self.threadpool = QThreadPool()

        #conectores
        self.ptajeBarPGHD.valueChanged.connect(self.actualizarPGHD)
        self.ptajeBarPGAD.valueChanged.connect(self.actualizarPGAD)
        self.ptajeBarPHD.valueChanged.connect(self.actualizarPHD)
        self.ptajeBarPAD.valueChanged.connect(self.actualizarPAD)
        self.ptajeBarPJAway.valueChanged.connect(self.actualizarPJAway)
        self.ptajeBarPJHome.valueChanged.connect(self.actualizarPJHome)
        self.ptajeBarRempate.valueChanged.connect(self.actualizarRempate)

        self.save.clicked.connect(self.guardarSetts)
        self.binding.clicked.connect(self.conectarConTablaAnterior)
        self.table.horizontalHeader().sectionClicked.connect(self.sortTable)
        self.table.secondTable.horizontalHeader().sectionClicked.connect(self.sortTable)
        self.table.verticalScrollBar().valueChanged.connect(self.printTheProgressBars)
        self.loadData.clicked.connect(self.loadDatabase)
        self.aplicar.clicked.connect(self.aplicarResultado)
        self.reset.clicked.connect(self.resetThigs)
        self.setleagues.clicked.connect(self.leagueDialog)
        self.table.secondTable.itemClicked.connect(self.openBrowser)

        self.startDate.dateChanged.connect(self.minorDate)
        self.endDate.dateChanged.connect(self.minorDate)

        #create layouts
        layout = QVBoxLayout()
        topLayout = QGridLayout()
        midLayout = QGridLayout()
        midLayout2 = QHBoxLayout()
        
        topLayout.addWidget(self.filtros, 0, 0, 1, 1)
        topLayout.addWidget(self.filterProfile, 0, 1, 1, 1)
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
        topLayout.addWidget(self.reset, 7, 4, 1, 1)
        topLayout.addWidget(self.setleagues, 9, 4, 1, 1)
        topLayout.addWidget(self.labelFrom, 9, 0, 1, 1)
        topLayout.addWidget(self.startDate, 9, 1, 1, 1)
        topLayout.addWidget(self.labelTo, 9, 2, 1, 1)
        topLayout.addWidget(self.endDate, 9, 3, 1, 1)

        midLayout.addWidget(self.resultados, 0, 0, 1, 1)
        midLayout.addWidget(self.ptajeEmpates, 1, 0, 1, 1)
        midLayout.addWidget(self.empates, 1, 1, 1, 1)
        midLayout.addWidget(self.partidos, 2, 1, 1, 1)

        midLayout2.addLayout(midLayout)
        midLayout2.addWidget(self.usedLeagues)

        layout.addLayout(topLayout)
        layout.addLayout(midLayout2)
        layout.addWidget(self.loadData)
        layout.addWidget(self.table)
        predictions.setLayout(layout)
        
        self.setCentralWidget(predictions)


    def actualizarPGHD(self):
        self.pghd.setText("PGHD:  {}%".format(self.ptajeBarPGHD.value()))
    
    def actualizarPGAD(self):
        self.pgad.setText("PGAD:  {}%".format(self.ptajeBarPGAD.value()))

    def actualizarPHD(self):
        self.phd.setText("PHD:   {}%".format(self.ptajeBarPHD.value()))

    def actualizarPAD(self):
        self.pad.setText("PAD:   {}%".format(self.ptajeBarPAD.value()))
        
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
        self.table.clearContents()

        self.table.setItems(self.currentDatos)
            
        self.getActualEmpates()
        self.printTheProgressBars()

    def guardarSetts(self):
        dlg = SaveDialog(self)
        dlg.setWindowTitle("Save/Load profile")
        dlg.exec_()


    def copyingToPredictions(self, esta):
        self.ptajeBarPGHD.setValue(esta[0])
        self.ptajeBarPGAD.setValue(esta[1])
        self.ptajeBarPHD.setValue(esta[2])
        self.ptajeBarPAD.setValue(esta[3])
        self.ptajeBarPPGHome.setBigerThanHandler(esta[4][0])
        self.ptajeBarPPGHome.setLessThanHandler(esta[4][1])
        self.ptajeBarPPGAway.setBigerThanHandler(esta[5][0])
        self.ptajeBarPPGAway.setLessThanHandler(esta[5][1])
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
                        self.ptajeBarPPGHome.values(),
                        self.ptajeBarPPGAway.values(),
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
        row = 0
        while row < self.table.rowCount():
            if self.currentDatos[row][4] != "N/D":
                string1 = ""
                resultado = self.currentDatos[row][4]
                indice = 0
                while indice < len(resultado) and resultado[indice] != "-":
                    string1 = string1 + resultado[indice]
                    indice+=1

                if indice < len(resultado) and string1[:-1] == resultado[indice+2:]:
                        
                    self.listadeEmpates.append(1)
                    self.empatesNum += 1
                else:

                    self.listadeEmpates.append(2)
            else:
                
                self.listadeEmpates.append(0)

            row +=1

        self.empates.setText(str(self.empatesNum) + " Empates")
        if(len(self.currentDatos) != 0):
            self.ptajeEmpates.setText(str(round(self.empatesNum/len(self.currentDatos) * 100, 2)) + "% de Empates")
        
        self.printTheProgressBars()

            
    def loadDatabase(self):
        self.loadData.setText("Loading...")
        self.loadData.setEnabled(False)
        self.progressBar.setValue(0)
        self.progressBar.show()

        worker = ChargeDatabase(self.chargestring)
        worker.signals.progress.connect(self.update_progress)
        worker.signals.data.connect(self.loadedData)
        self.threadpool.start(worker)


    def loadedData(self, data):
        self.datos = data[0]
        self.currentDatos = self.datos
        self.table.setItems(self.currentDatos)
        self.leagues = data[3]

        #ajustamos los handlers de fecha
        self.startDate.setMinimumDate(QDate(int(data[1][:4]), int(data[1][4:6]), int(data[1][6:])))
        self.endDate.setDate(QDate(int(data[2][:4]), int(data[2][4:6]), int(data[2][6:])))
        self.startDate.setDate(QDate(int(data[1][:4]), int(data[1][4:6]), int(data[1][6:])))
        self.endDate.setMinimumDate(self.startDate.date())
        self.startDate.setMaximumDate(self.endDate.date())
        self.endDate.setMaximumDate(QDate(int(data[2][:4]), int(data[2][4:6]), int(data[2][6:])))
        self.progressBar.hide()
        self.loadData.setText("Load data")
        self.getActualEmpates()
        self.partidos.setText(str(len(self.currentDatos)) + " Partidos")
        self.progressBar.hide()


    def printTheProgressBars(self):

        if len(self.currentDatos) > 0:
            fila = self.table.rowAt(0)
            end = self.table.rowAt(self.table.height())
            if end <= 0:
                end = self.table.rowCount()-1

            while fila >= 0 and fila <= end: 
                for col in range( self.table.columnCount()):
                    if isinstance(self.currentDatos[fila][col], float) or isinstance(self.currentDatos[fila][col], int):
                        bar1 = QProgressBar()
                        bar1.setTextVisible(True)
                        bar1.setMaximum(self.max_list[col])
                        if(self.currentDatos[fila][col] > bar1.maximum()):
                            bar1.setMaximum(self.currentDatos[fila][col])
                        bar1.setValue(self.currentDatos[fila][col])
                        bar1.setFormat(str(self.currentDatos[fila][col]))
                        bar1.setAlignment(Qt.AlignCenter)
                        self.table.setCellWidget(fila, col, bar1)
                        bar1.setStyleSheet(self.style1)

                fila +=1

        
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
                if not(len(self.activeLeagues) <= 0 or elemento[21] in self.activeLeagues):
                    isIn = False
                elif not(self.startDate.date() <= self.toDate(elemento[0]) and self.endDate.date() >= self.toDate(elemento[0])):
                    isIn = False
                elif not(self.ptajeBarPGHD.value() <= 0 or (isinstance(elemento[5], float) and elemento[5] >= self.ptajeBarPGHD.value())):
                    isIn = False

                elif not(self.ptajeBarPGAD.value() <= 0 or (isinstance(elemento[6], float) and elemento[6] >= self.ptajeBarPGAD.value())):
                    isIn = False

                elif not(self.ptajeBarPHD.value() <= 0 or (isinstance(elemento[7], float) and elemento[7] >= self.ptajeBarPHD.value())):
                    isIn = False

                elif not(self.ptajeBarPAD.value() <= 0 or (isinstance(elemento[8], float) and elemento[8] >= self.ptajeBarPAD.value())):
                    isIn = False

                elif not((self.ptajeBarTGPG.getBigerThanHandler() <= 0 and (isinstance(elemento[9], str))) or (
                                (isinstance(elemento[9], float) and elemento[9] >= self.ptajeBarTGPG.getBigerThanHandler()
                                and self.ptajeBarTGPG.getLessThanHandler() >= elemento[9]))):
                    isIn = False

                elif not((self.ptajeBarPPGHome.getBigerThanHandler() <= 0 and (isinstance(elemento[9], str))) or (
                                 (isinstance(elemento[9], float) and elemento[9] >= self.ptajeBarPPGHome.getBigerThanHandler()
                                 and (self.ptajeBarPPGHome.getLessThanHandler() >= elemento[9] or self.ptajeBarPPGHome.isMaxLessHandler())))):
                    isIn = False
                elif not((self.ptajeBarPPGAway.getBigerThanHandler() <= 0 and (isinstance(elemento[9], str))) or (
                                 (isinstance(elemento[9], float) and elemento[9] >= self.ptajeBarPPGAway.getBigerThanHandler()
                                 and (self.ptajeBarPPGAway.getLessThanHandler() >= elemento[9] or self.ptajeBarPPGAway.isMaxLessHandler())))):
                    isIn = False

                elif not(self.ptajeBarPJHome.value() <= 0 or elemento[12] >= self.ptajeBarPJHome.value()):
                    isIn = False

                elif isIn and not(self.ptajeBarPJAway.value() <= 0 or elemento[13] >= self.ptajeBarPJAway.value()):
                    isIn = False  
                
                elif not(self.ptajeBarRempate.value() <= 0 or elemento[14]+elemento[15]+elemento[16]+elemento[17] >= self.ptajeBarRempate.value()):
                    isIn = False

                elif not((self.ptajeBarODD1.getBigerThanHandler() <= 0 and (isinstance(elemento[18], str))) or (
                                    (isinstance(elemento[18], float) and elemento[18] >= self.ptajeBarODD1.getBigerThanHandler()
                                    and self.ptajeBarODD1.getLessThanHandler() >= elemento[18]))):
                    isIn = False

                elif not((self.ptajeBarODD2.getBigerThanHandler() <= 0 and (isinstance(elemento[19], str))) or (
                                    (isinstance(elemento[19], float) and elemento[19] >= self.ptajeBarODD2.getBigerThanHandler()
                                    and self.ptajeBarODD2.getLessThanHandler() >= elemento[19]))):
                    isIn = False  
                
                elif not((self.ptajeBarUNDER25.getBigerThanHandler() <= 0 and (isinstance(elemento[20], str))) or (
                                    (isinstance(elemento[20], float) and elemento[20] >= self.ptajeBarUNDER25.getBigerThanHandler()
                                    and self.ptajeBarUNDER25.getLessThanHandler() >= elemento[20]))):
                    isIn = False
                
                if  isIn:
                    self.currentDatos.append(elemento)
                
                if(contador%3000 == 0):
                    self.progressBar.setValue(contador/len(self.datos))
                
            self.progressBar.hide()
            self.partidos.setText(str(len(self.currentDatos)) + " Partidos")
            self.table.clearContents()
            
            self.table.setItems(self.currentDatos)
                
            self.getActualEmpates()
            self.printTheProgressBars()
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
        self.ptajeBarPPGHome.reset()
        self.ptajeBarPPGAway.reset()
        self.ptajeBarTGPG.reset()
        self.ptajeBarPJHome.setValue(0)
        self.ptajeBarPJAway.setValue(0)
        self.ptajeBarRempate.setValue(0)
        self.ptajeBarODD1.reset()
        self.ptajeBarODD2.reset()
        self.ptajeBarUNDER25.reset()
        
        self.activeLeagues = []
        self.usedLeagues.clear()
        
        self.startDate.setDate(self.startDate.minimumDate())
        self.endDate.setDate(self.startDate.maximumDate())

    def resizeEvent(self, event):#sobreescribimos el metodo
        self.printTheProgressBars()
        self.changeSize()
        QMainWindow.resizeEvent(self, event)

    def changeSize(self):
        self.ptajeBarODD1.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())
        self.ptajeBarODD2.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())
        self.ptajeBarUNDER25.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())
        self.ptajeBarTGPG.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())
        self.ptajeBarPPGHome.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())
        self.ptajeBarPPGAway.resizeWidth( width = self.ptajeBarPJAway.width(), height = self.ptajeBarPJAway.height())

    def toDate(self, elemento):
        return QDate(int(elemento[-4:]), int(elemento[3:5]), int( elemento[:2]))

    def minorDate(self):
        self.endDate.setMinimumDate(self.startDate.date())
        self.startDate.setMaximumDate(self.endDate.date())

    def leagueDialog(self):
        if len(self.leagues) > 0:
            dlg = LeaguesDialog(self.leagues)
            dlg.setWindowTitle(" Leagues Shown")
            dlg.data.connect(self.printe)
            dlg.exec_()
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("Try to load the database")
            msg.setWindowTitle("Database empty")
            msg.exec_()

    def printe(self, dats):
        self.activeLeagues = dats
        self.usedLeagues.clear()
        self.usedLeagues.addItems(self.activeLeagues)
        self.aplicarResultado()

    def openBrowser(self, item):
        if self.table.secondTable.column(item) == 0:
            webbrowser.open(
                f"https://www.flashscore.com/match/{self.currentDatos[self.table.secondTable.row(item)][-1]}/#match-summary",
                 new=2, autoraise=True)