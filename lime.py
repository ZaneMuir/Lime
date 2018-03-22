#!/usr/bin/env python3

import LimeOne  # 模块主要包含 当前采用的处理函数，详见'LimeOne/__init__.py'。
import os
import re
import sqlite3
# 数据将存储在sql数据库中。常见的sql操作，
# 可以参考网站:https://www.tutorialspoint.com/sqlite/index.htm

__version__ = "1.2.0-dev"

# __doc__ 作为说明文档的同时，也作为docopt模块的参数，可以更直观方便的提取命令行里的参数。
__doc__ = """
Lime {version}
analysis program for chewing behavior of Zhang's Lab.

Usage:
    lime.py [options] SENSORFILE [VIDEOFILE]

Options:
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
    -s THRESHSCALE --scale=THRESHSCALE          # mean - scale*std [default: 1]
    -t TIME --startTime=TIME                    # start time point [default: HHMM]
    -u SETUP --setup=SETUP                      # setup prefix, one of "TtC_NN","TtC_NH", "TtC_HH", "TtV_NN","TtV_NH", "TtV_HH" [default: TtV_NN]
    -v OFFSET --videoOffset=OFFSET              # video offset, aligning with sensor time, counts as second [default: 0.0]
    -w WIDTH --width=WIDTH                      # target area width, unit as px [default: 20]
    -z VIDEONAME --videoName=VIDEONAME          # video name [default: NaN/NaN/NaN/NaN]

typical command for 4-mice setup:
```lime.py -d 20171213 -t 1430 -u TtC_NH -n 4 -m C1M1/C2M1/C1M2/C2M2 -v 17 -f 3.653_3.142/3.653_3.142/3.653_3.142/3.653_3.142 20171213001_PW.txt 20171213001.mov```

tips: easier for editing to write these commands into an sh file.
""".format(version=__version__)

from docopt import docopt
arguments = docopt(__doc__, version='Lime %s' % __version__)
# 使用docopt模块约定并提取命令行参数。

# 以下为docopt返回的参数信息示例，格式为dict，值得注意的是：key和value均为字符串
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
 'videoName': 'Nan',
 'SENSORFILE': '20171213001_PW.txt',
 'VIDEOFILE': '20171213001.mov'}
 '''

# debug模式输出所得到的参数值
if arguments['--debug']:
    print(arguments)
    exit(0)


if not os.path.isdir(arguments['--output']):
    os.mkdir(arguments['--output'])

# 检验数据库是否存在，如果不，则新建一个
if not os.path.exists(os.path.join(arguments['--input'], arguments['--database'])):
    LimeOne.createNewDatabase(os.path.join(arguments['--input'], arguments['--database']))

# 与数据库链接，并获取cursor。cursor作为之后几乎所有的数据库操作的门户。
conn = sqlite3.connect(os.path.join(arguments['--input'], arguments['--database']))
dbCursor = conn.cursor()

# data pre-parsing
# TODO

sessionName = re.findall(r"(\d{11})_PW\.txt",arguments['SENSORFILE'])[0] # 基于传感器文件名获取本session的名字：即{DATE}{ID},如20171213001
mice = re.split("/",arguments['--miceSequence']) # 获取每只老鼠的名称
setups = re.split("/",arguments['--setup'])
setups_index = lambda x:int(x / 2)
# 生成每只老鼠的sessionID，如'TtC_NN_C1M1_L_20171213_1330_60'
sessionID = [   setups[setups_index(i)] + \
                '_' + mice[i] + ('_L_' if i%2 == 0 else '_R_') + \
                arguments['--date'] + '_'+arguments['--startTime'] + \
                '_' + arguments['--length']\
                for i in range(int(arguments['--cageSum']))]
oppositeMouseIndex = lambda x:x+(-1)**x # 对面小鼠index的生成函数

# 如果输入了视频文件，则分析视频。
if arguments['VIDEOFILE']:
    #　videoAnalysis
    print("step 1/4: video analysis")
    # 视频分析的主要方法，详见'LimeOne/video.py'
    LimeOne.videoMain(os.path.join(arguments['--input'],
                                   arguments['VIDEOFILE']),  # 视频文件的绝对路径
                      dbCursor,                           # sql cursor
                      "POSE_"+sessionName,  # sql 表格的名称，POSE_{SESSIONNAME}
                      ncage=int(arguments['--cageSum']),  # 该session中的笼数
                      width=int(arguments['--width']))  # 采样宽度，默认值为20个像素，上下各10个

    conn.commit() 　# 提交数据库的更新
else:
    print("step 1/4: video analysis, SKIP")

# 对视频选取的数据是否需要分析
if arguments['--poseAnalysis'] == 'True':
    print("step 2/4: pose analysis")
    # 视频数据的分析，详见'LimeOne/poseAnalysis.py'
    LimeOne.poseCheck(dbCursor,
                      sessionName,
                      sessionID,
                      offset=float(arguments['--videoOffset']),  # 视频中“开始”的时刻
                      output=arguments['--output'],              # 图像输出的目录
                      ncage=int(arguments['--cageSum']),         # 该session中的笼数
                      scale=float(arguments['--scale']))
    conn.commit()
else:
    print('step 2/4: pose analysis, SKIP')

# 传感器数据处理，详见'LimeOne/sensor.py'
print('step 3/4: sensor analysis')
LimeOne.sensorDB(os.path.join(arguments['--input'], arguments['SENSORFILE']),
                 arguments['--timeRange'],
                 sessionID,
                 float(arguments['--episode']),
                 dbCursor)
conn.commit()

# TODO result demonstration and summary entry creation
print('step 4/4: final analysis')
# 整合传感器与视频的信息，详见'LimeOne/videoOverSensor.py'
result = LimeOne.finalMain(sessionID,
                           dbCursor,
                           duration=int(arguments['--length']),
                           output=arguments['--output'])
conn.commit()

# 生成summary表格中的条目信息，详见'LimeOne/database.py'
video_name_list = re.split("/", arguments['--videoName'])
session_summary_info = []
Foods = [[float(subitem) for subitem in re.split('_', item)] for item in
         re.split('/', arguments['--food'])]
for index, each in enumerate(sessionID):
    item = [each]  # session ID
    item.append(setups[setups_index(index)])
    item.append(int(re.findall(r'C(\d+)M\d+', mice[index])[0]))  # cage number
    item.append(mice[index])  # mouse
    item.append(mice[oppositeMouseIndex(index)])  # OppositeMouse
    item.append(('L' if index % 2 == 0 else 'R'))  # Position
    item.append(index+1)  # position NUM
    item.append(int(arguments['--date']))
    item.append(arguments['--startTime'])
    item.append(int(arguments['--length']))
    item.append(arguments['--timeRange'])
    item.append(result[index][0])
    item.append(result[index][1])
    item.append(result[index][2])
    item.append(result[index][3])
    FoodBefore, FoodAfter = Foods[index]
    item.append(FoodBefore)
    item.append(FoodAfter)
    item.append(FoodBefore-FoodAfter)
    item.append(-1)
    item.append(float(arguments['--videoOffset']))
    item.append(video_name_list[index])
    session_summary_info.append(item)

# print(session_summary_info)
LimeOne.createNewSessionSummaryEntry(dbCursor, sessionID, session_summary_info)
# close database
conn.commit()
conn.close()
print('ALL DONE!')
