from PyQt5.QtCore import QThreadPool

from PyQt5.QtWidgets import (QLabel, QPushButton, QTableWidgetItem, QMessageBox,
                             QMainWindow, QWidget, QTableWidget, QVBoxLayout,
                             QProgressBar, QHBoxLayout, QCheckBox, QHeaderView) 

from dobleSlider import DobleSlider
from datetime import datetime, timedelta
from threaded import Orderer
import requests
import ast


class Analisis(QMainWindow):
    #la fecha solo el dia
    sfecha = (datetime.today()+timedelta(days=1)).strftime('%Y%m%d')

    #conexion
    url = "http://soccerdatastats.com/empates/odds.php"

    payload={}
    headers = {
    'Authorization': 'Basic QUM4ODBCUzU4MTpBc1NhQTg5NjU=',
    'Cookie': '__cfduid=dd2dc08704f713cbbfeae0b535e0db2181607335654'
    }

    data = {}
    #para iniciar y reiniciar
    restart_values = [[2, 3.5], [2, 3.5], [0, 2],[-5,5]]

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
        self.difOdds     = QLabel("Diff_odds:      -5.0-5.0")

        self.ptajeBarODD1 = DobleSlider(700, 20, 0, 5, 0.2, self.odd1)
        self.ptajeBarODD2 = DobleSlider(700, 20, 0, 5, 0.2, self.odd2)
        self.ptajeBarUNDER25 = DobleSlider(700, 20, 0, 5, 0.2, self.odd_under25)
        self.ptajeDifOds = DobleSlider(700, 20, -5, 5, 0.2, self.difOdds)

        self.autoValue()

        #checkbox
        self.onlyToday = QCheckBox("Only Today")

        #boton
        self.cargar = QPushButton("Load/Refresh")
        self.cargar.clicked.connect(self.cargarMatches)
        self.reset = QPushButton("Reset")
        self.reset.clicked.connect(self.resetValues)
        self.default = QPushButton("Default")
        self.default.clicked.connect(self.defaultValues)

        #progres bar
        self.progressBar = QProgressBar()
        self.progressBar.hide()

        #tabla        
        self.matches = QLabel("Matches")
        self.matches.setStyleSheet("font-size: 18px; font-weight: bold;")
        self.partidos = QLabel("Partidos")
        self.partidosContador = 0
        self.datos = []
        
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels(["Fecha", "Hora", "Home", "Away", "Odds1", "OddsX", "Odds2", "OddsU25", "Diff Odds"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionsClickable(True)
        self.table.horizontalHeader().sectionClicked.connect(self.sortTable)

        #para ordenar
        self.threadpool = QThreadPool()

        #layout
        self.widget = QWidget()

        mainLayout = QVBoxLayout()
        machesLayou = QHBoxLayout()
        oddlayout = QHBoxLayout()
        buttsLayout = QHBoxLayout()

        machesLayou.addWidget(self.matches)
        machesLayou.addWidget(self.partidos)
        machesLayou.addStretch()
        machesLayou.addWidget(self.progressBar)

        oddlayout.addWidget(self.odds)
        oddlayout.addStretch()
        oddlayout.addWidget(self.lastDate)

        
        buttsLayout.addWidget(self.onlyToday)
        buttsLayout.addStretch()
        buttsLayout.addWidget(self.reset)
        buttsLayout.addWidget(self.default)

        mainLayout.addLayout(oddlayout)
        mainLayout.addWidget(self.odd1)
        mainLayout.addWidget(self.ptajeBarODD1)
        mainLayout.addWidget(self.odd2)
        mainLayout.addWidget(self.ptajeBarODD2)
        mainLayout.addWidget(self.odd_under25)
        mainLayout.addWidget(self.ptajeBarUNDER25)
        mainLayout.addWidget(self.difOdds)
        mainLayout.addWidget(self.ptajeDifOds)
        mainLayout.addLayout(buttsLayout)
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

        #bajamos los datos
        if len(self.data) <= 0:
            response = requests.request("GET", self.url, headers=self.headers, data=self.payload)
            self.data = ast.literal_eval(response.text)

        #filtramos
        self.datos = []
        fecha = ""
        if self.onlyToday.isChecked():
            fecha = self.sfecha[:4] + "-" + self.sfecha[4:6] + "-" + self.sfecha[6:]

        self.partidosContador = 0
        contador = 0
        for dato in self.data["data"]:
            isIn = True
            if not((self.ptajeBarODD1.getLessThanHandler() >= dato["odd1"] or self.ptajeBarODD1.isMaxLessHandler()) and 
               (self.ptajeBarODD1.getBigerThanHandler() <= dato["odd1"] or self.ptajeBarODD1.isLowest())):
                    isIn = False
            elif not((self.ptajeBarODD2.getLessThanHandler() >= dato["odd2"] or self.ptajeBarODD2.isMaxLessHandler()) and 
               (self.ptajeBarODD2.getBigerThanHandler() <= dato["odd2"] or self.ptajeBarODD2.isLowest())):
                    isIn = False
            elif not((self.ptajeBarUNDER25.getLessThanHandler() >= dato["oddU25"] or self.ptajeBarUNDER25.isMaxLessHandler()) and 
               (self.ptajeBarUNDER25.getBigerThanHandler() <= dato["oddU25"] or self.ptajeBarUNDER25.isLowest())):
                    isIn = False
            elif not((self.ptajeDifOds.getLessThanHandler() >= dato["difOdds"] or self.ptajeDifOds.isMaxLessHandler()) and 
               (self.ptajeDifOds.getBigerThanHandler() <= dato["difOdds"] or self.ptajeDifOds.isLowest())):
                    isIn = False

            if self.onlyToday.isChecked() and fecha != dato["fecha"]:
                isIn =False

            if isIn:
                lista = []
                lista.append(self.getDate(dato["fecha"]))
                lista.append(dato["hora"])
                lista.append(dato["home"])
                lista.append(dato["away"])
                lista.append(dato["odd1"])
                lista.append(dato["oddX"])
                lista.append(dato["odd2"])
                lista.append(dato["oddU25"])
                lista.append(dato["difOdds"])
                self.datos.append(lista)
                self.partidosContador += 1

            self.progressBar.setValue(contador/len(self.data["data"]))
            contador +=1

        self.partidos.setText("Partidos: " + str(self.partidosContador))

        #añadimos a la tabla
        self.popularLaTabla()

        self.cargar.setEnabled(True)
        self.progressBar.hide()
        self.cargar.setText("Load/Refresh")
        auxFecha = datetime.now()
        self.lastDate.setText("Last refresh: " + auxFecha.strftime("%H:%M:%S %d/%m/%y"))

    
    def changeSize(self):
        self.ptajeBarODD1.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeBarODD2.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeBarUNDER25.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)
        self.ptajeDifOds.resizeWidth( width = self.widget.width()/10*9, height = self.ptajeBarODD1.height)

    def resizeEvent(self, event):#sobreescribimos el metodo
        self.changeSize()
        QMainWindow.resizeEvent(self, event)

    def sortTable(self, sortingColumn):
        if len(self.datos) > 0:
            self.progressBar.setValue(0)
            self.progressBar.show()
            worker = Orderer(self.datos, sortingColumn)
            worker.signals.progress.connect(self.update_progress)
            worker.signals.finished.connect(self.endBar)
            self.threadpool.start(worker)
        
        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("There´s nothing to arrange")
            msg.setWindowTitle("Database empty")
            msg.exec_()


    def update_progress(self, progress):
        self.progressBar.setValue(progress)

    def endBar(self):
        self.progressBar.hide()
        self.table.clearContents()
    
        self.popularLaTabla()

    def popularLaTabla(self):
        self.table.setRowCount(len(self.datos))
        self.progressBar.setValue(0)
        fila = 0
        for dato in self.datos:
            self.table.setItem(fila, 0, QTableWidgetItem(dato[0]))
            self.table.setItem(fila, 1, QTableWidgetItem(dato[1]))
            self.table.setItem(fila, 2, QTableWidgetItem(dato[2]))
            self.table.setItem(fila, 3, QTableWidgetItem(dato[3]))
            self.table.setItem(fila, 4, QTableWidgetItem(str(round(dato[4], 3))))
            self.table.setItem(fila, 5, QTableWidgetItem(str(round(dato[5], 3))))
            self.table.setItem(fila, 6, QTableWidgetItem(str(round(dato[6], 3))))
            self.table.setItem(fila, 7, QTableWidgetItem(str(round(dato[7], 3))))
            self.table.setItem(fila, 8, QTableWidgetItem(str(round(dato[8], 3))))
            fila += 1
            self.progressBar.setValue(fila/len(self.datos))
            
    def getDate(self, fecha):
        return fecha[8:] + "/" + fecha[5:7] + "/" + fecha[:4]

    def autoValue(self):
        self.ptajeBarODD1.setBigerThanHandler(self.restart_values[0][0])
        self.ptajeBarODD1.setLessThanHandler(self.restart_values[0][1])
        self.ptajeBarODD2.setBigerThanHandler(self.restart_values[1][0])
        self.ptajeBarODD2.setLessThanHandler(self.restart_values[1][1])
        self.ptajeBarUNDER25.setBigerThanHandler(self.restart_values[2][0])
        self.ptajeBarUNDER25.setLessThanHandler(self.restart_values[2][1])
        self.ptajeDifOds.setBigerThanHandler(self.restart_values[3][0])
        self.ptajeDifOds.setLessThanHandler(self.restart_values[3][1])

    def defaultValues(self):
        self.autoValue()
        self.onlyToday.setChecked(False)
        self.cargarMatches()

    def resetValues(self):
        self.ptajeBarODD1.setBigerThanHandler(0)
        self.ptajeBarODD1.setLessThanHandler(5)
        self.ptajeBarODD2.setBigerThanHandler(0)
        self.ptajeBarODD2.setLessThanHandler(5)
        self.ptajeBarUNDER25.setBigerThanHandler(0)
        self.ptajeBarUNDER25.setLessThanHandler(5)
        self.ptajeDifOds.setBigerThanHandler(-5)
        self.ptajeDifOds.setLessThanHandler(5)
        self.onlyToday.setChecked(False)
        self.cargarMatches()
        