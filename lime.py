from Sensor.power_protocol import main as sensorMain
from Sensor.special_items import checkFile
from Sensor.poseAnalysis import poseCheck_line as poseCheck
from Sensor.video import main as videoMain
from Sensor.videoOverSensor import main as finalMain
from Sensor.climbInfo import main as climbInfo
import os,time, re
startPoint = time.time()
__version__ = "1.1.2"
__doc__ = """
Lime {version}
analysis program for chewing behavior of Zhang's Lab.

Usage: lime.py [options] SENSORFILE [VIDEOFILE]

-i INDIR --input=INDIR                  # data directory [default: data]
-o OUTDIR --output=OUTDIR               # chart directory [default: chart]
-v OFFSET --videoOffset=OFFSET          # video offset, aligning with sensor time, counts as second [default: 0.0]
-e GAP --episode=GAP                    # episode gap length, unit as second [default: 4]
-c GAP --climbEpisode=GAP               # climbing episode gap length, unit as second [default: 0]
-t RANGE --timeRange=RANGE              # checking range, unit as second [default: 60_3600]
-d, --debug                             # debug mode
-p POSEANA --poseAnalysis=POSEANA       # need pose analysis only? [default: True]
-s EYESUFFIX --eyeDataSuffix=EYESUFFIX  # eye data file suffix [default: _%d_eye_60min.csv]
""".format(version=__version__)
from docopt import docopt
arguments = docopt(__doc__, version='Lime %s'%__version__)
#print(arguments)

arguments['--output'], arguments['eyeDataFile'] = checkFile(arguments['--output'],
                                                            os.path.join(arguments['--input'],arguments['SENSORFILE']),
                                                            int(arguments['--episode']),
                                                            arguments['--eyeDataSuffix'])

if arguments['--debug']:
    print(arguments)

if arguments['VIDEOFILE']:
    #videoAnalysis
    videoMain(  os.path.join(arguments['--input'], arguments['VIDEOFILE']),
                os.path.join(arguments['--input'], '%s_pose.csv'%os.path.splitext(arguments['SENSORFILE'])[0]))

    #os.system('Video/videoAnalysis %s %s'%( os.path.join(arguments['--input'], arguments['VIDEOFILE']),
    #                                        os.path.join(arguments['--input'], '%spose.csv'%os.path.splitext(arguments['VIDEOFILE'])[0])))
    #pose analysis
    arguments['--poseAnalysis'] == 'True'

if arguments['--poseAnalysis'] == 'True':
    print("pose analysis")
    poseCheck(  os.path.join(arguments['--input'], '%s_pose.csv'%os.path.splitext(arguments['SENSORFILE'])[0]),
                arguments['eyeDataFile'],
                float(arguments['--videoOffset']))
else:
    print('skip')

#sensor analysis
sensorMain(arguments)

ChewFilePath = os.path.join(arguments['--output']+'%d','bout_time_CH_%d.csv')

print("-"*12,"result","-"*12)
duration, count = finalMain(  ChewFilePath=ChewFilePath%(0,0),
            EyeFilePath=arguments['eyeDataFile']%0,
            outputName=arguments['--output']+'0')
climb_count, climb_duration, _ = climbInfo(arguments['eyeDataFile']%0, int(arguments['--climbEpisode']))
print("Channel 0 [left mouse]: \nchewing count: %d\nchewing duration: %.2f"%(count,duration))
print("climbing count: %d\nclimbing duration: %.2f\n"%(climb_count,climb_duration))

duration, count = finalMain(  ChewFilePath=ChewFilePath%(1,1),
            EyeFilePath=arguments['eyeDataFile']%1,
            outputName=arguments['--output']+'1')
climb_count, climb_duration, _ = climbInfo(arguments['eyeDataFile']%1, int(arguments['--climbEpisode']))
print("Channel 1 [right mouse]: \nchewing count: %d\nchewing duration: %.2f"%(count,duration))
print("climbing count: %d\nclimbing duration: %.2f"%(climb_count,climb_duration))
print("-"*32)
print('all done! %.2f'%(time.time()-startPoint))
