import mysql.connector

config = {
  'user': 'u370804460_flashscordavid',
  'password': 'FLasH$David2',
  'host': 'sql168.main-hosting.eu',
  'database': 'u370804460_flashscordavid',
  'raise_on_warnings': True
}        

class Database:
    
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(**config)
            self.cursor = self.connection.cursor()
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
        

    def querydb(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()
            return True
        except mysql.connector.Error as err:
            print(err)
            self.connection.rollback()
            return False

    def query(self, query):
        cursor = self.connection.cursor( dictionary=True )
        cursor.execute(query)
        return cursor.fetchall() 
        
    def queryTeamArg(self, args):
        cursor = self.connection.cursor( dictionary=True )
        cursor.execute("SELECT NAME FROM TEAMS WHERE ID = %s", (args,))

        return cursor.fetchall()
    
    def __del__(self):
        self.connection.close()