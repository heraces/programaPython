from PyQt5.QtWidgets import QTableWidget, QHeaderView, QTableWidgetItem
from PyQt5.QtCore import Qt


class CustomTableWidget(QTableWidget):
    def __init__(self):
        super(CustomTableWidget, self).__init__()
        #creamos la tablewidget como hicimos antes
        self.horizontalHeader().setSectionsClickable(True)
        self.setColumnCount(21)
        self.setHorizontalHeaderLabels(["Date", "Time", "Home team", "Away team",  "Resultado", "PGHD", "PGAD", "PHD", "PAD",
            "TGPG", "PPGHome", "PPGAway", "PJHome", "PJAway", "REH", "REA","REHH","REAA", "ODD1", "ODD2", "ODD UNDER 25"])
        
        self.horizontalHeader().resizeSection(0, 90)
        self.horizontalHeader().resizeSection(1, 55)
        self.horizontalHeader().resizeSection(4, 80)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)

        #second table
        self.secondTable = QTableWidget(self)        
        self.secondTable.setColumnCount(5)
        self.secondTable.setHorizontalHeaderLabels(["Date", "Time", "Home team", "Away team",  "Resultado"])
        self.secondTable.horizontalHeader().resizeSection(0, 90)
        self.secondTable.horizontalHeader().resizeSection(1, 55)
        self.secondTable.horizontalHeader().resizeSection(4, 80)

        #el resize del tablewidget se pasa al secondTable
        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)

        #si se mueve una se mueve la otra
        self.secondTable.verticalScrollBar().valueChanged.connect(self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(self.secondTable.verticalScrollBar().setValue)

        #set up de la secondTable
        self.secondTable.setFocusPolicy(Qt.NoFocus)
        self.secondTable.verticalHeader().hide()
        self.secondTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.viewport().stackUnder(self.secondTable) 

        self.updateFrozenTableGeometry()

        self.secondTable.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.secondTable.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        self.secondTable.setVerticalScrollMode(self.ScrollPerPixel)


    #metodos para sincronizar las dos tablas
    def updateSectionWidth(self, logicalIndex, oldSize, newSize):
        if logicalIndex == 0:
            self.secondTable.setColumnWidth(0, newSize) 
            self.secondTable.setColumnWidth(1, newSize) 
            self.secondTable.setColumnWidth(2, newSize) 
            self.secondTable.setColumnWidth(3, newSize) 
            self.secondTable.setColumnWidth(4, newSize) 
            self.updateFrozenTableGeometry()

    def updateSectionHeight(self, logicalIndex, oldSize, newSize):
        self.secondTable.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event):
        super(CustomTableWidget, self).resizeEvent(event)
        self.updateFrozenTableGeometry()

    def updateFrozenTableGeometry(self):
        self.secondTable.setGeometry(
                self.verticalHeader().width() + self.frameWidth(),
                self.frameWidth(), self.columnWidth(0)+self.columnWidth(1)+self.columnWidth(2)+self.columnWidth(3)+self.columnWidth(4),
                self.viewport().height() + self.horizontalHeader().height())

    def moveCursor(self, cursorAction, modifiers):
        current = super(CustomTableWidget, self).moveCursor(cursorAction, modifiers)
        if (cursorAction == self.MoveLeft and self.current.column() > 0 and
                 self.visualRect(current).topLeft().x() < self.secondTable.columnWidth(0)):
            
            newValue = (self.horizontalScrollBar().value() + self.visualRect(current).topLeft().x() -
                        self.secondTable.columnWidth(0))

            self.horizontalScrollBar().setValue(newValue)
        return current
   

    def setItems(self, datos):
        self.setRowCount(len(datos))
        self.secondTable.setRowCount(len(datos))

        fila = 0
        for row in datos:
            self.secondTable.setItem(fila, 0, QTableWidgetItem(str(row[0])))
            self.secondTable.setItem(fila, 1, QTableWidgetItem(str(row[1])))
            self.secondTable.setItem(fila, 2, QTableWidgetItem(str(row[2])))
            self.secondTable.setItem(fila, 3, QTableWidgetItem(str(row[3])))
            self.secondTable.setItem(fila, 4, QTableWidgetItem(str(row[4])))

            self.setItem(fila, 0, QTableWidgetItem(str(row[0])))
            self.setItem(fila, 1, QTableWidgetItem(str(row[1])))
            self.setItem(fila, 2, QTableWidgetItem(str(row[2])))
            self.setItem(fila, 3, QTableWidgetItem(str(row[3])))
            self.setItem(fila, 4, QTableWidgetItem(str(row[4])))
            self.setItem(fila, 5, QTableWidgetItem(str(row[5])))
            self.setItem(fila, 6, QTableWidgetItem(str(row[6])))
            self.setItem(fila, 7, QTableWidgetItem(str(row[7])))
            self.setItem(fila, 8, QTableWidgetItem(str(row[8])))
            self.setItem(fila, 9, QTableWidgetItem(str(row[9])))
            self.setItem(fila, 10, QTableWidgetItem(str(row[10])))
            self.setItem(fila, 11, QTableWidgetItem(str(row[11])))
            self.setItem(fila, 12, QTableWidgetItem(str(row[12])))
            self.setItem(fila, 13, QTableWidgetItem(str(row[13])))
            self.setItem(fila, 14, QTableWidgetItem(str(row[14])))
            self.setItem(fila, 15, QTableWidgetItem(str(row[15])))
            self.setItem(fila, 16, QTableWidgetItem(str(row[16])))
            self.setItem(fila, 17, QTableWidgetItem(str(row[17])))
            self.setItem(fila, 18, QTableWidgetItem(str(row[18])))
            self.setItem(fila, 19, QTableWidgetItem(str(row[19])))
            self.setItem(fila, 20, QTableWidgetItem(str(row[20])))

            fila += 1
                     

        #creamos modelo
        self.secondTable.show()

    def daColor(self, lista):
        pass