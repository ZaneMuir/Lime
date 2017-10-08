from special_items import chart_dir
import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import os

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

def horizontal_log_thresh_method(ch_num, time_array, power_array):
    ''' 目前计算阈值的方法：
        对power的数据取log10，用标准正态分布函数拟合[参考维基百科正态分布词条]，
        得到mu(loc)和sigma(scale)。
        阈值取10^(mu+sigma)'''

    logData = np.log10(power_array)
    loc, scale = stats.norm.fit(logData)
    on_thresh = 10**(loc+scale)

    dataSheet = horizontal_thresh_method(time_array, power_array, on_thresh)
    distribution_plot(ch_num, dataSheet)

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
