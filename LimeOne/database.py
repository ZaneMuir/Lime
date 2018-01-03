import sqlite3

def createNewDatabase(database_name):
    conn = sqlite3.connect(database_name)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE summary (
            SessionID       TEXT PRIMARY KEY NOT NULL,
            Cage            INT,
            Mouse           TEXT,
            OppositeMouse   TEXT,
            Position        TEXT,
            PositionNum     INT,
            SessionDate     TEXT,
            StartTime       TEXT,
            Duration        REAL,
            AnalysisLength  TEXT,
            ChewCount       INT,
            ChewTime        REAL,
            ClimbCount      INT,
            ClimbTime       REAL,
            FoodBefore      REAL,
            FoodAfter       REAL,
            Food            REAL,
            Weight          REAL
        );
    """)
    conn.commit()
    conn.close()
    print("INFO: create new database file: %s"%database_name)
    return True

def createNewPoseTable(cursor, session_name, title, pose_info):
    try:
        cursor.execute("""
            CREATE TABLE %s (
            Frame   REAL PRIMARY KEY,
            t       REAL %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))
    except sqlite3.OperationalError:
        cursor.execute("DROP TABLE %s;"%session_name)
        cursor.execute("""
            CREATE TABLE %s (
            Frame   INT PRIMARY KEY,
            t       REAL %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))

    command = "INSERT INTO %s VALUES (%s)"%(session_name, "%d"+",%f"*(len(title)+1))
    for item in pose_info:
        cursor.execute(command%item)
    return True

def createNewSessionTable(cursor, session_name, title, session_info):
    try:
        cursor.execute("""
            CREATE TABLE %s (
            No    Int PRIMARY KEY %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))
    except sqlite3.OperationalError:
        cursor.execute("DROP TABLE %s;"%session_name)
        cursor.execute("""
            CREATE TABLE %s (
            No    Int PRIMARY KEY %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))

    command = "INSERT INTO %s VALUES (%s)"%(session_name, "%d"+",%f"*(len(title)))
    for item in session_info:
        cursor.execute(command%item)
    return True


def createNewSessionSummaryEntry(cursor, sessionID, session_summary_info):
    for index, each in enumerate(sessionID):
        try:
            cursor.execute("SELECT * FROM summary WHERE SessionID = %s"%each)
            cursor.fetchall()
            cursor.execute("DELETE FROM summary WHERE SessionID = %s"%each)
        except sqlite3.OperationalError:
            pass

        command = """INSERT INTO summary VALUES ("%s",%d,"%s","%s","%s",%d,"%s","%s",%f,"%s",%d,%f,%d,%f,%f,%f,%f,%f)"""%(tuple(session_summary_info[index]))
        cursor.execute(command)
    return True
