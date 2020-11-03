from PyQt5.QtSql import QSqlDatabase, QSql, QSqlQuery
                          
class Settings:
    
    dblocal = QSqlDatabase("QSQLITE")
    #dial_value = Null
    #click_checked = Null
    def __init__(self):
        self.dblocal.setDatabaseName("filters.sqlite")
        self.dblocal.open()
        if len(self.dblocal.tables(QSql.Tables)) == 0:
            self.createTable()

    def charge(self):
        query = QSqlQuery("SELECT name FROM filtes", db = self.dblocal)
        lista = []
        while query.next():
            lista.append(query.value(0))
        return lista

    def delete(self, item):
        query = QSqlQuery(db = self.dblocal)
        query.prepare("DELETE FROM filtes WHERE name = ?")
        query.addBindValue(item)
        query.exec_()

    def addProfile(self, name):
        query = QSqlQuery(db = self.dblocal)
        query.prepare("INSERT INTO filtes(name, serarchLine, greater, greatValue)"
                      "VALUES (:name,:serarchLine,:greater,:GV)")
        query.bindValue(":name", name)
        query.bindValue(":serarchLine","")
        query.bindValue(":greater", 0)
        query.bindValue(":GV", 0)
        query.exec_()

    def updateProfile(self, profile, lista):
        query = QSqlQuery(db = self.dblocal)
        solicitud =  "UPDATE filtes SET "
        
        for item in lista:
            if lista[item][0]:
                solicitud += item + " = :" + item + ", "

        solicitud = solicitud[:-2]
        solicitud += " WHERE name = :name"
        query.prepare(solicitud)
        for item in lista:
            if lista[item][0]:
                query.bindValue(":"+item, lista[item][1])
        query.bindValue(":name", profile)
        query.exec_()
    
    def createTable(self):
        query = QSqlQuery(db = self.dblocal)
        query.prepare("CREATE TABLE filtes (name VARCHAR(20) PRIMARY KEY NOT NULL,"
                      "serarchLine VARCHAR(19), greater BIT(1), greatValue INT)")
        query.exec_()
        
    def loadProfile(self, profile):
        query = QSqlQuery(db = self.dblocal)
        query.prepare("SELECT name, serarchLine, greater, greatValue FROM filtes WHERE name = :profile")
        query.bindValue(":profile", profile)
        query.exec_()
        lista = []
        while query.next():
            aux = 0
            while None != query.value(aux):
                lista.append(query.value(aux))
                aux+=1
        return lista