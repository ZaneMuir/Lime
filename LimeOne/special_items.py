import os
#========================常量设置========================
powered_sheet_title = [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#NOTE: after 170907, all '1 CH_0  ' change into '1 CH_0'
#20170906_000:              [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
#20170906_003:              [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#20170906_001,20170907_ :   [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#FUTURE:                    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# power后的txt文件的columns names
#========================其他设置========================
def checkFile(chart_dir, target_data_path, episode_gap, eyeDataSuffix):
    if not os.path.isdir(chart_dir):
        os.mkdir(chart_dir)
    #NOTE: 为每次session提供不同的文件夹，以方便储存数据
    # SessionName_Gap_chName

    while not os.path.isfile(target_data_path):
        print('target file not found:',target_data_path)
        target_data_path = input('reenter the target file path:')
    eye_data_path = os.path.splitext(target_data_path)[0]+eyeDataSuffix

    chart_dir = os.path.join(chart_dir,'%s_%d_'%(os.path.splitext(os.path.split(target_data_path)[-1])[0],episode_gap))
    if not os.path.isdir(chart_dir+'0'):
        os.mkdir(chart_dir+'0')
    if not os.path.isdir(chart_dir+'1'):
        os.mkdir(chart_dir+'1')
    return chart_dir, eye_data_path
