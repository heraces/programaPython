
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot
from externDatabase import Database

class OrdererSignals(QObject):
    progress = pyqtSignal(int)
    finished = pyqtSignal()

class DbSignals(QObject):
    progress = pyqtSignal(int)
    data = pyqtSignal(list)

class ClasesSignals(QObject):
    data = pyqtSignal(list)
    
class Orderer(QRunnable):
    def __init__(self, datos, columna):
        super().__init__()
        # Store constructor arguments (re-used for processing)
        self.signals = OrdererSignals()
        self.datos = datos
        self.sortingColumn = columna

    @pyqtSlot()
    def run(self):
        for indice in range(len(self.datos)-1, 0, -1):
            for sorting in range(indice):
                if self.sortingColumn == 0:
                    first = self.datos[indice][0][-4:] + self.datos[indice][0][3:5] + self.datos[indice][0][:2]
                    second = self.datos[sorting][0][-4:] + self.datos[sorting][0][3:5] + self.datos[sorting][0][:2]
                    if int(first) < int(second):
                        line = self.datos[indice]
                        self.datos[indice] = self.datos[sorting]
                        self.datos[sorting] = line

                elif isinstance(self.datos[sorting][self.sortingColumn], float) or isinstance(self.datos[sorting][self.sortingColumn], int):
                        if isinstance(self.datos[indice][self.sortingColumn], str):
                            line = self.datos[indice]
                            self.datos[indice] = self.datos[sorting]
                            self.datos[sorting] = line
                        elif self.datos[sorting][self.sortingColumn] > self.datos[indice][self.sortingColumn]:
                            line = self.datos[indice]
                            self.datos[indice] = self.datos[sorting]
                            self.datos[sorting] = line

                elif (isinstance(self.datos[sorting][self.sortingColumn], str) and isinstance(self.datos[indice][self.sortingColumn], str) and
                        self.datos[sorting][self.sortingColumn] > self.datos[indice][self.sortingColumn]):
                        line = self.datos[indice]
                        self.datos[indice] = self.datos[sorting]
                        self.datos[sorting] = line

            if(indice%100 == 0):
                self.signals.progress.emit(100-int(indice/len(self.datos) * 100))
            
        self.signals.finished.emit()

