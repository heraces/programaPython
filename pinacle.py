from PyQt5.QtCore import QSize, Qt, QThreadPool, pyqtSignal, QDate

from PyQt5.QtWidgets import (QLabel, QPushButton, QStyle, QMessageBox, QTableWidgetItem,
                             QMainWindow, QSlider, QWidget, QTableWidget, QVBoxLayout,
                             QProgressBar, QHBoxLayout, QCheckBox, QHeaderView) 

from dobleSlider import DobleSlider
from datetime import datetime, timedelta
import http.client
import ast


class Analisis(QMainWindow):
    #la fecha solo el dia
    sfecha = (datetime.today()+timedelta(days=1)).strftime('%Y%m%d')

    #conexion
    conn = http.client.HTTPSConnection("api.ps3838.com")
    payload = ''
    headers = {
        'Authorization': 'Basic QUM4ODBCUzU4MTpBc1NhQTg5NjU=',
        'Cookie': '__cfduid=dd2dc08704f713cbbfeae0b535e0db2181607335654'
    }

    def __init__(self):
        super().__init__()

        #widgets odds
        self.odds = QLabel("Odds")
        self.odds.setStyleSheet("font-size: 16px; font-weight: bold;")

        #last date
        self.lastDate = QLabel("No researchs done")

        #doble sliders
        self.odd1        = QLabel("Odds1(home):     0.0-5.0")
        self.odd2        = QLabel("Odds2(away):     0.0-5.0")
        self.odd_under25 = QLabel("Odds_under 25:   0.0-5.0")
        self.difOdds     = QLabel("Diff_odds:      0.0-10.0")

        self.ptajeBarODD1 = DobleSlider(700, 20, 5, 0.2, self.odd1)
        self.ptajeBarODD2 = DobleSlider(700, 20, 5, 0.2, self.odd2)
        self.ptajeBarUNDER25 = DobleSlider(700, 20, 5, 0.2, self.odd_under25)
        self.ptajeDifOds = DobleSlider(700, 20, 10, 0.2, self.difOdds)

        self.onlyToday = QCheckBox("Only Today")
        #boton
        self.cargar = QPushButton("Load/Refresh")
        self.cargar.clicked.connect(self.cargarMatches)

        #progres bar
        self.progressBar = QProgressBar()
        self.progressBar.hide()

        #tabla        
        self.matches = QLabel("Matches")
        self.matches.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(["starts", "home", "away", "rotNum", "liveStatus", "status", "parlayRestriction"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        #layout
        self.widget = QWidget()

        mainLayout = QVBoxLayout()
        machesLayou = QHBoxLayout()
        oddlayout = QHBoxLayout()

        machesLayou.addWidget(self.matches)
        machesLayou.addWidget(self.progressBar)

        oddlayout.addWidget(self.odds)
        oddlayout.addStretch()
        oddlayout.addWidget(self.lastDate)

        mainLayout.addLayout(oddlayout)
        mainLayout.addWidget(self.odd1)
        mainLayout.addWidget(self.ptajeBarODD1)
        mainLayout.addWidget(self.odd2)
        mainLayout.addWidget(self.ptajeBarODD2)
        mainLayout.addWidget(self.odd_under25)
        mainLayout.addWidget(self.ptajeBarUNDER25)
        mainLayout.addWidget(self.difOdds)
        mainLayout.addWidget(self.ptajeDifOds)
        mainLayout.addWidget(self.onlyToday)
        mainLayout.addWidget(self.cargar)
        mainLayout.addLayout(machesLayou)
        mainLayout.addWidget(self.table)

        self.widget.setLayout(mainLayout)
        self.setCentralWidget(self.widget)


    def cargarMatches(self):
        self.cargar.setEnabled(False)
        self.cargar.setText("Loading...")
        self.progressBar.setValue(0)
        self.progressBar.show()

        self.conn.request("GET", "/v1/fixtures?sportId=29", self.payload, self.headers)
        res = self.conn.getresponse()
        data = res.read()

        datos = ast.literal_eval(data.decode("utf-8"))
        self.table.setRowCount(len(datos["league"]))
        fila = 0
        for dato in datos["league"]:
            for array in dato["events"]:
                    self.table.setItem(fila, 0, QTableWidgetItem(array["starts"]))
                    self.table.setItem(fila, 1, QTableWidgetItem(array["home"]))
                    self.table.setItem(fila, 2, QTableWidgetItem(array["away"]))
                    self.table.setItem(fila, 3, QTableWidgetItem(array["rotNum"]))
                    self.table.setItem(fila, 4, QTableWidgetItem(array["liveStatus"]))
                    self.table.setItem(fila, 5, QTableWidgetItem(array["status"]))
                    self.table.setItem(fila, 6, QTableWidgetItem(array["parlayRestriction"]))
                    fila += 1

        self.cargar.setEnabled(True)
        self.progressBar.hide()
        self.cargar.setText("Load/Refresh")
    
    def changeSize(self):
        self.ptajeBarODD1.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeBarODD2.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeBarUNDER25.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeDifOds.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)

    def resizeEvent(self, event):#sobreescribimos el metodo
        self.changeSize()
        QMainWindow.resizeEvent(self, event)