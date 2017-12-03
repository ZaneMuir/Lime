from Sensor.power_protocol import main as finalmain
from Sensor.special_items import checkFile
from Sensor.poseAnalysis import poseCheck
import os,time, re
startPoint = time.time()
__doc__ = """Lime
analysis program for chewing behavior of Zhang's Lab.

Usage: lime.py [options] SENSORFILE [VIDEOFILE]

--episode=GAP               episode gap length, unit as second [default: 4]
--input=INDIR               data directory [default: data]
--output=OUTDIR             chart directory [default: chart]
--eyeDataSuffix=EYESUFFIX   eye data file suffix [default: _%d_eye_60min.csv]
--timeRange=RANGE           checking range, unit as second [default: 60_3600]
--videoOffset=OFFSET        video offset, aligning with sensor time, counts as second [default: 0.0]
"""
from docopt import docopt
arguments = docopt(__doc__, version='Lime 2.0.0')
#print(arguments)

arguments['--output'], arguments['eyeDataFile'] = checkFile(arguments['--output'],
                                                            os.path.join(arguments['--input'],arguments['SENSORFILE']),
                                                            int(arguments['--episode']),
                                                            arguments['--eyeDataSuffix'])

print(arguments)

if arguments['VIDEOFILE']:
    #videoAnalysis
    os.system('Video/videoAnalysis %s %s'%( os.path.join(arguments['--input'], arguments['VIDEOFILE']),
                                            os.path.join(arguments['--input'], '%spose.csv'%os.path.splitext(arguments['VIDEOFILE'])[0])))
    #pose analysis
    poseCheck(  os.path.join(arguments['--input'], '%spose.csv'%os.path.splitext(arguments['VIDEOFILE'])[0]),
                arguments['eyeDataFile'],
                float(arguments['--videoOffset']))

#sensor analysis
finalmain(arguments)
print('all done! %.2f'%(time.time()-startPoint))
