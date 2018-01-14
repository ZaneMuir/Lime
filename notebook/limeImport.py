import sqlite3
import pandas as pd
import re
def getSQLTable(table_name, database, showSchema=False):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    c.execute("SELECT * FROM %s"%table_name)
    data = c.fetchall()

    c.execute("SELECT sql FROM sqlite_master WHERE name = \"%s\""%table_name)
    titlestr =c.fetchall()[0][0]
    
    if showSchema:
        print(titlestr)

    title = re.split(",",re.findall(r"\((.*?)\)", re.sub(r"\s","",re.sub(r"CREATE|TABLE|TEXT|INT|REAL|KEY|PRIMARY|NOT|NULL","",titlestr)))[0])

    result = pd.DataFrame(data,columns=title)
    conn.close()
    return result

def getSQLTableList(cursor):
    cursor.execute("SELECT name FROM sqlite_master WHERE type = \"table\";")
    result = cursor.fetchall()
    return [item[0] for item in result]


if __name__ == '__main__':
    #conn = sqlite3.connect("data/chewing.db")
    #c = conn.cursor()
    print(getSQLTable("summary", "data/chewing.db"))
    #print(getSQLTableList(c))
    #conn.close()
