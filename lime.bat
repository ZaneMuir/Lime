@echo off

::REM 实验的日期与时间
set SessionDate=20180203
set SessionTime=1500
set SessionId=004
set MiceSequence=C1M1/C2M1/C3M1/C4M1
set VideoOffset=11
set FoodSeq=3.3902_3.2269/4.1189_4.0292/3.4662_3.0142/3.4896_3.0894
::#############新增语句 set VideoName=normal/normal/normal/normal#############
set VideoName=normal/normal/normal/normal
::#############新增语句 set ThreshScale=1#############
set ThreshScale=1

::REM 实验设置[两只两只为一组]
set Setup=Loneliness1/Loneliness1

::同时有nCage只老鼠实验，从左往右依次为MiceSequence
:: C1 -> N1
:: C2 -> H1
:: C3 -> H2
:: C4 -> N2
:: C5 -> N3
:: C6 -> H3
:: C7 -> H4
set nCage=4

::========== 以下的选项仅在必需要时修改 ==========

::数据文件储存的目录
set DataDirPath=data
::图表输出目录
set ChartDirPath=chart

::sensor和视频文件
set SensorFile=%SessionDate%%SessionId%_PW.txt
set VideoFile=%SessionDate%%SessionId%.mov

::#############新增option: -z %VideoName%#############
::#############新增option: -s %ThreshScale%#############
python lime.py -s %ThreshScale% -z %VideoName% -r 60_1800 -i %DataDirPath% -o %ChartDirPath% -d %SessionDate% -t %SessionTime% -u %Setup% -n %nCage% -m %MiceSequence% -f %FoodSeq% -v %VideoOffset% %SensorFile% %VideoFile%

pause
