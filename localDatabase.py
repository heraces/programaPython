from PyQt5.QtWidgets import (QDialog, QWidget, QLabel, QLineEdit, QListView, QPushButton, QProgressBar,
            QCheckBox, QListWidget, QVBoxLayout, QMessageBox, QHBoxLayout, QGridLayout)
from PyQt5.QtCore import QSize, Qt
from settings import Settings

#clase para guardar en la database local
class SaveDialog(QDialog):
    def __init__(self, mainWindow):
        super().__init__()

        #referencia a Filters
        self.maninWindow =  mainWindow
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

        # actual progresbar
        self.ptajeBarPGHD = QProgressBar()
        self.ptajeBarPGHD.setTextVisible(False)
        self.ptajeBarPGHD.setFixedWidth(150)
        self.ptajeBarPGHD.setValue(self.maninWindow.ptajeBarPGHD.value())

        self.ptajeBarPGAD = QProgressBar()
        self.ptajeBarPGAD.setTextVisible(False)
        self.ptajeBarPGAD.setFixedWidth(150)
        self.ptajeBarPGAD.setValue(self.maninWindow.ptajeBarPGAD.value())

        self.ptajeBarPHD = QProgressBar()
        self.ptajeBarPHD.setTextVisible(False)
        self.ptajeBarPHD.setFixedWidth(150)
        self.ptajeBarPHD.setValue(self.maninWindow.ptajeBarPHD.value())

        self.ptajeBarPAD = QProgressBar()
        self.ptajeBarPAD.setTextVisible(False)
        self.ptajeBarPAD.setFixedWidth(150)
        self.ptajeBarPAD.setValue(self.maninWindow.ptajeBarPAD.value())

        self.ptajeBarPPGHome = QProgressBar()
        self.ptajeBarPPGHome.setTextVisible(False)
        self.ptajeBarPPGHome.setFixedWidth(150)
        self.ptajeBarPPGHome.setValue(self.maninWindow.ptajeBarPPGHome.value()* self.ptajeBarPPGHome.maximum() / self.maninWindow.ptajeBarPPGHome.maximum())

        self.ptajeBarPPGAway = QProgressBar()
        self.ptajeBarPPGAway.setTextVisible(False)
        self.ptajeBarPPGAway.setFixedWidth(150)
        self.ptajeBarPPGAway.setValue(self.maninWindow.ptajeBarPPGAway.value() * self.ptajeBarPPGAway.maximum() / self.maninWindow.ptajeBarPPGAway.maximum())
        

        self.ptajeBarTGPG = QProgressBar()
        self.ptajeBarTGPG.setTextVisible(False)
        self.ptajeBarTGPG.setFixedWidth(150)
        self.ptajeBarTGPG.setValue(self.maninWindow.ptajeBarTGPG.value() * self.ptajeBarTGPG.maximum() / self.maninWindow.ptajeBarTGPG.maximum())

        self.ptajeBarPJHome = QProgressBar()
        self.ptajeBarPJHome.setTextVisible(False)
        self.ptajeBarPJHome.setFixedWidth(150)
        self.ptajeBarPJHome.setValue(self.maninWindow.ptajeBarPJHome.value() * self.ptajeBarPJHome.maximum() / self.maninWindow.ptajeBarPJHome.maximum())

        self.ptajeBarPJAway = QProgressBar()
        self.ptajeBarPJAway.setTextVisible(False)
        self.ptajeBarPJAway.setFixedWidth(150)
        self.ptajeBarPJAway.setValue(self.maninWindow.ptajeBarPJAway.value() * self.ptajeBarPJAway.maximum() / self.maninWindow.ptajeBarPJAway.maximum())

        self.ptajeBarRempate = QProgressBar()
        self.ptajeBarRempate.setTextVisible(False)
        self.ptajeBarRempate.setFixedWidth(150)
        self.ptajeBarRempate.setValue(self.maninWindow.ptajeBarRempate.value() * self.ptajeBarRempate.maximum() / self.maninWindow.ptajeBarRempate.maximum())


        #saved data
        self.ssavedData = QLabel("Saved Data")
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

        #saved progressbar

        self.savedptajeBarPGHD = QProgressBar()
        self.savedptajeBarPGHD.setFixedWidth(150)
        self.savedptajeBarPGHD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarPGAD = QProgressBar()
        self.savedptajeBarPGAD.setFixedWidth(150)
        self.savedptajeBarPGAD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPHD = QProgressBar()
        self.savedptajeBarPHD.setFixedWidth(150)
        self.savedptajeBarPHD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPAD = QProgressBar()
        self.savedptajeBarPAD.setFixedWidth(150)
        self.savedptajeBarPAD.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        
        self.savedptajeBarPPGHome = QProgressBar()
        self.savedptajeBarPPGHome.setFixedWidth(150)
        self.savedptajeBarPPGHome.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPPGAway = QProgressBar()
        self.savedptajeBarPPGAway.setFixedWidth(150)
        self.savedptajeBarPPGAway.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarTGPG = QProgressBar()
        self.savedptajeBarTGPG.setFixedWidth(150)
        self.savedptajeBarTGPG.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPJHome = QProgressBar()
        self.savedptajeBarPJHome.setFixedWidth(150)
        self.savedptajeBarPJHome.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarPJAway = QProgressBar()
        self.savedptajeBarPJAway.setFixedWidth(150)
        self.savedptajeBarPJAway.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")

        self.savedptajeBarRempate = QProgressBar()
        self.savedptajeBarRempate.setFixedWidth(150)
        self.savedptajeBarRempate.setStyleSheet("QProgressBar::chunk {background-color: rgb(150,150,150);}")
        

        self.listProfiles = QListWidget()
        self.listProfiles.setGeometry(50, 70, 150, 60) 

        #buttons
        self.save = QPushButton("Save")
        self.load = QPushButton("Load")
        self.add = QPushButton("Add")
        self.delete = QPushButton("Delete")
        
        
        #otras cosas
        """
        self.currentProfile.setReadOnly(True)
        self.listProfiles.addItems(self.settings.charge())
        self.newName()
        self.namer.returnPressed.connect(self.namerSend)
        self.new.clicked.connect(self.newNameOpen)
        self.delete.clicked.connect(self.deleteProfile)
        self.listProfiles.currentItemChanged.connect(self.changeCurrentItem)
        """

        #self.save.clicked.connect(self.saveData)
        #self.aply.clicked.connect(self.loadData)


        
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

        #buttons
        settsLayout.addWidget(self.save)
        settsLayout.addWidget(self.load)
        settsLayout.addStretch()
        settsLayout.addWidget(self.add)
        settsLayout.addWidget(self.delete)

        bottomLayout.addWidget(self.listProfiles)
        bottomLayout.addLayout(settsLayout)


        mainLayout.addLayout(dataLayout)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)
        self.setFixedSize(QSize(420, 500))
