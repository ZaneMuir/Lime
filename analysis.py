from special_items import chart_dir #, sampling_frequency, fitting_func,cluster_k
import numpy as np
import pandas as pd
#from scipy import signal, optimize
#from scipy.cluster.vq import kmeans
import scipy.stats as stats
import matplotlib.pyplot as plt
import os
#import warnings
#warnings.filterwarnings('ignore') # to suppress runtime warnings.

def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def countWithRange(target, countRange=None, name='power'):
    if countRange is None:
        target_data = target[name].values
    else:
        target_data = target[name].values[countRange[0]:countRange[1]]
    utarget,uind=np.unique(target_data,return_inverse=True)
    target_count=np.bincount(uind)
    auc = target_count.sum()

    return utarget, target_count, auc

def horizontal_thresh_method(time_array, power_array, on_thresh):
    spike = np.sign(power_array-on_thresh)
    data = pd.DataFrame(np.hstack((time_array[:,np.newaxis], power_array[:,np.newaxis], spike[:,np.newaxis])),
                        columns=['time','power','spike'])
    return data

def horizontal_log_thresh_method(ch_num, time_array, power_array):
    #print('power:',power_array)
    logData = np.log10(power_array)
    param = stats.norm.fit(logData)
    #print('param:',param)
    on_thresh = 10**param[0]*1.5
    #print('channel %d current thresh:'%ch_num, on_thresh)

    dataSheet = horizontal_thresh_method(time_array, power_array, on_thresh)

    uData, dataCount, auc = countWithRange(dataSheet)
    plt.figure(figsize=(20,10))
    plt.semilogx(uData, dataCount)
    plt.plot([on_thresh, on_thresh],[0,dataCount.max()])
    #plt.xlim(0,dataCount[-1]*0.005)
    plt.savefig(os.path.join(chart_dir+str(ch_num),'distribution_plot.png'), bbox_inches='tight')
    plt.close()

    return dataSheet, on_thresh

def eye_data_episode(eye_data_sheet, episode_gap=4):
    ''' 对视频分析的结果进行episode归类
        返回值：list(tuple(start,end),...)'''
    raw_data = np.array([])
    for index in range(eye_data_sheet.shape[0]):
        start = eye_data_sheet.iloc[index]['start']
        end = eye_data_sheet.iloc[index]['end']
        if start>end:
            start, end = end, start
        #print(start,end)
        raw_data = np.hstack((raw_data, np.linspace(start,end,(end-start)*1000)))

    bout_time_array = group_consecutive(raw_data, step=episode_gap)
    bout_time_pair = [(bout_time_array[index][0], bout_time_array[index][-1]) for index in range(len(bout_time_array))]

    return bout_time_pair

#REVIEW: shall we cancel this?
#def power_spectrum_with_fitting(data,psd_list,ch_num,title='', isPlot = False):
#    #psd_list = [(90,150,'ctrl'),
#    #            (195,202,'195_202'),
#    #            (209,214,'209_214'),
#    #            (277,300,'277_300'),
#    #            (418,426,'418_426')]
#    fitting_popt = []
#    out_name = []
#
#    print('checking PSD ch_%d'%ch_num)
#
#    for start, end, name in tqdm(psd_list):
#        target = data[(data.time >= start) & (data.time <= end)]['raw'].values
#        fx, Pxx = signal.welch(target, sampling_frequency, nperseg=len(target))
#        try:
#            popt , _ = optimize.curve_fit(fitting_func,fx,Pxx)
#        except TypeError:
#            out_name.append(name)
#            continue
#        fitting_popt.append(popt)
#    return fitting_popt, out_name

#REVIEW: shall we cancel this?
#def scatter_cluster(ch_num,data,bout_time_pair):
#    popt_list, out_name = power_spectrum_with_fitting(data, bout_time_pair, ch_num, isPlot=False) #数据拟合
#    bout_time_pair = [item for item in bout_time_pair if item[-1] not in out_name] #删去拟合未果的数据
#
#    mean_list = [(data[(data.time >= start) & (data.time <= end)]['raw'].mean(), name) for start, end, name in bout_time_pair]
#    argument_list = [(popt_list[index][0], popt_list[index][1], mean_list[index][0], mean_list[index][1]) for index in range(len(mean_list))]
#    #NOTE: for [A, tau, mean, name]
#    exile_name = [x[-1] for x in argument_list if x[1] < -10]      #NOTE: 除去长度不足10个的数据
#    bout_time_pair = [x for x in bout_time_pair if x[-1] not in exile_name]
#
#    #k-means clustering
#    #NOTE:codebook: np.array([A, tau, C])
#    codebook, distortion = kmeans(list(map(lambda x:x[:3],argument_list)),cluster_k) # k-means clustering
#    #print('k-means result:', codebook, distortion)
#
#    #cluster and delete data
#    #NOTE: scatter_result:list[(A, tau, mean, name, genre)]
#    scatter_result = []
#    for item in argument_list:
#        distance1 = np.sqrt((item[0]-codebook[0][0])**2+(item[1]-codebook[0][1])**2+(item[2]-codebook[0][2])**2)
#        distance2 = np.sqrt((item[0]-codebook[1][0])**2+(item[1]-codebook[1][1])**2+(item[2]-codebook[1][2])**2)
#        genre = 1 if distance1 > distance2 else 2
#        scatter_result.append((item[0], item[1], item[2], item[3], genre))
#
#    return codebook, scatter_result
