import os
#========================常量设置========================
target_data_path = os.path.join(os.path.split(__file__)[0],'data/20170906_003.txt') #NOTE: 处理的目标原始文件
eye_data_path = os.path.splitext(target_data_path)[0]+'_eye_10min.csv'
chart_dir = os.path.join(os.path.split(__file__)[0],'chart') #NOTE: 储存图标与其他数据
#video_dir = os.path.join(os.path.split(__file__)[0],'video') #储存视频临时文件与渲染后文件

powered_sheet_title = [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#NOTE: after 170907, all '1 CH_0  ' change into '1 CH_0'
#20170906_000:              [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
#20170906_003:              [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#20170906_001,20170907_ :   [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#FUTURE:                    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# power后的txt文件的columns names

skip_time = 60 #seconds NOTE: 跳过前60秒的数据，避免power引起的数据的扭曲
eyed_span = [(60,600)] #seconds NOTE: 人工分析的时间段
noise_span = (3400, 3700) #NOTE: 噪音区间 BUG: 目前需要人工的去设定，建议之后的实验设法固定一个时间段使得饼干不会被碰
#0906000: (1500,2000)
#0906001: (7000,8000)
#0906003: (3400, 3700)
#0907001: (1780,1820)
#0907002: (580,640)

episode_gap = 4 #seconds NOTE:
video_episode_gap = 20 #seconds NOTE: 对视频采用episode分析

#stimuli between on and off threshold are valid: threshold = scale * sigma
powered_on_threshold_scale = 10         #XXX:  BUG: 目前需要人工设定，需要更新的自动求值算法
powered_off_threshold_scale = 12        #XXX: 历史原因被留存，请忽略

#ced_frequency = 29762      #Hz; ced system
sampling_frequency = 1000   #Hz NOTE:sampling_duration calculated as len(data)/sampling_frequency

#KDE analysis const #NOTE: NOT USING KDE ANALYSIS ANY MORE
#kernel_bandwidth = 1.5              # bandwith 'h' :: make the curve smooth enough
#kernel_type = 'gaussian'            #'gaussian', 'tophat', 'epanechnikov', 'exponential', 'linear', 'cosine'
#using Silverman's rule of thumb for optimal h: std(data)*(4/3/n)^(1/5)
#off_scale = 0.25                    # compensate the off-effect

#multiprocessing
#kernel = 4

#miscellanous
#check = lambda x:x                  #for debugging.

import numpy as np
fitting_func = lambda x,A,tau,C:A*np.exp(-x/tau)+C #NOTE: fitting function

#k-means clustering
cluster_k = 2 #NOTE: K均值聚类的分类组数
#iteration = 20
#kmeans_thresh = 1e-5


#========================其他设置========================
if not os.path.isdir(chart_dir):
    os.mkdir(chart_dir)
#REVIEW: 为每次session提供不同的文件夹，以方便储存数据
# SessionName_N_Gap_NoiseRange
chart_dir = os.path.join(chart_dir,'%s_%.1f_%.1f_%s'%(os.path.splitext(os.path.split(target_data_path)[-1])[0],powered_on_threshold_scale,episode_gap,'%d_%d'%noise_span if noise_span != None else 'None'))
if not os.path.isdir(chart_dir):
    os.mkdir(chart_dir)



#if not os.path.isdir(video_dir):
#    os.mkdir(video_dir)
#    os.mkdir(os.path.join(video_dir,'temp'))

if not os.path.isfile(target_data_path):
    print('target file not found:',target_data_path)
    target_data_path = input('reenter the target file path:')
    eye_data_path = os.path.splitext(target_data_path)[0]+'_eye.csv'
