from PyQt5.QtWidgets import (QDialog, QWidget, QLabel, QLineEdit, QListView, QPushButton, QProgressBar, QInputDialog,
            QCheckBox, QListWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout, QStyle)
from PyQt5.QtCore import QSize, Qt

from PyQt5.QtGui import QIcon

import json

#clase para guardar en la database local
class SaveDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        #referencia a Filters
        self.maninWindow =  mainWindow
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))
        self.setStyleSheet("QProgressBar "
                          "{"
                                "height: 5px;"
                          "}")

        # actual labels
        self.actual = QLabel("Actual Data")
        self.pghd = QLabel("PGHD:")
        self.pgad = QLabel("PGAD:")
        self.phd = QLabel("PHD: ")
        self.pad = QLabel("PAD: ")
        self.ppghome = QLabel("PPGHome:")
        self.ppgaway = QLabel("PPGAway:")
        self.tgpg = QLabel("TGPG:")
        self.pjhome = QLabel("PJHome:")
        self.pjaway = QLabel("PJAway:")
        self.rempate = QLabel("REmpate:")
        self.odd1 = QLabel("ODD1:")
        self.odd2 = QLabel("ODD2:")
        self.odd_under25 = QLabel("UNDER25:")

        # actual progresbar
        self.ptajeBarPGHD = QProgressBar()
        self.ptajeBarPGHD.setTextVisible(False)
        self.ptajeBarPGHD.setFixedWidth(150)

        self.ptajeBarPGAD = QProgressBar()
        self.ptajeBarPGAD.setTextVisible(False)
        self.ptajeBarPGAD.setFixedWidth(150)

        self.ptajeBarPHD = QProgressBar()
        self.ptajeBarPHD.setTextVisible(False)
        self.ptajeBarPHD.setFixedWidth(150)

        self.ptajeBarPAD = QProgressBar()
        self.ptajeBarPAD.setTextVisible(False)
        self.ptajeBarPAD.setFixedWidth(150)

        self.ptajeBarPPGHome = QProgressBar()
        self.ptajeBarPPGHome.setTextVisible(False)
        self.ptajeBarPPGHome.setFixedWidth(150)

        self.ptajeBarPPGAway = QProgressBar()
        self.ptajeBarPPGAway.setTextVisible(False)
        self.ptajeBarPPGAway.setFixedWidth(150)
        

        self.ptajeBarTGPG = QProgressBar()
        self.ptajeBarTGPG.setTextVisible(False)
        self.ptajeBarTGPG.setFixedWidth(150)

        self.ptajeBarPJHome = QProgressBar()
        self.ptajeBarPJHome.setTextVisible(False)
        self.ptajeBarPJHome.setFixedWidth(150)

        self.ptajeBarPJAway = QProgressBar()
        self.ptajeBarPJAway.setTextVisible(False)
        self.ptajeBarPJAway.setFixedWidth(150)

        self.ptajeBarRempate = QProgressBar()
        self.ptajeBarRempate.setTextVisible(False)
        self.ptajeBarRempate.setFixedWidth(150)

        self.ptajeBarODDS1 = QProgressBar()
        self.ptajeBarODDS1.setTextVisible(False)
        self.ptajeBarODDS1.setFixedWidth(150)

        self.ptajeBarODDS2 = QProgressBar()
        self.ptajeBarODDS2.setTextVisible(False)
        self.ptajeBarODDS2.setFixedWidth(150)
        
        self.ptajeBarODDS_UNDER25 = QProgressBar()
        self.ptajeBarODDS_UNDER25.setTextVisible(False)
        self.ptajeBarODDS_UNDER25.setFixedWidth(150)

        self.setCurrentBars()

        #saved data
        self.ssavedData = QLabel("Saved Data:")
        self.spghd = QLabel("|")
        self.spgad = QLabel("|")
        self.sphd = QLabel("|")
        self.spad = QLabel("|")
        self.sppghome = QLabel("|")
        self.sppgaway = QLabel("|")
        self.stgpg = QLabel("|")
        self.spjhome = QLabel("|")
        self.spjaway = QLabel("|")
        self.srempate = QLabel("|")
        self.sodd1 = QLabel("|")
        self.sodd2 = QLabel("|")
        self.sodd_under25 = QLabel("|")

        #saved progressbar

        self.savedptajeBarPGHD = QProgressBar()
        self.savedptajeBarPGHD.setFixedWidth(150)
        self.savedptajeBarPGHD.setTextVisible(False)
        self.savedptajeBarPGHD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarPGAD = QProgressBar()
        self.savedptajeBarPGAD.setFixedWidth(150)
        self.savedptajeBarPGAD.setTextVisible(False)
        self.savedptajeBarPGAD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPHD = QProgressBar()
        self.savedptajeBarPHD.setFixedWidth(150)
        self.savedptajeBarPHD.setTextVisible(False)
        self.savedptajeBarPHD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPAD = QProgressBar()
        self.savedptajeBarPAD.setFixedWidth(150)
        self.savedptajeBarPAD.setTextVisible(False)
        self.savedptajeBarPAD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarPPGHome = QProgressBar()
        self.savedptajeBarPPGHome.setFixedWidth(150)
        self.savedptajeBarPPGHome.setTextVisible(False)
        self.savedptajeBarPPGHome.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPPGAway = QProgressBar()
        self.savedptajeBarPPGAway.setFixedWidth(150)
        self.savedptajeBarPPGAway.setTextVisible(False)
        self.savedptajeBarPPGAway.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarTGPG = QProgressBar()
        self.savedptajeBarTGPG.setFixedWidth(150)
        self.savedptajeBarTGPG.setTextVisible(False)
        self.savedptajeBarTGPG.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPJHome = QProgressBar()
        self.savedptajeBarPJHome.setFixedWidth(150)
        self.savedptajeBarPJHome.setTextVisible(False)
        self.savedptajeBarPJHome.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPJAway = QProgressBar()
        self.savedptajeBarPJAway.setFixedWidth(150)
        self.savedptajeBarPJAway.setTextVisible(False)
        self.savedptajeBarPJAway.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarRempate = QProgressBar()
        self.savedptajeBarRempate.setFixedWidth(150)
        self.savedptajeBarRempate.setTextVisible(False)
        self.savedptajeBarRempate.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarODD1 = QProgressBar()
        self.savedptajeBarODD1.setFixedWidth(150)
        self.savedptajeBarODD1.setTextVisible(False)
        self.savedptajeBarODD1.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarODD2 = QProgressBar()
        self.savedptajeBarODD2.setFixedWidth(150)
        self.savedptajeBarODD2.setTextVisible(False)
        self.savedptajeBarODD2.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarODD_UNDER25 = QProgressBar()
        self.savedptajeBarODD_UNDER25.setFixedWidth(150)
        self.savedptajeBarODD_UNDER25.setTextVisible(False)
        self.savedptajeBarODD_UNDER25.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        

        self.listProfiles = QListWidget()
        self.listProfiles.setGeometry(50, 70, 150, 60) 

        #buttons
        self.save = QPushButton("Save")
        self.save.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))
        self.load = QPushButton("Load")
        self.add = QPushButton("Add")
        self.delete = QPushButton("Delete")
        self.delete.setIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogDiscardButton")))

        #conections

        self.save.clicked.connect(self.saveData)
        self.load.clicked.connect(self.loadData)
        self.delete.clicked.connect(self.deleteSelected)
        self.add.clicked.connect(self.addProfile)

        self.listProfiles.itemSelectionChanged.connect(self.setsavedBars)


        #other things
        self.actualizarLista()
        
        #layouts
        mainLayout = QVBoxLayout()
        dataLayout = QGridLayout()
        settsLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        #actual labels
        dataLayout.addWidget(self.actual, 0, 0, 1, 1)
        dataLayout.addWidget(self.pghd, 1, 0, 1, 1)
        dataLayout.addWidget(self.pgad, 2, 0, 1, 1)
        dataLayout.addWidget(self.phd, 3, 0, 1, 1)
        dataLayout.addWidget(self.pad, 4, 0, 1, 1)
        dataLayout.addWidget(self.ppghome, 5, 0, 1, 1)
        dataLayout.addWidget(self.ppgaway, 6, 0, 1, 1)
        dataLayout.addWidget(self.tgpg, 7, 0, 1, 1)
        dataLayout.addWidget(self.pjhome, 8, 0, 1, 1)
        dataLayout.addWidget(self.pjaway, 9, 0, 1, 1)
        dataLayout.addWidget(self.rempate, 10, 0, 1, 1)
        dataLayout.addWidget(self.odd1, 11, 0, 1, 1)
        dataLayout.addWidget(self.odd2, 12, 0, 1, 1)
        dataLayout.addWidget(self.odd_under25, 13, 0, 1, 1)

        #actal progressbar
        dataLayout.addWidget(self.ptajeBarPGHD, 1, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPGAD, 2, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPHD, 3, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPAD, 4, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPPGHome, 5, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPPGAway, 6, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarTGPG, 7, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPJHome, 8, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarPJAway, 9, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarRempate, 10, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarODDS1, 11, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarODDS2, 12, 1, 1, 1)
        dataLayout.addWidget(self.ptajeBarODDS_UNDER25, 13, 1, 1, 1)

       #saved labels
        dataLayout.addWidget(self.ssavedData, 0, 3, 1, 1)
        dataLayout.addWidget(self.spghd, 1, 2, 1, 1)
        dataLayout.addWidget(self.spgad, 2, 2, 1, 1)
        dataLayout.addWidget(self.sphd, 3, 2, 1, 1)
        dataLayout.addWidget(self.spad, 4, 2, 1, 1)
        dataLayout.addWidget(self.sppghome, 5, 2, 1, 1)
        dataLayout.addWidget(self.sppgaway, 6, 2, 1, 1)
        dataLayout.addWidget(self.stgpg, 7, 2, 1, 1)
        dataLayout.addWidget(self.spjhome, 8, 2, 1, 1)
        dataLayout.addWidget(self.spjaway, 9, 2, 1, 1)
        dataLayout.addWidget(self.srempate, 10, 2, 1, 1)
        dataLayout.addWidget(self.sodd1, 11, 2, 1, 1)
        dataLayout.addWidget(self.sodd2, 12, 2, 1, 1)
        dataLayout.addWidget(self.sodd_under25, 13, 2, 1, 1)

        #saved progressbar
        dataLayout.addWidget(self.savedptajeBarPGHD, 1, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPGAD, 2, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPHD, 3, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPAD, 4, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPPGHome, 5, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPPGAway, 6, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarTGPG, 7, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPJHome, 8, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarPJAway, 9, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarRempate, 10, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarODD1, 11, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarODD2, 12, 3, 1, 1)
        dataLayout.addWidget(self.savedptajeBarODD_UNDER25, 13, 3, 1, 1)

        #buttons
        settsLayout.addWidget(self.save)
        settsLayout.addWidget(self.load)
        settsLayout.addStretch()
        settsLayout.addWidget(self.add)
        settsLayout.addStretch()
        settsLayout.addWidget(self.delete)

        bottomLayout.addWidget(self.listProfiles)
        bottomLayout.addLayout(settsLayout)


        mainLayout.addLayout(dataLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)
        self.setFixedSize(QSize(420, 500))

    def deleteSelected(self):
        if len(self.listProfiles.selectedItems()) > 0:
            data ={}
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)               
            
            data.pop(self.listProfiles.takeItem(self.listProfiles.row(self.listProfiles.currentItem())).text())

            with open('svdStngs.json', "w") as json_file:
                json.dump(data, json_file)
            
            self.actualizarLista()
            self.ssavedData.setText("Saved data:")


    def addProfile(self):
            text, ok = QInputDialog.getText(self, 'Add profile', "Name your new profile:")
            if ok and text != "":
                try:
                    saveit = True
                    data = {}
                    with open('svdStngs.json', "r") as json_file:
                        data = json.load(json_file)
                        for d in data:
                            if d == text:
                                msg = QMessageBox()
                                msg.setIcon(QMessageBox.Warning)
                                msg.setText("There´s already a profile with this name")
                                msg.setWindowTitle("Name already taken")
                                msg.exec_()
                                saveit = False
                    
                    if saveit:
                        with open('svdStngs.json', "w") as json_file:
                            data[text] = {"PGHD" : 0, "PGAD" : 0, "PHD" : 0, "PAD" : 0,"TGPG" : 0, 
                                    "PPGHome" : 0, "PPGAway" : 0, "PJHome" : 0, "PJAway" : 0, "REmpate" : 0,
                                    "ODDS1" : 0, "ODDS2" : 0, "ODDS_UNDER25" : 0}
                            json.dump(data, json_file)
                        self.actualizarLista()
                            
                except KeyError:
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("An error has occur")
                    msg.setWindowTitle("Error")
                    msg.exec_()

    def setsavedBars(self):
        if len(self.listProfiles.selectedItems()) >= 1:
            self.ssavedData.setText("Saved data: {}".format(self.listProfiles.currentItem().text()))
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)     
                
                self.savedptajeBarPGHD.setValue(data[self.listProfiles.currentItem().text()]["PGHD"])
                self.savedptajeBarPGAD.setValue(data[self.listProfiles.currentItem().text()]["PGAD"])
                self.savedptajeBarPHD.setValue(data[self.listProfiles.currentItem().text()]["PHD"])
                self.savedptajeBarPAD.setValue(data[self.listProfiles.currentItem().text()]["PAD"])
                self.savedptajeBarPPGHome.setValue(data[self.listProfiles.currentItem().text()]["PPGHome"] * self.savedptajeBarPPGHome.maximum() / self.maninWindow.ptajeBarPPGHome.maximum())
                self.savedptajeBarPPGAway.setValue(data[self.listProfiles.currentItem().text()]["PPGAway"] * self.savedptajeBarPPGAway.maximum() / self.maninWindow.ptajeBarPPGAway.maximum())
                self.savedptajeBarTGPG.setValue(data[self.listProfiles.currentItem().text()]["TGPG"] * self.savedptajeBarTGPG.maximum() / self.maninWindow.ptajeBarTGPG.maximum())
                self.savedptajeBarPJHome.setValue(data[self.listProfiles.currentItem().text()]["PJHome"] * self.savedptajeBarPJHome.maximum() / self.maninWindow.ptajeBarPJHome.maximum())
                self.savedptajeBarPJAway.setValue(data[self.listProfiles.currentItem().text()]["PJAway"] * self.savedptajeBarPJAway.maximum() / self.maninWindow.ptajeBarPJAway.maximum())
                self.savedptajeBarRempate.setValue(data[self.listProfiles.currentItem().text()]["REmpate"] * self.savedptajeBarRempate.maximum() / self.maninWindow.ptajeBarRempate.maximum())         
                self.savedptajeBarODD1.setValue(data[self.listProfiles.currentItem().text()]["ODDS1"] * self.savedptajeBarODD1.maximum() / self.maninWindow.ptajeBarODD1.maximum())         
                self.savedptajeBarODD2.setValue(data[self.listProfiles.currentItem().text()]["ODDS2"] * self.savedptajeBarODD2.maximum() / self.maninWindow.ptajeBarODD2.maximum())         
                self.savedptajeBarODD_UNDER25.setValue(data[self.listProfiles.currentItem().text()]["ODDS_UNDER25"] * self.savedptajeBarODD_UNDER25.maximum() / self.maninWindow.ptajeBarUNDER25.maximum())         

    def setCurrentBars(self):

        self.ptajeBarPGHD.setValue(self.maninWindow.ptajeBarPGHD.value())
        self.ptajeBarPGAD.setValue(self.maninWindow.ptajeBarPGAD.value())
        self.ptajeBarPHD.setValue(self.maninWindow.ptajeBarPHD.value())
        self.ptajeBarPAD.setValue(self.maninWindow.ptajeBarPAD.value())
        self.ptajeBarPPGHome.setValue(self.maninWindow.ptajeBarPPGHome.value()* self.ptajeBarPPGHome.maximum() / self.maninWindow.ptajeBarPPGHome.maximum())
        self.ptajeBarPPGAway.setValue(self.maninWindow.ptajeBarPPGAway.value() * self.ptajeBarPPGAway.maximum() / self.maninWindow.ptajeBarPPGAway.maximum())
        self.ptajeBarTGPG.setValue(self.maninWindow.ptajeBarTGPG.value() * self.ptajeBarTGPG.maximum() / self.maninWindow.ptajeBarTGPG.maximum())
        self.ptajeBarPJHome.setValue(self.maninWindow.ptajeBarPJHome.value() * self.ptajeBarPJHome.maximum() / self.maninWindow.ptajeBarPJHome.maximum())
        self.ptajeBarPJAway.setValue(self.maninWindow.ptajeBarPJAway.value() * self.ptajeBarPJAway.maximum() / self.maninWindow.ptajeBarPJAway.maximum())
        self.ptajeBarRempate.setValue(self.maninWindow.ptajeBarRempate.value() * self.ptajeBarRempate.maximum() / self.maninWindow.ptajeBarRempate.maximum())
        self.ptajeBarODDS1.setValue(self.maninWindow.ptajeBarODD1.value() * self.ptajeBarODDS1.maximum() / self.maninWindow.ptajeBarODD1.maximum())
        self.ptajeBarODDS2.setValue(self.maninWindow.ptajeBarODD2.value() * self.ptajeBarODDS2.maximum() / self.maninWindow.ptajeBarODD2.maximum())
        self.ptajeBarODDS_UNDER25.setValue(self.maninWindow.ptajeBarUNDER25.value() * self.ptajeBarODDS_UNDER25.maximum() / self.maninWindow.ptajeBarUNDER25.maximum())

    def actualizarLista(self):    
        with open('svdStngs.json', "r") as json_file:
            try:
                self.listProfiles.clear()
                data = json.load(json_file)
                for d in data:
                    self.listProfiles.addItem(d)
                self.setsavedBars()
            except:
                pass
    
    def saveData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            data ={}
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)

            data[self.listProfiles.currentItem().text()] = {"PGHD" : self.maninWindow.ptajeBarPGHD.value(),
                                                            "PGAD" : self.maninWindow.ptajeBarPGAD.value(),
                                                            "PHD" : self.maninWindow.ptajeBarPHD.value(),
                                                            "PAD" : self.maninWindow.ptajeBarPAD.value(),
                                                            "TGPG" : self.maninWindow.ptajeBarTGPG.value(), 
                                                            "PPGHome" : self.maninWindow.ptajeBarPPGHome.value(),
                                                            "PPGAway" : self.maninWindow.ptajeBarPPGAway.value(),
                                                            "PJHome" : self.maninWindow.ptajeBarPJHome.value(),
                                                            "PJAway" : self.maninWindow.ptajeBarPJAway.value(),
                                                            "REmpate" : self.maninWindow.ptajeBarRempate.value(),
                                                            "ODDS1" : self.maninWindow.ptajeBarODD1.value(),
                                                            "ODDS2" : self.maninWindow.ptajeBarODD2.value(),
                                                            "ODDS_UNDER25" : self.maninWindow.ptajeBarUNDER25.value()
                                                            }

            with open('svdStngs.json', "w") as json_file:
                    json.dump(data, json_file)
                
            self.setsavedBars()

    def loadData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)

                self.maninWindow.ptajeBarPGHD.setValue(data[self.listProfiles.currentItem().text()]["PGHD"])
                self.maninWindow.ptajeBarPGAD.setValue(data[self.listProfiles.currentItem().text()]["PGAD"])
                self.maninWindow.ptajeBarPHD.setValue(data[self.listProfiles.currentItem().text()]["PHD"])
                self.maninWindow.ptajeBarPAD.setValue(data[self.listProfiles.currentItem().text()]["PAD"])
                self.maninWindow.ptajeBarTGPG.setValue(data[self.listProfiles.currentItem().text()]["TGPG"])
                self.maninWindow.ptajeBarPPGHome.setValue(data[self.listProfiles.currentItem().text()]["PPGHome"])
                self.maninWindow.ptajeBarPPGAway.setValue(data[self.listProfiles.currentItem().text()]["PPGAway"])
                self.maninWindow.ptajeBarPJHome.setValue(data[self.listProfiles.currentItem().text()]["PJHome"])
                self.maninWindow.ptajeBarPJAway.setValue(data[self.listProfiles.currentItem().text()]["PJAway"])
                self.maninWindow.ptajeBarRempate.setValue(data[self.listProfiles.currentItem().text()]["REmpate"])
                self.maninWindow.ptajeBarODD1.setValue(data[self.listProfiles.currentItem().text()]["ODDS1"])
                self.maninWindow.ptajeBarODD2.setValue(data[self.listProfiles.currentItem().text()]["ODDS2"])
                self.maninWindow.ptajeBarUNDER25.setValue(data[self.listProfiles.currentItem().text()]["ODDS_UNDER25"])
                
            self.setCurrentBars()
            self.maninWindow.aplicarResultado()
            self.close()
