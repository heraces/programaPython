
from PyQt5.QtWidgets import (QLabel, QPushButton, QInputDialog, QListWidget, QDialog, QAbstractItemView,
                            QVBoxLayout, QMessageBox, QHBoxLayout, QStyle)
from PyQt5.QtCore import QSize, pyqtSignal
import json

class SaveLeaguesDialog(QDialog):
    data = pyqtSignal(list)
    def __init__(self, leagues):
        super().__init__()
        self.leagues = leagues

        #labes tontas
        self.profileLabel = QLabel("Profile: ")
        self.leaguesLabel = QLabel("Leagues: ")

        #lsita para mostrar leagues guardadas
        self.showLeaguesList = QListWidget()

        #lista
        self.listProfiles = QListWidget()
        self.listProfiles.setGeometry(50, 70, 150, 60) 
        self.listProfiles.setSelectionMode(QAbstractItemView.SingleSelection)
        self.listProfiles.itemSelectionChanged.connect(self.showLeagues)
        
        #buttons         
        self.save = QPushButton("Save")
        self.save.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))
        self.load = QPushButton("Filter")
        self.add = QPushButton("Add")
        self.delete = QPushButton("Delete")
        self.delete.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogDiscardButton")))

        self.save.clicked.connect(self.saveData)
        self.load.clicked.connect(self.loadData)
        self.delete.clicked.connect(self.deleteSelected)
        self.add.clicked.connect(self.addProfile)
        self.actualizarLista()

        #layouts
        mainLayout = QVBoxLayout()
        settsLayout = QVBoxLayout()
        topLayout = QHBoxLayout()

        settsLayout.addWidget(self.save)
        settsLayout.addWidget(self.load)
        settsLayout.addStretch()
        settsLayout.addWidget(self.add)
        settsLayout.addStretch()
        settsLayout.addWidget(self.delete)

        topLayout.addWidget(self.listProfiles)
        topLayout.addLayout(settsLayout)

        mainLayout.addWidget(self.profileLabel)
        mainLayout.addLayout(topLayout)
        mainLayout.addWidget(self.leaguesLabel)
        mainLayout.addWidget(self.showLeaguesList)

        self.setLayout(mainLayout)
        self.setFixedSize(QSize(350, 400))

    def deleteSelected(self):
        if len(self.listProfiles.selectedItems()) > 0:
            data ={}
            with open('leaguesSaved.json', "r") as json_file:
                data = json.load(json_file)               
            
            data.pop(self.listProfiles.takeItem(self.listProfiles.row(self.listProfiles.currentItem())).text())

            with open('leaguesSaved.json', "w") as json_file:
                json.dump(data, json_file)
            
            self.actualizarLista()


    def addProfile(self):
            text, ok = QInputDialog.getText(self, 'Add profile', "Name your new profile:")
            if ok and text != "":
                try:
                    saveit = True
                    with open("leaguesSaved.json") as json_file:
                        data = json.load(json_file)
                        for d in data:
                            if d == text:
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Warning)
                                msg.setText("There´s already a profile with this name")
                                msg.setWindowTitle("Name already taken")
                                msg.exec_()
                                saveit = False 
                                break
                            
                    if saveit:
                        with open('leaguesSaved.json', "w") as json_file:
                            data[text] = []
                            json.dump(data, json_file)
                        self.actualizarLista()
                            
                except KeyError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Critical)
                    msg.setText("An error has occur")
                    msg.setWindowTitle("Error")
                    msg.exec_()
       
    def actualizarLista(self):    
        with open('leaguesSaved.json', "r") as json_file:
            try:
                self.listProfiles.clear()
                data = json.load(json_file)
                for d in data:
                    self.listProfiles.addItem(d)
            except:
                pass
    

    def saveData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            data ={}

            with open('leaguesSaved.json', "r") as json_file:
                data = json.load(json_file)

            data[self.listProfiles.currentItem().text()] = self.leagues
            with open('leaguesSaved.json', "w") as json_file:
                json.dump(data, json_file)
            
            self.actualizarLista()

    def loadData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            with open('leaguesSaved.json', "r") as json_file:
                self.data.emit(json.load(json_file)[self.listProfiles.currentItem().text()])

            self.close()

    def showLeagues(self):
        self.showLeaguesList.clear()
        with open('leaguesSaved.json', "r") as json_file:
            self.showLeaguesList.addItems(json.load(json_file)[self.listProfiles.currentItem().text()])
