'''database.py
主要包含对数据库操作的相关函数。
- 创建新的数据库
- 创建新的视频信息原始数据表格
- 创建新的视频分析结果表格
- 添加summary词条'''

import sqlite3

def createNewDatabase(database_name):
    '''createNewDatabase(database_name::string)
    database_name: 数据库的地址名称

    创建新的数据库，并创建summary表格'''
    conn = sqlite3.connect(database_name) # 自动创建数据库
    c = conn.cursor()

    # 创建summary表格
    c.execute("""
        CREATE TABLE IF NOT EXISTS summary (
            SessionID       TEXT PRIMARY KEY NOT NULL,
            Setup           TEXT,
            Cage            INT,
            Mouse           TEXT,
            OppositeMouse   TEXT,
            Position        TEXT,
            PositionNum     INT,
            SessionDate     INT,
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
            Weight          REAL,
            setoff          REAL,
            VideoName       TEXT
        );
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS weight (
            Cage        INT,
            CageName    TEXT,
            Mouse       TEXT,
            SessionDate INT,
            Weight      REAL,
            Food        REAL
        )""")
    conn.commit()
    conn.close()
    print("INFO: create new database file: %s"%database_name)
    return True

def createNewPoseTable(cursor, session_name, title, pose_info):
    '''createNewPoseTable(cursor::sqlite3.cursor, session_name::string, title::list, pose_info::list)
    cursor: 数据库cursor
    session_name: session的序号，即{DATE}{ID}
    title: 表头，应与ncage个数相对应，每只老鼠的title为p{ID},如，ncage=4时，title=['p1','p2','p3','p4']
    pose_info: 视频的原始数据，列表中每个元素应为list或者tuple，每个元素应包含: (frame::int, time::real, p1::real, p2::real, ...)
    '''
    try:
        # 创建表格
        cursor.execute("""
            CREATE TABLE %s (
            Frame   REAL PRIMARY KEY,
            t       REAL %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))
    except sqlite3.OperationalError: # 若已经存在该表格，则将原来的表格删去。
        cursor.execute("DROP TABLE %s;"%session_name)
        cursor.execute("""
            CREATE TABLE %s (
            Frame   INT PRIMARY KEY,
            t       REAL %s);
        """%(session_name, ''.join([ ',\n%s      REAL'%n for n in title])))

    # 生成需要执行的sql命令
    command = "INSERT INTO %s VALUES (%s)"%(session_name, "%d"+",%.3f"*(len(title)+1))
    for item in pose_info:
        cursor.execute(command%item)
    return True

def createNewSessionTable(cursor, session_name, title, session_info):
    '''createNewSessionTable(cursor::sqlite3.cursor, session_name::string, title::list, session_info::list)
    类似。

    表格主要用来保存攀爬与啃食的起始与终止时刻信息，session_info中的每个元素应包含:(id::int, start::real, end::real)'''
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

    command = "INSERT INTO %s VALUES (%s)"%(session_name, "%d"+",%.3f"*(len(title)))
    for item in session_info:
        cursor.execute(command%item)
    return True


def createNewSessionSummaryEntry(cursor, sessionID, session_summary_info):
    '''createNewSessionSummaryEntry(cursor::sqlite3.cursor, sessionID::list, session_summary_info::list)'''
    for index, each in enumerate(sessionID):
        try:
            cursor.execute("SELECT * FROM summary WHERE SessionID = %s"%each)
            cursor.fetchall()
            cursor.execute("DELETE FROM summary WHERE SessionID = %s"%each)
            print("delete former entry")
        except sqlite3.OperationalError:
            print("create new entry: ", each)
            pass

        command = """INSERT INTO summary VALUES ("%s","%s",%d,"%s","%s","%s",%d,%d,"%s",%f,"%s",%d,%.3f,%d,%.3f,%.3f,%.3f,%.3f,%.3f,%.1f,"%s")"""%(tuple(session_summary_info[index]))
        cursor.execute(command)
    return True

if __name__ == '__main__':
    createNewDatabase('chewing.db')
