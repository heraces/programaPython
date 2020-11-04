import pandas as pd
from PyQt5.QtCore import QSize, Qt, QThreadPool
from PyQt5.QtWidgets import (QLineEdit, QLabel, QPushButton,
                             QMainWindow, QSlider, QWidget, QTableView,
                             QVBoxLayout, QCheckBox, QHBoxLayout, QProgressBar,
                             QDoubleSpinBox, QTabWidget, QGridLayout)

from tableModel import TableModel
from saveLocalDatabaseFile import SaveDosPuntosTheClass
from externDatabase import Database
from threaded import Orderer, OrdererSignals


class Filters(QMainWindow):
    def __init__(self):
        super().__init__()
        #creates widgets
        globalWidgets = QWidget()
        globalWidgets.setWindowTitle("Backtesting")
        #widgets layout1
        self.filtros = QLabel("Filtros")
        self.filtros.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.pghd = QLabel("PGHD:  0%")
        self.pgad = QLabel("PGAD:  0%")
        self.phd = QLabel("PHD:   0%")
        self.pad = QLabel("PAD:   0%")
        self.ptajeBarPGHD = QSlider(Qt.Horizontal)
        self.ptajeBarPGAD = QSlider(Qt.Horizontal)
        self.ptajeBarPHD = QSlider(Qt.Horizontal)
        self.ptajeBarPAD = QSlider(Qt.Horizontal)
        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.aplicar = QPushButton("Aplicar")
        self.progressBar.setFixedWidth(100)


        self.ptajeBarPGHD.setRange(0, 100)
        self.ptajeBarPGHD.setSingleStep(.1)
        
        self.ptajeBarPGAD.setRange(0, 100)
        self.ptajeBarPGAD.setSingleStep(.1)
        
        self.ptajeBarPHD.setRange(0, 100)
        self.ptajeBarPHD.setSingleStep(.1)

        self.ptajeBarPAD.setRange(0, 100)
        self.ptajeBarPAD.setSingleStep(.1)

        #widgets layout2
        self.resultados = QLabel("Resultados")
        self.resultados.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.ptajeEmpates = QLabel("% de Empates")
        self.empates = QLabel("0 Empates")
        self.partidos = QLabel("0 Partidos")
        self.empatesNum = 0
        
        #Tabla
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionsClickable(True)

        #conectores
        self.ptajeBarPGHD.valueChanged.connect(self.actualizarPGHD)
        self.ptajeBarPGAD.valueChanged.connect(self.actualizarPGAD)
        self.ptajeBarPHD.valueChanged.connect(self.actualizarPHD)
        self.ptajeBarPAD.valueChanged.connect(self.actualizarPAD)
        self.aplicar.clicked.connect(self.aplicarResultado)
        self.table.horizontalHeader().sectionClicked.connect(self.sortTable)
        

        #databases y tal
        db = Database()

        rows = db.query("SELECT * FROM FIXTURES")
        self.teams = db.query("SELECT * FROM TEAMS ORDER BY ascii(ID) ASC")
        self.datos =[]

        for row in rows:   
            
            row["ID_HOME"] = self.findName(row["ID_HOME"])
            row["ID_AWAY"] = self.findName(row["ID_AWAY"])

            maRalla = []
            maRalla.append(self.getDate(row["DATE"]))
            maRalla.append(self.getTime(row["TIME"]))
            maRalla.append(row["ID_HOME"])
            maRalla.append(row["ID_AWAY"])
            maRalla.append(self.getTheGlobalHomePercentage(row))
            maRalla.append(self.getTheGlobalAwayPercentage(row))
            maRalla.append(self.getTheHomePercentage(row))
            maRalla.append(self.getTheAwayPercentage(row))
            maRalla.append(self.getResultado(row))

            self.datos.append(maRalla)

        self.currentDatos = self.datos
        self.listadeEmpates = []
        self.headers = ["Date", "Time", "Home team", "Away team", "PGHD", "PGAD", "PHD", "PAD", "Resultado"]
        self.getActualEmpates()
        self.data = pd.DataFrame(self.currentDatos, columns= self.headers) 
        self.partidos.setText(str(len(self.currentDatos))+ "Partidos")
        self.model = TableModel(self.data, self.listadeEmpates)
        self.table.setModel(self.model)


        #threads
        self.threadpool = QThreadPool()

        #creates layout
        layout = QVBoxLayout()
        topLayout = QGridLayout()
        midLayout = QGridLayout()
        
        topLayout.addWidget(self.filtros, 0, 0, 1, 1)
        topLayout.addWidget(self.pghd, 1, 0, 1, 1)
        topLayout.addWidget(self.pgad, 1, 2, 1, 1)
        topLayout.addWidget(self.phd, 2, 0, 1, 1)
        topLayout.addWidget(self.pad, 2, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPGHD, 1, 1, 1, 1)
        topLayout.addWidget(self.ptajeBarPGAD, 1, 3, 1, 1)
        topLayout.addWidget(self.ptajeBarPHD, 2, 1, 1, 1)
        topLayout.addWidget(self.ptajeBarPAD, 2, 3, 1, 1)
        topLayout.addWidget(self.progressBar, 1, 4, 1, 1)
        topLayout.addWidget(self.aplicar, 2, 4, 1, 1)
  
        midLayout.addWidget(self.resultados, 0, 0, 1, 1)
        midLayout.addWidget(self.ptajeEmpates, 1, 0, 1, 1)
        midLayout.addWidget(self.empates, 1, 1, 1, 1)
        midLayout.addWidget(self.partidos, 2, 1, 1, 1)

        layout.addLayout(topLayout)
        layout.addLayout(midLayout)
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

    def findName(self, targetID):
        primero = 0
        ultimo = len(self.teams)-1
        medio = int(ultimo/2)
        while primero <= ultimo:
            if targetID == self.teams[medio]["ID"]:
                return self.teams[medio]["NAME"]

            if targetID > self.teams[medio]["ID"]:
                primero = medio+1
            else:
                ultimo = medio-1
            medio = int((ultimo+primero)/2)
        return ""


    def getDate(self, fecha):
        return fecha[:4] + "/" + fecha[4:6] + "/" + fecha[6:]


    def getTime(self, fecha):
        while len(fecha) < 4:
             fecha = "0" + fecha
        return fecha[:2] + " : " + fecha[2:]


    def getTheGlobalHomePercentage(self, row):
        if row["HW"] + row["HD"]+ row["HL"] != 0:
            return round(row["HD"] / (row["HW"] + row["HD"]+ row["HL"]) * 100, 3)

        return "N/D"


    def getTheGlobalAwayPercentage(self, row):
        if row["AW"] + row["AD"]+ row["AL"] != 0:
            return round(row["AD"] / (row["AW"] + row["AD"]+ row["AL"]) * 100, 3)

        return "N/D"

    def getTheHomePercentage(self, row):
        if row["HHW"] + row["HHD"]+ row["HHL"] != 0:
            return round(row["HHD"] / (row["HHW"] + row["HHD"]+ row["HL"]) * 100, 3)

        return "N/D"

    def getTheAwayPercentage(self, row):
        if row["AAW"] + row["AAD"]+ row["AAL"] != 0:
            return round(row["AAD"] / (row["AAW"] + row["AAD"]+ row["AAL"])* 100, 3) 

        return "N/D"

    def getResultado(self, row):
        if row["FTHG"] < 0:
            return "N/D"
        return str(row["FTHG"]) + " - " + str(row["FTAG"])

    def getActualEmpates(self): 
        self.empatesNum = 0
        self.listadeEmpates = []
        for currentDato in self.currentDatos:
            if currentDato[-1] != "N/D":
                string1 = ""
                resultado = currentDato[-1]
                indice = 0
                while indice < len(resultado) and resultado[indice] != "-":
                    string1 = string1 + resultado[indice]
                    indice+=1

                if indice < len(resultado) and string1[:-1] == resultado[indice+2:]:
                    self.empatesNum +=1
                    self.listadeEmpates.append(True)
                else:
                    self.listadeEmpates.append(False)
            
            else:
                self.listadeEmpates.append(False)

        self.empates.setText(str(self.empatesNum) + " Empates")
        if(len(self.currentDatos) != 0):
            self.ptajeEmpates.setText(str(round(self.empatesNum/len(self.currentDatos) * 100, 2)) + "% de Empates")

    def aplicarResultado(self):
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
            
            if  isIn:
                self.currentDatos.append(elemento)
            
            if(contador%1500 == 0):
                self.progressBar.setValue(contador/len(self.datos))
            
        self.progressBar.hide()
        self.getActualEmpates()
        self.partidos.setText(str(len(self.currentDatos)) + " Partidos")
        self.data = pd.DataFrame(self.currentDatos, columns= self.headers) 
        self.model = TableModel(self.data, self.listadeEmpates)
        self.table.setModel(self.model)

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
        self.model = TableModel(self.data, self.listadeEmpates)
        self.table.setModel(self.model)
        self.getActualEmpates()

