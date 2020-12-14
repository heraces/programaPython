from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty

from PyQt5.QtWidgets import (QTableWidget, QApplication, QMainWindow, QWidget, QComboBox, QLabel,
                             QVBoxLayout, QInputDialog, QTableWidgetItem, QHeaderView)
from PyQt5.QtCore import QSize

import sys
import csv

api_id = #API
api_hash = #HAS
phone = #TLF (INT)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Users telegram Channel")
        self.init()#set up te app view

        #creamos el cliente
        self.client = TelegramClient('BetApuestas_Session', api_id, api_hash)
        self.client.connect()

        #autentificamos
        if not self.client.is_user_authorized():
            text, ok = QInputDialog.getText(self, 'Autentication', "Confirm your autentication: ")
            if ok and text != "":
                self.client.send_code_request(phone)
                self.client.sign_in(phone, text)

        #we get thte channels
        self.groups=[]
        for chat in self.client.iter_dialogs():
            try:
                if chat.is_channel:
                    self.groups.append(chat)
                    self.channelList.addItem(chat.title)
            except:
                continue

        #tomamos el primer channel 
        target_group = self.groups[self.channelList.currentIndex()]

        self.all_participants = []
        self.all_participants = self.client.get_participants(target_group, aggressive=True)


        #saving file
        with open("SBWS.csv","w",encoding='UTF-8') as f:
            writer = csv.writer(f,delimiter=";",lineterminator="\n")
            #writer.writerow(['username','user id', 'access hash','name','group', 'group id'])
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

        self.showTable()


    def init(self):
        widget = QWidget()
        layout = QVBoxLayout()
        mainLabel = QLabel("Choose the channel")
        listLabel = QLabel("List of users of this channel")

        self.channelList = QComboBox()
        self.channelList.currentIndexChanged.connect(self.changeChannel)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["alias", "first name", "last name", "phone number"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        layout.addWidget(mainLabel)
        layout.addWidget(self.channelList)
        layout.addWidget(listLabel)
        layout.addWidget(self.table)

        widget.setLayout(layout)

        self.setMinimumSize(QSize(1000, 700))
        self.setCentralWidget(widget)

    #cambiamos participantes y tal
    def changeChannel(self, index):
        target_group= self.groups[self.channelList.currentIndex()]
        self.all_participants = self.client.get_participants(target_group, aggressive=True)
        self.showTable()

    #cuando cerramos cerramos el cliente
    def close(self):
        self.client.disconnect()
        super().close()

    #poblamos la tabla
    def showTable(self):
        self.table.clearContents()
        with open("SBWS.csv","r",encoding='UTF-8') as f:
            data = list(csv.reader(f,delimiter=";",lineterminator="\n"))
            self.table.setRowCount(len(data))
            fila = 0
            for row in data:
                self.table.setItem(fila, 0, QTableWidgetItem(str(row[0])))
                self.table.setItem(fila, 1, QTableWidgetItem(str(row[1])))
                self.table.setItem(fila, 2, QTableWidgetItem(str(row[2])))
                self.table.setItem(fila, 3, QTableWidgetItem(str(row[3])))
                fila += 1
              


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()