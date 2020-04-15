import argparse
import psycopg2
from Config import GetConfig
from SQLQueries import dropTables, createTables, nameTables

def CreateDatabase():
    dbParams = GetConfig("postgresql")
    conn = psycopg2.connect(host= dbParams["host"], user= dbParams["user"], password= dbParams["password"])
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    
    dropStr = "DROP DATABASE IF EXISTS {}".format(dbParams["database"])
    cur.execute(dropStr)
    
    createStr = 'CREATE DATABASE {} WITH ENCODING "utf8" TEMPLATE template0'.format(dbParams["database"])
    cur.execute(createStr)
    
    conn.close()

def GetCur():
    dbParams = GetConfig("postgresql")
    conn = psycopg2.connect(**dbParams)
    conn.set_session(autocommit=True)
    cur = conn.cursor()
    return conn, cur

def DropTable():
    conn, cur = GetCur()
    for query in dropTables[::-1]: #reverse drop for FOREIGN KEY error
        cur.execute(query)
    conn.close()

def DropTableBy(name):
    conn, cur = GetCur()
    cur.execute(dropTables[nameTables.index(name)])
    conn.close()

def CreateTable():
    conn, cur = GetCur()
    for query in createTables:
        cur.execute(query)
    conn.close()

def CreateTableWith(name):
    conn, cur = GetCur()
    cur.execute(createTables[nameTables.index(name)])
    conn.close()

def Run():
    parser = argparse.ArgumentParser(description= 'Execute Database.')
    
    parser.add_argument("-a", action= "store_true", dest= "createAll")
    parser.add_argument("-c", action= "store", nargs= "*", dest= "createTable")
    parser.add_argument("-d", action= "store", nargs= "*", dest= "dropTable")
    args = parser.parse_args()
    
    if args.createAll:
        CreateDatabase()
        CreateTable()
    
    if args.dropTable is not None:
        if len(args.dropTable) == 0:
            DropTable()
        else:
            for name in args.dropTable:
                if name in nameTables:
                    DropTableBy(name)
    
    if args.createTable is not None:
        if len(args.createTable) == 0:
            CreateTable()
        else:
            for name in args.createTable:
                if name in nameTables:
                    CreateTableWith(name)

if __name__ == "__main__":
    Run()