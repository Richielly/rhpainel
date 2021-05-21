import sqlite3 as sql

class TransactionObject():
    database = "RH.db"
    conn = None
    cursor = None
    connected = False

    conn = sql.connect(database)
    conn.commit()
    conn.close()

    def connection(self):
        TransactionObject.conn = sql.connect(TransactionObject.database)
        return TransactionObject.conn

    def connect(self):
        TransactionObject.conn = sql.connect(TransactionObject.database)
        TransactionObject.cursor = TransactionObject.conn.cursor()
        TransactionObject.connected = True

    def disconnect(self):
        TransactionObject.conn.close()
        TransactionObject.connected = False

    def execute(self, sql, parms=None):
        if TransactionObject.connected:
            if parms == None:
                TransactionObject.cursor.execute(sql)
            else:
                TransactionObject.cursor.execute(sql, parms)
            return True
        else:
            return False

    def fetchall(self):
        return TransactionObject.cursor.fetchall()

    def persist(self):
        if TransactionObject.connected:
            TransactionObject.conn.commit()
            return True
        else:
            return False

    def view(self):
        trans = TransactionObject()
        trans.connect()
        trans.execute("SELECT f.* FROM ferias f")
        rows = trans.fetchall()
        trans.disconnect()
        return rows

    def insert(self,colaborador, setor, periodo, inicio , diasprimeiraparte, diassegundaparte, dataprimeiraparte, datasegundaparte):
        trans = TransactionObject()
        trans.connect()
        trans.execute("INSERT INTO ferias VALUES(NULL, ?,?,?,?,?,?,?,?)", (colaborador, setor, periodo, inicio , diasprimeiraparte, diassegundaparte, dataprimeiraparte, datasegundaparte))
        trans.persist()
        trans.disconnect()

    def dropTable(self):
        trans = TransactionObject()
        trans.connect()
        trans.execute("Delete FROM ferias")
        if trans.persist():
            trans.disconnect()
            return True, "Limpeza do banco feita com sucesso."
        else: return False, "Não foi possível fazer a limpeza do banco."

def createDB():
    trans = TransactionObject()
    trans.connect()
    trans.execute("CREATE TABLE IF NOT EXISTS  ferias (id INTEGER PRIMARY KEY , colaborador text, setor text, periodo text, inicio text, diasprimeiraparte text, diassegundaparte text, dataprimeiraparte text, datasegundaparte text)")
    trans.persist()
    trans.disconnect()

createDB()