"""
    def newName(self):
        self.giveNewName = QWidget()
        self.giveNewName.setFixedSize(QSize(300, 50))
        self.giveNewName.setWindowTitle("Add profile")
        self.namer = QLineEdit(self.giveNewName)
        self.namer.setFixedSize(QSize(300, 50))
        self.namer.setMaxLength(19)

    def newNameOpen(self):
        self.giveNewName.show()

    def namerSend(self):
        if not self.namer.text() == "":
            if 0 < len(self.listProfiles.findItems(self.namer.text(), Qt.MatchExactly)):
                QMessageBox.about(self, "Imposible", "A profile with this name already exist")                
            else:
                self.listProfiles.addItem(self.namer.text())
                self.settings.addProfile(self.namer.text())
                
        self.giveNewName.close()
        self.namer.clear()

    def deleteProfile(self):
        listItems = self.listProfiles.selectedItems()
        if not listItems: return        
        for item in listItems:
            self.settings.delete(item.text())
            self.listProfiles.takeItem(self.listProfiles.row(item))

    def changeGreaterValue(self, checked):
        if checked:
            self.checkBoxG.setText("less")
            self.greate = 1
        else:
            self.checkBoxG.setText("more")
            self.greate = 0

    def changeCurrentItem(self):
        if(self.listProfiles.currentItem()):
            self.currentProfile.setText(self.listProfiles.currentItem().text())

    def saveData(self):
        lista ={}
        a = {"serarchLine": [self.checkBoxSB.isChecked(),self.checkBoxSB.text()]}
        lista.update(a)
        a = {"greater": [self.checkBoxG.isChecked(),self.greate]}
        lista.update(a)
        a = {"greatValue": [self.checkBoxGV.isChecked(), self.greaterValue]}
        lista.update(a)

        self.settings.updateProfile(self.listProfiles.currentItem().text(), lista)

    def loadData(self):
        elsita = self.settings.loadProfile(self.listProfiles.currentItem().text())
        if elsita[1] == "-Nothing-":
            self.maninWindow.search.setText("")
        else:
            self.maninWindow.search.setText(elsita[1])

        if elsita[2] == 0:
            self.maninWindow.loadGreater(False)
        else:
            self.maninWindow.loadGreater(True)

        self.maninWindow.porcentaje.setValue(elsita[3])
        self.maninWindow.onChanged()



    def multipleSelect(self):
        if self.checkBox.isChecked():
            self.checkBoxG.setChecked(True)
            self.checkBoxGV.setChecked(True)
            self.checkBoxSB.setChecked(True)
        else:
            self.checkBoxG.setChecked(False)
            self.checkBoxGV.setChecked(False)
            self.checkBoxSB.setChecked(False)

    def interselect(self):
        if self.checkBoxG.isChecked() and self.checkBoxSB.isChecked() and self.checkBoxGV.isChecked():
            self.checkBox.setChecked(True)
        else:
            self.checkBox.setChecked(False)"""