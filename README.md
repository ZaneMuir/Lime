# Lime
analysis program for chewing behavior of Zhang's Lab.

if you are using Windows, you have to build the ```videoAnalysis``` by yourself.

## Usage 使用方法

使用方法与相关可调参数如下。运行后会首先弹出第一帧，拖拽可画水平线作为截取的区域，高度默认为2px。先选取左侧(0)，再选取右侧(1)；完成后键入回车。程序运行完后(ca. 6min.), 会输出综合的chew count与chew duration值。

数据文件(\*\_PW.txt, \*.mov)默认放于data文件夹(或者自行修改```--input```参数)中。最终数据输出于chart文件夹中(或者自行修改```--output```参数)；另外，chew count与chew duration值仅输出在终端，请注意保存。

```
Lime
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
```

## Demo 示例

![demo](demo/screenshot-selection.png)
( drag to draw two lines for target area, the left line first; then press ```ENTER``` for further procedures )

![demo](demo/screenshot.png)

## Files Structure 文件目录结构

```
LimeOne
+-data
|  +- 20171123001_PW.txt
|  +- 20171123001.mov
|  +- ...
+-Sensor
|  +- ...
+-Video
|  +- ...
+-chart
|  +- 20171123001_PW_4_0
|  |  +- ...
|  +- 20171123001_PW_4_0
|  |  +- ...
+-lime.py
+-README.txt
+-requirements.txt
```

## requirements Python依赖模块

- docopt
- matplotlib
- numpy
- scipy [optional]
- pandas
- opencv-python
- Cython [optional]
- halo [optional]
- tqdm
