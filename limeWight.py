import sqlite3
import os, time

__version__ = '1.0.0'
__doc__ = '''
LimeWeight {version}

Usage:
    LimeWeight.py [options] -c CAGENUM WEIGHTSEQ ...
    LimeWeight.py [options] --nw NAMEWEIGHTSEQ ...

Options:
--debug         # debug mode
-c CAGENUM      # cage number
-d DATE         # dateStr
-n NMICE        # total mice sum [default: 8]
-i INPUTDIR     # input data directory [default: data]
-f DATABASE     # database file [default: chewing.db]

'''.format(version = __version__)

from docopt import docopt
arguments = docopt(__doc__, version=__version__)

if arguments['--debug']:
    print(arguments)

conn = sqlite3.connect(os.path.join(arguments['-i'], arguments['-f']))
c = conn.cursor()

dateStr = arguments['-d'] or time.strftime("%Y%m%d")

if not arguments['--nw']:
    for each in range(int(arguments['-n'])):
        mouseID = 'C%sM%d'%(arguments['-c'], each+1)
        weight = arguments['WEIGHTSEQ'][each]

        command = "UPDATE summary SET Weight=%s WHERE Mouse=\"%s\" and SessionDate=\"%s\""%(weight, mouseID, dateStr)
        print(command)
        c.execute(command)
else:
    if len(arguments['NAMEWEIGHTSEQ']) % 2 == 1: raise ValueError("invalid input data:"+arguments['NAMEWEIGHTSEQ'].__str__()+'\nnumber of elements shall be even.')
    for index in range(len(arguments['NAMEWEIGHTSEQ']) // 2):
        mouseID = arguments['NAMEWEIGHTSEQ'][index * 2]
        weight = arguments['NAMEWEIGHTSEQ'][index * 2 + 1]

        c.execute("SELECT Weight From summary WHERE Mouse=\"%s\" and SessionDate=\"%s\";"%(mouseID, dateStr))
        if len(c.fetchall()) == 0:
            print("WARNING: NO ENTRY FOR MOUSE(%s)! process lime.py for Mouse(%s) first please."%(mouseID,mouseID))
        else:
            command = "UPDATE summary SET Weight=%s WHERE Mouse=\"%s\" and SessionDate=\"%s\";"%(weight, mouseID, dateStr)
            print(command)
            c.execute(command)

# NOTE: to add some extra scripts here
conn.commit()
conn.close()
