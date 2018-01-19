#实验的日期与时间
SessionDate=20171123
SessionTime=1430
SessionId=001

#实验设置[两只两只为一组]
Setup=TtC_NH/TtC_NN

#同时有nCage只老鼠实验，从左往右依次为MiceSequence
# C1 -> N1
# C2 -> H1
# C3 -> H2
# C4 -> N2
# C5 -> N3
# C6 -> H3
# C7 -> H4
nCage=4 #偶数
MiceSequence=C1M1/C2M1/C1M2/C2M2

#每只老鼠食物的消耗状况
FoodSeq=3.653_3.142/3.653_3.142/3.653_3.142/3.653_3.142

#视频延迟时间
VideoOffset=17

#========== 以下的选项仅在必需要时修改 ==========

#数据文件储存的目录
DataDirPath=data
#图表输出目录
ChartDirPath=chart

#sensor和视频文件
SensorFile=$SessionDate$SessionId"_PW.txt"
VideoFile=$SessionDate$SessionId.mov

#using Julia
#julia LimeJulia/Lime.jl \
#using python3
python3 lime.py -i $DataDirPath -o $ChartDirPath -d $SessionDate -t $SessionTime -u $Setup -n $nCage -m $MiceSequence -f $FoodSeq -v $VideoOffset $SensorFile $VideoFile

# Other Options:
#
# database file path
#-b chewing.db
#
# climbing episode gap length, unit as second
#-c 0
#
# episode gap length, unit as second
#-e 4
#
# session length, unit as minute [default: 60]
#-l 60
#
# need pose analysis only? [default: True]
#-p True
#
# checking range, unit as second [default: 60_3600]
#-r 60_3600
#
# target area width, unit as px [default: 20]
#-w 20
