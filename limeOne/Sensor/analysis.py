#from .special_items import chart_dir
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

def distribution_plot(ch_num, dataSheet, on_thresh, chart_dir,title='distribution_plot.png'):
    uData, dataCount, auc = countWithRange(dataSheet)

    #plt.figure(figsize=(20,10))
    #plt.semilogx(uData, dataCount)
    #plt.plot([on_thresh, on_thresh],[0,dataCount.max()])
    #plt.xlim(0,dataCount[-1]*0.005)
    #plt.savefig(os.path.join(chart_dir+str(ch_num),title), bbox_inches='tight')
    #plt.close()

    plt.figure(figsize=(20,10))
    ax = plt.subplot(111)
    ax.hist(dataSheet['power'].values,bins=np.linspace(0,1e-3,500))
    ax.plot([on_thresh, on_thresh],[0,dataCount.max()])
    #ax.set_xscale('log')
    plt.savefig(os.path.join(chart_dir+str(ch_num),title), bbox_inches='tight')
    plt.close()

def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def countWithRange(target, countRange=None, name='power'):
    ''' 统计DataFrame中不同的值出现的次数
        target :: DataFrame() :: 数据源；
        countRange :: tuple(start,end) :: 节选数据的index，默认为None；
        name :: str() :: column名称，默认为\'power\'。'''
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

def horizontal_log_thresh_method(ch_num, time_array, power_array,chart_dir):
    ''' 目前计算阈值的方法：
        对power的数据取log10，用标准正态分布函数拟合[参考维基百科正态分布词条]，
        得到mu(loc)和sigma(scale)。
        阈值取10^(mu+sigma)'''

    logData = np.log10(power_array)
    loc, scale = stats.norm.fit(logData)
    on_thresh = 10**(loc+scale)

    #print(loc, scale)

    if power_array.max() < 0.0005:
        on_thresh = 0.0005
        print("power_array.max is:", power_array.max())
    else:
        on_thresh = on_thresh #if power_array.max() < 0.0005 else 0.0005

    dataSheet = horizontal_thresh_method(time_array, power_array, on_thresh)
    distribution_plot(ch_num, dataSheet, on_thresh,chart_dir)

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
