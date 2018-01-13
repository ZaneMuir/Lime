#!/usr/bin/env python3
# backup data with a hard drive

import sqlite3

def backupDataBase(ffrom, fto):
    connFrom = sqlite3.connect(ffrom)
    cursorFrom = connFrom.cursor()
    connTo = sqlite3.connect(fto)
    cursorTo = connTo.cursor()

    #TODO get list
    command = "SELECT name FROM sqlite_master WHERE type=\"table\";"
    cursorFrom.execute(command)
    fromList = cursorFrom.fetchall()[0]

    cursorTo.execute(command)
    toList = cursorTo.fetchall()[0]

    #TODO find: new, deleted, changed
    for item in toList:
        if item not in fromList:
            cursorTo.execute("DROP TABLE %s;"%item)

    for item in fromList:
        if item not in toList:
            cursorFrom.execute("SELECT sql FROM sqlite_master WHERE type = 'table' AND name = '%s'"%item)
            tableschema = cursorFrom.fetchall()[0][0]
            cursorTo.executescript(tableschema+';')

            #TODO



    #TODO back



if __name__ == '__main__':
    __doc__ = '''
    limeBackup

    Usage: limeBackup.py [options] SOURCE TARGET

    Options:
        --debug     #debug mode'''

    from docopt import docopt
    arguments = docopt(__doc__)

    if arguments['--debug']:
        print(arguments)

    backupDataBase(arguments['SOURCE'], arguments['TARGET'])
