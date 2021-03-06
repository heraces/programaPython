from PyQt5.QtWidgets import QVBoxLayout, QPushButton, QCheckBox, QDialog, QGridLayout, QScrollArea, QWidget, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal
from saveLeaguesDialog import SaveLeaguesDialog

class LeaguesDialog(QDialog):
    data = pyqtSignal(list)
    
    def __init__(self, leagues):
        super().__init__()
        #datos 
        self.maLeages = []
        leaguesAux = leagues #para ordenar la lista easy
        leaguesAux.sort()

        #widgets
        self.go = QPushButton("Filter")
        self.allCheck = QCheckBox("All Leagues")
        self.save = QPushButton("Save/load")
        self.save.clicked.connect(self.guardar)

        scrollarea = QScrollArea()
        scrollarea.setVerticalScrollBarPolicy( Qt.ScrollBarAlwaysOn )
        scrollarea.setWidgetResizable( True )
        
        widget = QWidget()
        scrollarea.setWidget(widget)

        leagues_layout = QGridLayout()
        widget.setLayout(leagues_layout)

        #rellenamos la main lista
        col = 0
        row = 0
        for league in leaguesAux:
            self.maLeages.append(QCheckBox(league))
            self.maLeages[-1].clicked.connect(self.setUpThaCheckboxes)
            leagues_layout.addWidget(self.maLeages[-1], row, col, 1, 1)

            col += 1
            if col%4 == 0:
                col = 0
                row +=1

        
        layout = QVBoxLayout()
        layout2 = QHBoxLayout()

        layout2.addWidget(self.allCheck)
        layout2.addStretch()
        layout2.addWidget(self.save)
        layout.addLayout(layout2)
        layout.addWidget(scrollarea)
        layout.addWidget(self.go)
        self.setLayout(layout) 

        self.go.clicked.connect(self.filter)
        self.allCheck.clicked.connect(self.setUpThaCheckboxesMaster)

    def setUpThaCheckboxes(self):
        aux = True
        for element in self.maLeages:
            if not element.isChecked():
                aux = False
                break
        if aux:
            self.allCheck.setChecked(True)
        else:
            self.allCheck.setChecked(False)


    def setUpThaCheckboxesMaster(self):
        for element in self.maLeages:
            element.setChecked(self.allCheck.isChecked())
        
    def filter(self):
        datos = []
        for league in self.maLeages:
            if league.isChecked():
                datos.append(league.text())
        self.close()
        self.data.emit(datos)

    def guardar(self):
        datos = []
        for league in self.maLeages:
            if league.isChecked():
                datos.append(league.text())

        dlg = SaveLeaguesDialog(datos)
        dlg.setWindowTitle("Save/Load profile")
        dlg.data.connect(self.actualizarDats)
        dlg.exec_()

    def actualizarDats(self, lista):
        self.data.emit(lista)
        self.close()