import os
#========================常量设置========================
target_data_path = os.path.join(os.path.split(__file__)[0],'data','20171008_005.txt')   #待处理的spike导出txt文件地址
eye_data_path = os.path.splitext(target_data_path)[0]+'_%d_eye_10min.csv'               #人工分析后的结果文件
chart_dir = os.path.join(os.path.split(__file__)[0],'chart')                            #储存结果的目录

powered_sheet_title = [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#NOTE: after 170907, all '1 CH_0  ' change into '1 CH_0'
#20170906_000:              [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
#20170906_003:              [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#20170906_001,20170907_ :   [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#FUTURE:                    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# power后的txt文件的columns names

taking_time = (60,1800) #seconds NOTE:跳过前60秒的数据，避免power引起的数据的扭曲; 跳过1800秒后的数据，方便统计数据。
eyed_span = [(60,800)]  #seconds NOTE: 人工分析的时间段

episode_gap = 4         #seconds NOTE: episode聚类间隔时长
video_episode_gap = 4   #seconds NOTE: 对视频采用episode分析

#========================其他设置========================
if not os.path.isdir(chart_dir):
    os.mkdir(chart_dir)
#NOTE: 为每次session提供不同的文件夹，以方便储存数据
# SessionName_Gap_chName
chart_dir = os.path.join(chart_dir,'%s_%d_'%(os.path.splitext(os.path.split(target_data_path)[-1])[0],episode_gap))
if not os.path.isdir(chart_dir+'0'):
    os.mkdir(chart_dir+'0')
if not os.path.isdir(chart_dir+'1'):
    os.mkdir(chart_dir+'1')

if not os.path.isfile(target_data_path):
    print('target file not found:',target_data_path)
    target_data_path = input('reenter the target file path:')
    eye_data_path = os.path.splitext(target_data_path)[0]+'_eye.csv'
