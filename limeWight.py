import sqlite3
import os

__version__ = '1.0.0'
__doc__ = '''
LimeWeight {version}

Usage:
    LimeWeight.py -c CAGENUM -d DATE [options] (WEIGHTSEQ ...)

Options:
--debug         # debug mode
-c CAGENUM      # cage number
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

dateStr = arguments['DATE']
for each in range(int(arguments['-n'])):
    mouseID = 'C%sM%d'%(arguments['-c'], each+1)
    weight = arguments['WEIGHTSEQ'][each]

    command = "UPDATE summary SET Weight=%s WHERE Mouse=\"%s\" and SessionDate=\"%s\""%(weight, mouseID, dateStr)
    print(command)
    c.execute(command)

# NOTE: to add some extra scripts here

conn.commit()
conn.close()
