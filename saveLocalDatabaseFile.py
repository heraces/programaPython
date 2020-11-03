from PyQt5.QtWidgets import (QMainWindow, QWidget, QLabel, QLineEdit, QListView, QPushButton,
            QCheckBox, QListWidget, QVBoxLayout, QMessageBox, QHBoxLayout)
from PyQt5.QtCore import QSize, Qt
from settings import Settings

#clase para guardar en la database local
class SaveDosPuntosTheClass(QMainWindow):
    def __init__(self, mainWindow):
        super().__init__()

        #referencia a Filters
        self.maninWindow =  mainWindow
        #widgets
        mainWidget = QWidget(self)
        #profiles
        profiles = QLabel("Profiles")
        self.listProfiles = QListWidget()
        self.listProfiles.setGeometry(50, 70, 150, 60) 
        self.new = QPushButton("New")
        self.delete = QPushButton("Delete")
        self.currentProfile = QLineEdit()
        #settings in such profiles
        self.checkBox = QCheckBox()
        self.labelSB = QLabel("Searck bar")
        self.labelSP = QLabel("Selected profile")
        self.labelValue = QLabel("Value filter")
        self.checkBoxSB = QCheckBox("-Nothing-")
        self.checkBoxG = QCheckBox("more")
        self.checkBoxGV = QCheckBox("than: 0")

        self.save = QPushButton("Save")
        self.aply = QPushButton("Load all")

        #default values of those settings and valiables which we´ll store
        self.greate = 0
        self.searchBar = "-Nothing-"
        self.greaterValue = 0.0
        
        #getDatabase
        self.settings = Settings()
        
        #otras cosas

        self.currentProfile.setReadOnly(True)
        self.listProfiles.addItems(self.settings.charge())
        self.newName()
        self.namer.returnPressed.connect(self.namerSend)
        self.new.clicked.connect(self.newNameOpen)
        self.delete.clicked.connect(self.deleteProfile)
        self.checkBox.clicked.connect(self.multipleSelect)
        self.checkBoxG.clicked.connect(self.interselect)
        self.checkBoxGV.clicked.connect(self.interselect)
        self.checkBoxSB.clicked.connect(self.interselect)
        self.listProfiles.currentItemChanged.connect(self.changeCurrentItem)

        self.save.clicked.connect(self.saveData)
        self.aply.clicked.connect(self.loadData)


        
        #layouts
        leftLayout = QVBoxLayout()
        rigthLayout = QVBoxLayout()
        mainLayout = QHBoxLayout()
        layerGreater = QHBoxLayout()

        
        layerGreater.addWidget(self.checkBoxG)
        layerGreater.addWidget(self.checkBoxGV)
        layerGreater.addWidget(self.save)
        layerGreater.addWidget(self.aply)
        
        leftLayout.addWidget(profiles)
        leftLayout.addWidget(self.listProfiles)
        leftLayout.addWidget(self.labelSP)
        leftLayout.addWidget(self.currentProfile)
        leftLayout.addWidget(self.checkBox)
        leftLayout.addWidget(self.labelSB)
        leftLayout.addWidget(self.checkBoxSB)
        leftLayout.addWidget(self.labelValue)
        leftLayout.addLayout(layerGreater)
        

        rigthLayout.addWidget(self.new)
        rigthLayout.addWidget(self.delete)

        mainLayout.addLayout(leftLayout)
        mainLayout.addLayout(rigthLayout)
        
        mainWidget.setLayout(mainLayout)
        self.setMinimumSize(QSize(400, 500))
        self.setCentralWidget(mainWidget)

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
            self.checkBox.setChecked(False)