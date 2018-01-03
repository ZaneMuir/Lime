import LimeOne
import os,time, re
import sqlite3
import numpy as np
startPoint = time.time()
__version__ = "1.2.0"
__doc__ = """
Lime {version}
analysis program for chewing behavior of Zhang's Lab.

Usage:
    lime.py [options] SENSORFILE [VIDEOFILE]


-b DATABASENAME --database=DATABASENAME     # database file path [default: chewing.db]
-c GAP --climbEpisode=GAP                   # climbing episode gap length, unit as second [default: 0]
--debug                                     # debug mode
-d DATE --date=DATE                         # session date [default: YYYYMMDD]
-e GAP --episode=GAP                        # episode gap length, unit as second [default: 4]
-f FOOD --food=FOOD                         # food weight data, unit as gram [default: 2.000_1.000]
-i INDIR --input=INDIR                      # data directory [default: data]
-l LENGTH --length=LENGTH                   # session length, unit as minute [default: 60]
-m MICESEQ --miceSequence=MICESEQ           # mice sequence, from left to right [default: C1M1/C1M2/C1M3/C1M4]
-n NCAGE --cageSum=NCAGE                    # total mice number in this session [default: 2]
-o OUTDIR --output=OUTDIR                   # chart directory [default: chart]
-p POSEANA --poseAnalysis=POSEANA           # need pose analysis only? [default: True]
-r RANGE --timeRange=RANGE                  # checking range, unit as second [default: 60_3600]
-t TIME --startTime=TIME                    # start time point [default: HHMM]
-u SETUP --setup=SETUP                      # setup prefix, one of "TtC_NN","TtC_NH", "TtC_HH", "TtV_NN","TtV_NH", "TtV_HH" [default: TtV_NN]
-v OFFSET --videoOffset=OFFSET              # video offset, aligning with sensor time, counts as second [default: 0.0]
-w WIDTH --width=WIDTH                      # target area width, unit as px [default: 20]
""".format(version=__version__)

from docopt import docopt
arguments = docopt(__doc__, version='Lime %s'%__version__)

'''
{'--cageSum': '4',
 '--climbEpisode': '0',
 '--database': None,
 '--date': '20171213',
 '--debug': True,
 '--episode': '4',
 '--food': '3.653_3.142',
 '--input': 'data',
 '--length': '60',
 '--miceSequence': 'C1M1/C2M1/C1M2/C2M2',
 '--output': 'chart',
 '--poseAnalysis': 'True',
 '--setup': 'TtC_NH',
 '--startTime': '1430',
 '--timeRange': '60_3600',
 '--videoOffset': '17',
 '--width': '20',
 'SENSORFILE': '20171213001_PW.txt',
 'VIDEOFILE': '20171213001.mov'}
 '''


if arguments['--debug']:
    print(arguments)


# check database file
if not os.path.exists(os.path.join(arguments['--input'], arguments['--database'])):
    LimeOne.createNewDatabase(os.path.join(arguments['--input'], arguments['--database']))

# connect with database
conn = sqlite3.connect(os.path.join(arguments['--input'], arguments['--database']))
dbCursor = conn.cursor()

# data pre-parsing
# TODO

sessionName = re.findall(r"(\d{11})_PW\.txt",arguments['SENSORFILE'])[0]
mice = re.split("/",arguments['--miceSequence'])
sessionID = [   arguments['--setup'] + \
                '_' + mice[i] + ('_L_' if i%2 == 0 else '_R_') + \
                arguments['--date'] + '_'+arguments['--startTime'] + \
                '_' + arguments['--length']\
                for i in range(int(arguments['--cageSum']))]
oppositeMouseIndex = lambda x:x+(-1)**x


if arguments['VIDEOFILE']:
    #videoAnalysis
    print("step 1/4: video analysis")
    LimeOne.videoMain(  os.path.join(arguments['--input'], arguments['VIDEOFILE']), # absolute path of video file
                        dbCursor, # sql cursor
                        "POSE_"+os.path.splitext(arguments['VIDEOFILE'])[0], # sql table name
                        ncage=int(arguments['--cageSum']), # total cage number
                        width=int(arguments['--width'])) # sampling width, default 20 pixels, ie. p0 ± 10 px.
else:
    print("step 1/4: video analysis, SKIP")


if arguments['--poseAnalysis'] == 'True':
    print("step 2/4: pose analysis")
    LimeOne.poseCheck(  dbCursor,
                        sessionName,
                        sessionID,
                        offset=float(arguments['--videoOffset']),
                        output=arguments['--output'],
                        ncage=int(arguments['--cageSum']))
else:
    print('step 2/4: pose analysis, SKIP')

#sensor analysis
print('step 3/4: sensor analysis')
LimeOne.sensorDB(   os.path.join(arguments['--input'],arguments['SENSORFILE']),
                    arguments['--timeRange'],
                    sessionID,
                    float(arguments['--episode']),
                    dbCursor
                    )



#TODO result demonstration and summary entry creation
print('step 4/4: final analysis')
result = LimeOne.finalMain(  sessionID,
                             dbCursor,
                             duration = int(arguments['--length']),
                             output=arguments['--output'])

session_summary_info = []
for index, each in enumerate(sessionID):
    item = [each] # session ID
    item.append(int(re.findall(r'C(\d+)M\d+',mice[index])[0])) # cage number
    item.append(mice[index]) # mouse
    item.append(mice[oppositeMouseIndex(index)]) #OppositeMouse
    item.append(('L' if index%2 == 0 else 'R')) #Position
    item.append(index+1) # position NUM
    item.append(arguments['--date'])
    item.append(arguments['--startTime'])
    item.append(int(arguments['--length']))
    item.append(arguments['--timeRange'])
    item.append(result[index][0])
    item.append(result[index][1])
    item.append(result[index][2])
    item.append(result[index][3])
    FoodBefore, FoodAfter = re.split("_",arguments['--food'])
    item.append(float(FoodBefore))
    item.append(float(FoodAfter))
    item.append(float(FoodBefore)-float(FoodAfter))
    item.append(-1)
    session_summary_info.append(item)

'''CREATE TABLE summary (
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
);'''

LimeOne.createNewSessionSummaryEntry(dbCursor, sessionID, session_summary_info)
# close database
conn.commit()
conn.close()
print('ALL DONE!')
