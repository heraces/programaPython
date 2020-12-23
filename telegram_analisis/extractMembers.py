from telethon.sync import TelegramClient
from telethon.tl import functions
from PyQt5.QtWidgets import (QTableWidget, QApplication, QMainWindow, QWidget, QComboBox, QLabel, QProgressBar, QLineEdit,
                             QVBoxLayout, QHBoxLayout, QInputDialog, QTableWidgetItem, QHeaderView, QMessageBox,QPushButton)
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
        self.client = TelegramClient('MemberAnalisis_Session', api_id, api_hash)
        self.client.connect()

        #autentificamos
        if not self.client.is_user_authorized():
            text, ok = QInputDialog.getText(self, 'Autentication', "Confirm your autentication: ")
            if ok:
                self.client.send_code_request(phone)
                self.client.sign_in(phone, text)

        #we get the channels
        self.groups = []
        for chat in self.client.iter_dialogs():
            if chat.is_channel:
                try:
                    aux = self.client.get_participants(chat, aggressive=True)
                    self.groups.append(chat)
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
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["alias", "first name", "last name", "phone number", "Eliminar"])
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
            target_group= self.groups[self.channelList.currentIndex()]
            self.all_participants = []
            for user in self.client.get_participants(target_group, aggressive=True):
                if not user.is_self:
                    lista = []
                    lista.append(user.id)
                    lista.append(str(user.username))
                    lista.append(str(user.first_name))
                    lista.append(str(user.last_name))
                    lista.append(str(user.phone))
                    lista.append(user.contact)
                    self.all_participants.append(lista)
                          
            self.showTable()

        else:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)
            msg.setText("This account is admin of no channels")
            msg.setWindowTitle("No channels found")
            msg.exec_()

    #poblamos la tabla
    def showTable(self):
        self.table.clearContents()
        self.buttonefective = []
        self.table.setRowCount(len(self.all_participants))
        self.progressbar.setValue(0)
        self.progressbar.show()
        fila = 0
        for user in self.all_participants:
            lista = []
            #nombre
            aux = QLineEdit(str(user[2]))
            aux.setAlignment(Qt.AlignHCenter)
            aux.setStyleSheet("QLineEdit, QLineEdit:focus { border: none; }")
            aux.returnPressed.connect(self.changeName)

            #last_name
            aux2 = QLineEdit(str(user[3]))
            aux2.setAlignment(Qt.AlignHCenter)
            aux2.setStyleSheet("QLineEdit, QLineEdit:focus { border: none; }")
            aux2.returnPressed.connect(self.changeLastName)

            lista.append(aux)
            lista.append(aux2)
            self.buttonefective.append(lista)
            
            button = QPushButton("Eliminar")
            lista.append(button)
            #button.clicked.connect(self.delete)
            
            self.table.setItem(fila, 0, QTableWidgetItem(str(user[1])))
            self.table.setCellWidget(fila, 1, aux)
            self.table.setCellWidget(fila, 2, aux2)
            self.table.setItem(fila, 3, QTableWidgetItem(str(user[4])))
            self.table.setCellWidget(fila, 4, button)

            self.table.item(fila, 0).setTextAlignment(Qt.AlignHCenter)
            self.table.item(fila, 3).setTextAlignment(Qt.AlignHCenter)

            fila += 1

            self.progressbar.setValue(int(fila/len(self.all_participants) * 100))

        self.progressbar.hide()

    def ordenar(self, sortingColumn):
        if len(self.groups) > 0: 
            self.progressbar.setValue(0)
            self.progressbar.show()
            sortingColumn += 1
            row = 0
            for indice in range(len(self.all_participants)-1, 0, -1):
                for sorting in range(indice):
                    if self.all_participants[sorting][sortingColumn] > self.all_participants[indice][sortingColumn]:
                        line = self.all_participants[indice]
                        self.all_participants[indice] = self.all_participants[sorting]
                        self.all_participants[sorting] = line

                self.progressbar.setValue(int(row/len(self.all_participants) *100))
                row += 1

            self.progressbar.hide()
            self.showTable()

    #cuando cerramos cerramos el cliente
    def close(self):
        self.client.disconnect()
        super().close()

    def changeLastName(self):
        if self.all_participants[self.table.currentRow()][5]:
            self.client(functions.contacts.DeleteContactsRequest( id=[self.all_participants[self.table.currentRow()][0]])) 

        self.client(functions.contacts.AddContactRequest(
                id=self.all_participants[self.table.currentRow()][0],
                first_name=self.all_participants[self.table.currentRow()][2],
                last_name=self.buttonefective[self.table.currentRow()][1].text(),
                phone=self.table.item(self.table.currentRow(), 3).text(),
                add_phone_privacy_exception=True
        ))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("You have changed the last name of the user")
        msg.setWindowTitle("Information change")
        msg.exec_()

    def changeName(self):
        if self.all_participants[self.table.currentRow()][5]:
            self.client(functions.contacts.DeleteContactsRequest( id=[self.all_participants[self.table.currentRow()][0]])) 
        self.client(functions.contacts.AddContactRequest(
                id=self.all_participants[self.table.currentRow()][0],
                first_name=self.buttonefective[self.table.currentRow()][0].text(),
                last_name=self.all_participants[self.table.currentRow()][3],
                phone=self.table.item(self.table.currentRow(), 3).text(),
                add_phone_privacy_exception=True
        ))
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("You have changed the first name of the user")
        msg.setWindowTitle("Information change")
        msg.exec_()

    def delete(self):
        self.client.kick_participant(self.groups[self.channelList.currentIndex()], self.all_participants[self.table.currentRow()])
        target_group= self.groups[self.channelList.currentIndex()]
        self.all_participants = self.client.get_participants(target_group, aggressive=True)
        self.showTable()


app = QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()