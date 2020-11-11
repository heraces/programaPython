from PyQt5.QtCore import QSize, Qt
from PyQt5.QtWidgets import (QLabel, QPushButton, QStyle, QProgressBar,
                             QMainWindow, QSlider, QWidget, QTableView, 
                             QVBoxLayout, QCheckBox, QHBoxLayout, QGridLayout)
                                                          
from PyQt5.QtGui import QIcon


class Predictions(QMainWindow):
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
        self.phd = QLabel("PHD:    0%")
        self.pad = QLabel("PAD:    0%")
        self.aplicar = QPushButton("Aplicar")
        self.save = QPushButton("Save/Load")
        self.ppghome = QLabel("PPGHome:   0")
        self.ppgaway = QLabel("PPGAway:   0")
        self.tgpg = QLabel("TGPG:    0")
        self.pjhome = QLabel("PJHome:   0")
        self.pjaway = QLabel("PJAway:    0")
        self.rempate = QLabel("REmpate:  0")

        self.binding = QPushButton("Binging")

        self.ptajeBarPGHD = QSlider(Qt.Horizontal)
        self.ptajeBarPGAD = QSlider(Qt.Horizontal)
        self.ptajeBarPHD = QSlider(Qt.Horizontal)
        self.ptajeBarPAD = QSlider(Qt.Horizontal)
        self.ptajeBarPPGHome = QSlider(Qt.Horizontal)
        self.ptajeBarPPGAway = QSlider(Qt.Horizontal)
        self.ptajeBarTGPG = QSlider(Qt.Horizontal)
        self.ptajeBarPJHome = QSlider(Qt.Horizontal)
        self.ptajeBarPJAway = QSlider(Qt.Horizontal)
        self.ptajeBarRempate = QSlider(Qt.Horizontal)

        self.progressBar = QProgressBar()
        self.progressBar.hide()
        self.progressBar.setFixedWidth(100)

        self.ptajeBarPGHD.setRange(0, 100)
        self.ptajeBarPGAD.setRange(0, 100)
        self.ptajeBarPHD.setRange(0, 100)
        self.ptajeBarPAD.setRange(0, 100)
        self.ptajeBarPPGHome.setRange(0, 10)
        self.ptajeBarPPGAway.setRange(0, 10)
        self.ptajeBarTGPG.setRange(0, 10)
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
        
        #Tabla
        self.table = QTableView()
        self.table.setSortingEnabled(True)
        self.table.horizontalHeader().setSectionsClickable(True)



        #create layouts
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
        topLayout.addWidget(self.save, 4, 4, 1, 1)
        topLayout.addWidget(self.binding, 0, 4, 1, 1)
        topLayout.addWidget(self.tgpg, 3, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarTGPG, 3, 1, 1, 1)
        topLayout.addWidget(self.ppghome, 4, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarPPGHome, 4, 1, 1, 1)
        topLayout.addWidget(self.ppgaway, 4, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPPGAway, 4, 3, 1, 1)
        topLayout.addWidget(self.pjhome, 5, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarPJHome, 5, 1, 1, 1)
        topLayout.addWidget(self.pjaway, 5, 2, 1, 1)
        topLayout.addWidget(self.ptajeBarPJAway, 5, 3, 1, 1)
        topLayout.addWidget(self.rempate, 6, 0, 1, 1)
        topLayout.addWidget(self.ptajeBarRempate, 6, 1, 1, 1)

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