class ChargeDatabase(QRunnable):
    def __init__(self, query):
        super().__init__()
        self.signals = DbSignals()
        self.query = query

    @pyqtSlot()
    def run(self):
        datos =[]
        db = Database()
        rows = db.query(self.query)
        self.signals.progress.emit(50)
        self.teams = db.query("SELECT * FROM TEAMS ORDER BY ascii(ID) ASC")

        minDate = rows[0]["DATE"]
        maxDate = rows[0]["DATE"]
        leagues = []
        for row in rows:   

            if minDate > row["DATE"]:
                minDate = row["DATE"]
            elif maxDate < row["DATE"]:
                maxDate = row["DATE"]
            if row["ID_LEAGUE"] not in leagues:
                leagues.append(row["ID_LEAGUE"])

            maRalla = []
            maRalla.append(self.getDate(row["DATE"]))
            maRalla.append(self.getTime(row["TIME"]))
            maRalla.append(self.findName(row["ID_HOME"]))
            maRalla.append(self.findName(row["ID_AWAY"]))
            maRalla.append(self.getResultado(row))
            maRalla.append(self.getTheGlobalHomePercentage(row))
            maRalla.append(self.getTheGlobalAwayPercentage(row))
            maRalla.append(self.getTheHomePercentage(row))
            maRalla.append(self.getTheAwayPercentage(row))
            maRalla.append(self.getTotalGoalsInGame(row))
            maRalla.append(self.getPPGHome(row))
            maRalla.append(self.getPPGAway(row))
            maRalla.append(self.getPJHome(row))
            maRalla.append(self.getPJAway(row))
            maRalla.append(row["REH"])
            maRalla.append(row["REA"])
            maRalla.append(row["REHH"])
            maRalla.append(row["REAA"])
            maRalla.append(row["ODDS_1"])
            maRalla.append(row["ODDS_2"])
            maRalla.append(row["ODDS_UNDER25FT"])
            maRalla.append(row["ID_LEAGUE"])

            datos.append(maRalla)
            if(len(datos) % 1000):
                self.signals.progress.emit(len(datos)/len(rows)*50 + 50)

        self.signals.data.emit([datos, minDate, maxDate, leagues])
        del db


    
    def findName(self, targetID):
        primero = 0
        ultimo = len(self.teams)-1
        medio = int(ultimo/2)
        while primero <= ultimo:
            if targetID == self.teams[medio]["ID"]:
                return self.teams[medio]["NAME"]

            if targetID > self.teams[medio]["ID"]:
                primero = medio+1
            else:
                ultimo = medio-1
            medio = int((ultimo+primero)/2)
        return ""

    
    def getDate(self, fecha):
        return fecha[6:] + "/" + fecha[4:6] + "/" + fecha[:4]


    def getTime(self, fecha):
        while len(fecha) < 4:
             fecha = "0" + fecha
        return fecha[:2] + " : " + fecha[2:]


    def getTheGlobalHomePercentage(self, row):
        if row["HW"] + row["HD"]+ row["HL"] != 0:
            return round(row["HD"] / (row["HW"] + row["HD"]+ row["HL"]) * 100, 3)

        return "N/D"

    def getTheGlobalAwayPercentage(self, row):

        if row["AW"] + row["AD"]+ row["AL"] != 0:
            return round(row["AD"] / (row["AW"] + row["AD"]+ row["AL"]) * 100, 3)

        return "N/D"

    def getTheHomePercentage(self, row):
        if row["HHW"] + row["HHD"]+ row["HHL"] != 0:
            return round(row["HHD"] / (row["HHW"] + row["HHD"]+ row["HL"]) * 100, 3)

        return "N/D"

    def getTheAwayPercentage(self, row):
        if row["AAW"] + row["AAD"]+ row["AAL"] != 0:
            return round(row["AAD"] / (row["AAW"] + row["AAD"]+ row["AAL"])* 100, 3) 

        return "N/D"

    def getTotalGoalsInGame(self, row):
        if row["AW"] + row["AD"]+ row["AL"] != 0 or row["HW"] + row["HD"]+ row["HL"] != 0:
            a = 0
            b = 0
            if row["HW"] + row["HD"]+ row["HL"] != 0:
                a = (row["GOALSGH"] + row["GOALCGH"]) / (row["HW"] + row["HD"]+ row["HL"])
            if row["AW"] + row["AD"]+ row["AL"] != 0:
                b = (row["GOALSGH"] + row["GOALCGH"]) / (row["AW"] + row["AD"]+ row["AL"])
            
            return round(((a+b)/2), 3)

        return "N/D"

    def getPPGHome(self, row):
        if row["HW"] + row["HD"]+ row["HL"] != 0:
            return round((3*row["HW"] + row["HD"])/(row["HW"] + row["HD"]+ row["HL"]), 3)
        return "N/D"

    def getPPGAway(self, row):
        if row["AW"] + row["AD"]+ row["AL"] != 0:
            return round((3*row["AW"] + row["AD"])/(row["AW"] + row["AD"]+ row["AL"]), 3)
        return "N/D"

    def getPJHome(self, row):
        return row["HW"] + row["HD"]+ row["HL"]

    def getPJAway(self, row):
        return row["AW"] + row["AD"]+ row["AL"]

    def getResultado(self, row):
        if row["FTHG"] < 0:
            return "N/D"
        return str(row["FTHG"]) + " - " + str(row["FTAG"])

class GetTeams(QRunnable):
    def __init__(self):
        super().__init__()
        self.signals = ClasesSignals()

    @pyqtSlot()
    def run(self):
        db = Database()
        self.signals.data.emit(db.query("""SELECT ID_LEAGUE, LEAGUE_PLAYED, LEAGUE_DRAWS FROM FIXTURES GROUP BY ID_LEAGUE"""))
        del db