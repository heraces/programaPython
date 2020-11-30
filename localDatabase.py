from PyQt5.QtWidgets import (QLabel, QPushButton, QInputDialog, QListWidget, QDialog, QAbstractItemView,
                            QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout, QStyle, QCheckBox)
from PyQt5.QtCore import QSize

import json

#clase para guardar en la database local
class SaveDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        #referencia a Filters
        self.maninWindow =  mainWindow
        self.setWindowIcon(self.style().standardIcon(getattr(QStyle, "SP_DialogSaveButton")))

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

        # los checkbox
        self.allCheck = QCheckBox()
        self.allCheck.setCheckable(True)
        self.allCheck.setChecked(True)
        self.pghdCheck = QCheckBox()
        self.pghdCheck.setCheckable(True)
        self.pgadCheck = QCheckBox()
        self.pgadCheck.setCheckable(True)
        self.phdCheck = QCheckBox()
        self.phdCheck.setCheckable(True)
        self.padCheck = QCheckBox()
        self.padCheck.setCheckable(True)
        self.ppghomeCheck = QCheckBox()
        self.ppghomeCheck.setCheckable(True)
        self.ppgawayCheck = QCheckBox()
        self.ppgawayCheck.setCheckable(True)
        self.tgpgCheck = QCheckBox()
        self.tgpgCheck.setCheckable(True)
        self.pjhomeCheck = QCheckBox()
        self.pjhomeCheck.setCheckable(True)
        self.pjawayCheck = QCheckBox()
        self.pjawayCheck.setCheckable(True)
        self.rempateCheck = QCheckBox()
        self.rempateCheck.setCheckable(True)
        self.odd1Check = QCheckBox()
        self.odd1Check.setCheckable(True)
        self.odd2Check = QCheckBox()
        self.odd2Check.setCheckable(True)
        self.odd_under25Check = QCheckBox()
        self.odd_under25Check.setCheckable(True)
        self.isChecked = True

        #labels value
        self.pghdValue = QLabel(str(self.maninWindow.ptajeBarPGHD.value()))
        self.pgadValue = QLabel(str(self.maninWindow.ptajeBarPGAD.value()))
        self.phdValue = QLabel(str(self.maninWindow.ptajeBarPHD.value()))
        self.padValue = QLabel(str(self.maninWindow.ptajeBarPAD.value()))
        self.ppghomeValue = QLabel(str(self.maninWindow.ptajeBarPPGHome.value()))
        self.ppgawayValue = QLabel(str(self.maninWindow.ptajeBarPPGAway.value()))
        self.tgpgValue = QLabel(self.maninWindow.ptajeBarTGPG.valuesToString())
        self.pjhomeValue = QLabel(str(self.maninWindow.ptajeBarPJHome.value()))
        self.pjawayValue = QLabel(str(self.maninWindow.ptajeBarPJAway.value()))
        self.rempateValue = QLabel(str(self.maninWindow.ptajeBarRempate.value()))
        self.odd1Value = QLabel(self.maninWindow.ptajeBarODD1.valuesToString())
        self.odd2Value = QLabel(self.maninWindow.ptajeBarODD2.valuesToString())
        self.odd_under25Value = QLabel(self.maninWindow.ptajeBarUNDER25.valuesToString())

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

        #saved value
        self.spghdValue = QLabel("0")
        self.spgadValue = QLabel("0")
        self.sphdValue = QLabel("0")
        self.spadValue = QLabel("0")
        self.sppghomeValue = QLabel("0")
        self.sppgawayValue = QLabel("0")
        self.stgpgValue = QLabel("0-5")
        self.spjhomeValue = QLabel("0")
        self.spjawayValue = QLabel("0")
        self.srempateValue =QLabel("0")
        self.sodd1Value = QLabel("0-10")
        self.sodd2Value = QLabel("0-10")
        self.sodd_under25Value = QLabel("0-10")

        self.listProfiles = QListWidget()
        self.listProfiles.setGeometry(50, 70, 150, 60) 
        self.listProfiles.setSelectionMode(QAbstractItemView.SingleSelection)

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

        #connect CheckBoxes
        self.allCheck.clicked.connect(self.checkBoxMaster)
        self.pghdCheck.clicked.connect(self.checkBoxManager)
        self.pgadCheck.clicked.connect(self.checkBoxManager)
        self.phdCheck.clicked.connect(self.checkBoxManager)
        self.padCheck.clicked.connect(self.checkBoxManager)
        self.ppghomeCheck.clicked.connect(self.checkBoxManager)
        self.ppgawayCheck.clicked.connect(self.checkBoxManager)
        self.tgpgCheck.clicked.connect(self.checkBoxManager)
        self.pjhomeCheck.clicked.connect(self.checkBoxManager)
        self.pjawayCheck.clicked.connect(self.checkBoxManager)
        self.rempateCheck.clicked.connect(self.checkBoxManager)
        self.odd1Check.clicked.connect(self.checkBoxManager)
        self.odd2Check.clicked.connect(self.checkBoxManager)
        self.odd_under25Check.clicked.connect(self.checkBoxManager)


        #other things
        self.actualizarLista()
        self.checkBoxMaster()

        #layouts
        mainLayout = QVBoxLayout()
        dataLayout = QGridLayout()
        settsLayout = QVBoxLayout()
        bottomLayout = QHBoxLayout()

        #checkBoxes 
        dataLayout.addWidget(self.allCheck, 0, 0, 1, 1)
        dataLayout.addWidget(self.pghdCheck, 1, 0, 1, 1)
        dataLayout.addWidget(self.pgadCheck, 2, 0, 1, 1)
        dataLayout.addWidget(self.phdCheck, 3, 0, 1, 1)
        dataLayout.addWidget(self.padCheck, 4, 0, 1, 1)
        dataLayout.addWidget(self.ppghomeCheck, 5, 0, 1, 1)
        dataLayout.addWidget(self.ppgawayCheck, 6, 0, 1, 1)
        dataLayout.addWidget(self.tgpgCheck, 7, 0, 1, 1)
        dataLayout.addWidget(self.pjhomeCheck, 8, 0, 1, 1)
        dataLayout.addWidget(self.pjawayCheck, 9, 0, 1, 1)
        dataLayout.addWidget(self.rempateCheck, 10, 0, 1, 1)
        dataLayout.addWidget(self.odd1Check, 11, 0, 1, 1)
        dataLayout.addWidget(self.odd2Check, 12, 0, 1, 1)
        dataLayout.addWidget(self.odd_under25Check, 13, 0, 1, 1) 

        #actual labels
        dataLayout.addWidget(self.actual, 0, 1, 1, 1)
        dataLayout.addWidget(self.pghd, 1, 1, 1, 1)
        dataLayout.addWidget(self.pgad, 2, 1, 1, 1)
        dataLayout.addWidget(self.phd, 3, 1, 1, 1)
        dataLayout.addWidget(self.pad, 4, 1, 1, 1)
        dataLayout.addWidget(self.ppghome, 5, 1, 1, 1)
        dataLayout.addWidget(self.ppgaway, 6, 1, 1, 1)
        dataLayout.addWidget(self.tgpg, 7, 1, 1, 1)
        dataLayout.addWidget(self.pjhome, 8, 1, 1, 1)
        dataLayout.addWidget(self.pjaway, 9, 1, 1, 1)
        dataLayout.addWidget(self.rempate, 10, 1, 1, 1)
        dataLayout.addWidget(self.odd1, 11, 1, 1, 1)
        dataLayout.addWidget(self.odd2, 12, 1, 1, 1)
        dataLayout.addWidget(self.odd_under25, 13, 1, 1, 1) 
        
        #values
        dataLayout.addWidget(self.pghdValue, 1, 2, 1, 1)
        dataLayout.addWidget(self.pgadValue, 2, 2, 1, 1)
        dataLayout.addWidget(self.phdValue, 3, 2, 1, 1)
        dataLayout.addWidget(self.padValue, 4, 2, 1, 1)
        dataLayout.addWidget(self.ppghomeValue, 5, 2, 1, 1)
        dataLayout.addWidget(self.ppgawayValue, 6, 2, 1, 1)
        dataLayout.addWidget(self.tgpgValue, 7, 2, 1, 1)
        dataLayout.addWidget(self.pjhomeValue, 8, 2, 1, 1)
        dataLayout.addWidget(self.pjawayValue, 9, 2, 1, 1)
        dataLayout.addWidget(self.rempateValue, 10, 2, 1, 1)
        dataLayout.addWidget(self.odd1Value, 11, 2, 1, 1)
        dataLayout.addWidget(self.odd2Value, 12, 2, 1, 1)
        dataLayout.addWidget(self.odd_under25Value, 13, 2, 1, 1)

       #saved labels
        dataLayout.addWidget(self.ssavedData, 0, 4, 1, 1)
        dataLayout.addWidget(self.spghd, 1, 3, 1, 1)
        dataLayout.addWidget(self.spgad, 2, 3, 1, 1)
        dataLayout.addWidget(self.sphd, 3, 3, 1, 1)
        dataLayout.addWidget(self.spad, 4, 3, 1, 1)
        dataLayout.addWidget(self.sppghome, 5, 3, 1, 1)
        dataLayout.addWidget(self.sppgaway, 6, 3, 1, 1)
        dataLayout.addWidget(self.stgpg, 7, 3, 1, 1)
        dataLayout.addWidget(self.spjhome, 8, 3, 1, 1)
        dataLayout.addWidget(self.spjaway, 9, 3, 1, 1)
        dataLayout.addWidget(self.srempate, 10, 3, 1, 1)
        dataLayout.addWidget(self.sodd1, 11, 3, 1, 1)
        dataLayout.addWidget(self.sodd2, 12, 3, 1, 1)
        dataLayout.addWidget(self.sodd_under25, 13, 3, 1, 1)

        #saved values
        dataLayout.addWidget(self.spghdValue, 1, 4, 1, 1)
        dataLayout.addWidget(self.spgadValue, 2, 4, 1, 1)
        dataLayout.addWidget(self.sphdValue, 3, 4, 1, 1)
        dataLayout.addWidget(self.spadValue, 4, 4, 1, 1)
        dataLayout.addWidget(self.sppghomeValue, 5, 4, 1, 1)
        dataLayout.addWidget(self.sppgawayValue, 6, 4, 1, 1)
        dataLayout.addWidget(self.stgpgValue, 7, 4, 1, 1)
        dataLayout.addWidget(self.spjhomeValue, 8, 4, 1, 1)
        dataLayout.addWidget(self.spjawayValue, 9, 4, 1, 1)
        dataLayout.addWidget(self.srempateValue, 10, 4, 1, 1)
        dataLayout.addWidget(self.sodd1Value, 11, 4, 1, 1)
        dataLayout.addWidget(self.sodd2Value, 12, 4, 1, 1)
        dataLayout.addWidget(self.sodd_under25Value, 13, 4, 1, 1)

        dataLayout.setColumnStretch(5,1)

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
                if text == "-":
                    msg = QMessageBox()
                    msg.setIcon(QMessageBox.Warning)
                    msg.setText("Está feo eso que intentas hacer ¬¬")
                    msg.setWindowTitle("Nombre invalido")
                    msg.exec_()
                else:
                    try:
                        saveit = True
                        with open("svdStngs.json") as json_file:
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
                                data[text] = {"PGHD" : 0, "PGAD" : 0, "PHD" : 0, "PAD" : 0,"TGPG" : [0, 1], 
                                        "PPGHome" : 0, "PPGAway" : 0, "PJHome" : 0, "PJAway" : 0, "REmpate" : 0,
                                        "ODDS1" : [0, 1], "ODDS2" : [0, 1], "ODDS_UNDER25" : [0, 1]}
                                json.dump(data, json_file)
                            self.actualizarLista()
                            
                    except KeyError:
                        msg = QMessageBox()
                        msg.setIcon(QMessageBox.Critical)
                        msg.setText("An error has occur")
                        msg.setWindowTitle("Error")
                        msg.exec_()

    def setsavedBars(self):
        if len(self.listProfiles.selectedItems()) >= 1:
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)
                self.ssavedData.setText("Saved data: {}".format(self.listProfiles.currentItem().text()))
                self.spghdValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PGHD"],2)))
                self.spgadValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PGAD"],2)))
                self.sphdValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PHD"],2)))
                self.spadValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PAD"],2)))
                self.stgpgValue.setText(str(round(data[self.listProfiles.currentItem().text()]["TGPG"][0],2)) + "-" + 
                                                    str(round(data[self.listProfiles.currentItem().text()]["TGPG"][1],2)))
                self.sppghomeValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PPGHome"],2)))
                self.sppgawayValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PPGAway"],2)))
                self.spjhomeValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PJHome"],2)))
                self.spjawayValue.setText(str(round(data[self.listProfiles.currentItem().text()]["PJAway"],2)))
                self.srempateValue.setText(str(round(data[self.listProfiles.currentItem().text()]["REmpate"])))
                self.sodd1Value.setText(str(round(data[self.listProfiles.currentItem().text()]["ODDS1"][0],2))+ "-" + 
                                                    str(round(data[self.listProfiles.currentItem().text()]["ODDS1"][1],2)))
                self.sodd2Value.setText(str(round(data[self.listProfiles.currentItem().text()]["ODDS2"][0],2))+ "-" + 
                                                    str(round(data[self.listProfiles.currentItem().text()]["ODDS2"][1],2)))
                self.sodd_under25Value.setText(str(round(data[self.listProfiles.currentItem().text()]["ODDS_UNDER25"][0],2))+ "-" + 
                                                    str(round(data[self.listProfiles.currentItem().text()]["ODDS_UNDER25"][1],2)))
       
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

        for i in range(self.listProfiles.count()):
            if self.maninWindow.filterProfile.text() == self.listProfiles.item(i).text() + " -profile":
               self.listProfiles.setCurrentRow(i)
               break
    
    def saveData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            data ={}
            dic = {}

            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)
                dic = data[self.listProfiles.currentItem().text()]

            if self.pghdCheck.isChecked():
                dic["PGHD"] = self.maninWindow.ptajeBarPGHD.value()
            if self.pgadCheck.isChecked():  
                dic["PGAD"] = self.maninWindow.ptajeBarPGAD.value()      
            if self.phdCheck.isChecked():
                dic["PHD"] = self.maninWindow.ptajeBarPHD.value() 
            if self.padCheck.isChecked():
                dic["PAD"] = self.maninWindow.ptajeBarPAD.value()
            if self.tgpgCheck.isChecked():
                dic["TGPG"] = self.maninWindow.ptajeBarTGPG.values()
            if self.ppghomeCheck.isChecked():
                dic["PPGHome"] = self.maninWindow.ptajeBarPPGHome.value()
            if self.ppgawayCheck.isChecked():
                dic["PPGAway"] = self.maninWindow.ptajeBarPPGAway.value()                
            if self.pjhomeCheck.isChecked():
                dic["PJHome"] = self.maninWindow.ptajeBarPJHome.value()
            if self.pjawayCheck.isChecked():
                dic["PJAway"] = self.maninWindow.ptajeBarPJAway.value()
            if self.rempateCheck.isChecked():
                dic["REmpate"] = self.maninWindow.ptajeBarRempate.value()
            if self.odd1Check.isChecked():
                dic["ODDS1"] = self.maninWindow.ptajeBarODD1.values()
            if self.odd2Check.isChecked():
                dic["ODDS2"] = self.maninWindow.ptajeBarODD2.values()
            if self.odd_under25Check.isChecked():
                dic["ODDS_UNDER25"] = self.maninWindow.ptajeBarUNDER25.values()

            data[self.listProfiles.currentItem().text()] = dic

            with open('svdStngs.json', "w") as json_file:
                    json.dump(data, json_file)
                
            self.setsavedBars()

    def loadData(self):
        if len(self.listProfiles.selectedItems()) > 0:
            with open('svdStngs.json', "r") as json_file:
                data = json.load(json_file)

                if self.pghdCheck.isChecked():
                    self.maninWindow.ptajeBarPGHD.setValue(data[self.listProfiles.selectedItems()[0].text()]["PGHD"])
                if self.pgadCheck.isChecked():
                    self.maninWindow.ptajeBarPGAD.setValue(data[self.listProfiles.selectedItems()[0].text()]["PGAD"])
                if self.phdCheck.isChecked():
                    self.maninWindow.ptajeBarPHD.setValue(data[self.listProfiles.selectedItems()[0].text()]["PHD"])
                if self.padCheck.isChecked():
                    self.maninWindow.ptajeBarPAD.setValue(data[self.listProfiles.selectedItems()[0].text()]["PAD"])
                if self.ppghomeCheck.isChecked():
                    self.maninWindow.ptajeBarPPGHome.setValue(data[self.listProfiles.selectedItems()[0].text()]["PPGHome"])
                if self.ppgawayCheck.isChecked():
                    self.maninWindow.ptajeBarPPGAway.setValue(data[self.listProfiles.selectedItems()[0].text()]["PPGAway"])
                if self.pjhomeCheck.isChecked():
                    self.maninWindow.ptajeBarPJHome.setValue(data[self.listProfiles.selectedItems()[0].text()]["PJHome"])
                if self.pjawayCheck.isChecked():
                    self.maninWindow.ptajeBarPJAway.setValue(data[self.listProfiles.selectedItems()[0].text()]["PJAway"])
                if self.rempateCheck.isChecked():
                    self.maninWindow.ptajeBarRempate.setValue(data[self.listProfiles.selectedItems()[0].text()]["REmpate"])

                
                if self.tgpgCheck.isChecked():
                    self.maninWindow.ptajeBarTGPG.setBigerThanHandler(data[self.listProfiles.selectedItems()[0].text()]["TGPG"][0])
                    self.maninWindow.ptajeBarTGPG.setLessThanHandler(data[self.listProfiles.selectedItems()[0].text()]["TGPG"][1])
                if self.odd1Check.isChecked():
                    self.maninWindow.ptajeBarODD1.setBigerThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS1"][0])
                    self.maninWindow.ptajeBarODD1.setLessThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS1"][1])
                if self.odd2Check.isChecked():
                    self.maninWindow.ptajeBarODD2.setBigerThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS2"][0])
                    self.maninWindow.ptajeBarODD2.setLessThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS2"][1])
                if self.odd_under25Check.isChecked():
                    self.maninWindow.ptajeBarUNDER25.setBigerThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS_UNDER25"][0])
                    self.maninWindow.ptajeBarUNDER25.setLessThanHandler(data[self.listProfiles.selectedItems()[0].text()]["ODDS_UNDER25"][1])
                
            self.maninWindow.filterProfile.setText(self.listProfiles.selectedItems()[0].text() + " -profile")
            self.maninWindow.aplicarResultado()
            self.close()

    def checkBoxManager(self):
        self.isChecked = True
        if not self.pghdCheck.isChecked():
            self.isChecked = False
        elif not self.pgadCheck.isChecked():
            self.isChecked = False
        elif not self.phdCheck.isChecked():
            self.isChecked = False
        elif not self.padCheck.isChecked():
            self.isChecked = False
        elif not self.ppghomeCheck.isChecked():
            self.isChecked = False
        elif not self.ppgawayCheck.isChecked():
           self.isChecked = False
        elif not self.tgpgCheck.isChecked():
            self.isChecked = False
        elif not self.pjhomeCheck.isChecked():
            self.isChecked = False
        elif not self.pjawayCheck.isChecked():
            self.isChecked = False
        elif not self.rempateCheck.isChecked():
            self.isChecked = False
        elif not self.odd1Check.isChecked():
            self.isChecked = False
        elif not self.odd2Check.isChecked():
            self.isChecked = False
        elif not self.odd_under25Check.isChecked():
            self.isChecked = False
            
        self.allCheck.setChecked(self.isChecked)

    def checkBoxMaster(self):
        if self.allCheck.isChecked():
            self.isChecked = True
            self.pghdCheck.setChecked(True)
            self.pgadCheck.setChecked(True)
            self.phdCheck.setChecked(True)
            self.padCheck.setChecked(True)
            self.ppghomeCheck.setChecked(True)
            self.ppgawayCheck.setChecked(True)
            self.tgpgCheck.setChecked(True)
            self.pjhomeCheck.setChecked(True)
            self.pjawayCheck.setChecked(True)
            self.rempateCheck.setChecked(True)
            self.odd1Check.setChecked(True)
            self.odd2Check.setChecked(True)
            self.odd_under25Check.setChecked(True)

        else:
            self.isChecked = False
            self.pghdCheck.setChecked(False)
            self.pgadCheck.setChecked(False)
            self.phdCheck.setChecked(False)
            self.padCheck.setChecked(False)
            self.ppghomeCheck.setChecked(False)
            self.ppgawayCheck.setChecked(False)
            self.tgpgCheck.setChecked(False)
            self.pjhomeCheck.setChecked(False)
            self.pjawayCheck.setChecked(False)
            self.rempateCheck.setChecked(False)
            self.odd1Check.setChecked(False)
            self.odd2Check.setChecked(False)
            self.odd_under25Check.setChecked(False)