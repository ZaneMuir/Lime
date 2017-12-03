# Lime
analysis program for chewing behavior of Zhang's Lab.

if you are using Windows, you have to build the ```videoAnalysis``` by yourself.

## usage
```
Lime
analysis program for chewing behavior of Zhang's Lab.

Usage: lime.py [options] SENSORFILE [VIDEOFILE]

--episode=GAP               episode gap length, unit as second [default: 4]
--input=INDIR               data directory [default: data]
--output=OUTDIR             chart directory [default: chart]
--eyeDataSuffix=EYESUFFIX   eye data file suffix [default: _%d_eye_60min.csv]
--timeRange=RANGE           checking range, unit as second [default: 60_3600]
--videoOffset=OFFSET        video offset, aligning with sensor time, counts as second [default: 0.0]
```
