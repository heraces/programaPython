from PyQt5.QtCore import QAbstractTableModel, Qt
from PyQt5 import QtGui

class TableModel(QAbstractTableModel):
    def __init__(self, data, colors):
        super().__init__()
        self._data = data
        self.colorList = colors
        
    def data(self, index, role):
        if role == Qt.BackgroundRole:            
            if len(self.colorList) >= index.row():
                if self.colorList[index.row()] == 1:    
                    return QtGui.QColor(70, 240, 40, 200)
                elif self.colorList[index.row()] == 2:
                    return QtGui.QColor(230, 40, 20, 100)

        if role == Qt.DisplayRole:
            # Get the raw value
            value = self._data.iloc[index.row(), index.column()]
            return str(value)
            


    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])
            if orientation == Qt.Vertical:
                return str(self._data.index[section])

        
