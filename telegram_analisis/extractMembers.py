from telethon.sync import TelegramClient

from PyQt5.QtWidgets import (QTableWidget, QApplication, QMainWindow, QWidget, QComboBox, QLabel, QProgressBar,
                             QVBoxLayout, QHBoxLayout, QInputDialog, QTableWidgetItem, QHeaderView, QMessageBox)
from PyQt5.QtCore import QSize, Qt

import sys
import csv

api_id = #API
api_hash = #HASH
phone = #TLF (INT)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Users telegram Channel")
        self.init()#sets up the app view

        #creamos el cliente
        self.client = TelegramClient('BetApuestas_Session', api_id, api_hash)
        self.client.connect()

        #autentificamos
        if not self.client.is_user_authorized():
            text, ok = QInputDialog.getText(self, 'Autentication', "Confirm your autentication: ")
            if ok:
                self.client.send_code_request(phone)
                self.client.sign_in(phone, text)

        #we get the channels
        self.dic = {}
        self.groups = []
        for chat in self.client.iter_dialogs():
            try:
                if chat.is_channel:
                    self.groups.append(chat)
                    self.dic[chat.title] = False
                    self.channelList.addItem(chat.title)
            except:
                continue

    def init(self):
        widget = QWidget()
        layout = QVBoxLayout()
        progreslayout = QHBoxLayout()
        mainLabel = QLabel("Choose the channel")
        listLabel = QLabel("List of users of this channel")
        self.progressbar = QProgressBar()

        self.channelList = QComboBox()
        self.channelList.currentIndexChanged.connect(self.changeChannel)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["alias", "first name", "last name", "phone number"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.horizontalHeader().sectionClicked.connect(self.ordenar)

        progreslayout.addWidget(listLabel)
        progreslayout.addStretch()
        progreslayout.addWidget(self.progressbar)

        layout.addWidget(mainLabel)
        layout.addWidget(self.channelList)
        layout.addLayout(progreslayout)
        layout.addWidget(self.table)

        widget.setLayout(layout)

        self.setMinimumSize(QSize(1000, 700))
        self.setCentralWidget(widget)

    #cambiamos participantes y tal
    def changeChannel(self, index):
        if len(self.groups) > 0: 
            #si no hemos guardado ese canal lo guardamos
            if not self.dic[self.channelList.currentText()]:
                target_group= self.groups[self.channelList.currentIndex()]
                self.all_participants = self.client.get_participants(target_group, aggressive=True)
                self.dic[self.channelList.currentText()] = True
                self.save()

            self.showTable()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This account owns no channels")
            msg.setWindowTitle("You have no channels")
            msg.exec_()

    #poblamos la tabla
    def showTable(self):
        self.table.clearContents()
        name = self.channelList.currentText() + ".csv"
        with open(name,"r",encoding='UTF-8') as f:
            data = list(csv.reader(f,delimiter=";",lineterminator="\n"))
            self.table.setRowCount(len(data))
            self.progressbar.setValue(0)
            self.progressbar.show()
            fila = 0
            for row in data:
                self.table.setItem(fila, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(fila, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(fila, 2, QTableWidgetItem(str(row[2])))
                self.table.setItem(fila, 3, QTableWidgetItem(str(row[3])))

                self.table.item(fila, 0).setTextAlignment(Qt.AlignHCenter)
                self.table.item(fila, 1).setTextAlignment(Qt.AlignHCenter)
                self.table.item(fila, 2).setTextAlignment(Qt.AlignHCenter)
                self.table.item(fila, 3).setTextAlignment(Qt.AlignHCenter)
                fila += 1

                self.progressbar.setValue(int(fila/len(data) * 100))

            self.progressbar.hide()
              
    def save(self):
        name = self.channelList.currentText() + ".csv"
        with open(name,"w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=";",lineterminator="\n")
            for user in self.all_participants:
                if not user.is_self:
                    if user.username:
                        username= user.username
                    else:
                        username= ""
                    if user.first_name:
                        first_name= user.first_name
                    else:
                        first_name= ""
                    if user.last_name:
                        last_name= user.last_name
                    else:
                        last_name= ""
                    writer.writerow([username, first_name, last_name, user.phone])  

    def ordenar(self, sortingColumn):
        if len(self.groups) > 0: 
            self.progressbar.setValue(0)
            self.progressbar.show()
            arrangeList = []
            name = self.channelList.currentText() + ".csv"
            with open(name,"r",encoding='UTF-8') as f:
                arrangeList.extend(list(csv.reader(f,delimiter=";",lineterminator="\n")))

            row = 0
            for indice in range(len(arrangeList)-1, 0, -1):
                for sorting in range(indice):
                    if arrangeList[sorting][sortingColumn] > arrangeList[indice][sortingColumn]:
                        line = arrangeList[indice]
                        arrangeList[indice] = arrangeList[sorting]
                        arrangeList[sorting] = line

                self.progressbar.setValue(int(row/len(arrangeList) *100))
                row += 1
            
            with open(name,"w",encoding='UTF-8') as f:
                writer = csv.writer(f,delimiter=";",lineterminator="\n")
                for item in arrangeList:
                    writer.writerow(item)

            self.progressbar.hide()
            self.showTable()

    #cuando cerramos cerramos el cliente
    def close(self):
        self.client.disconnect()
        super().close()

app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()