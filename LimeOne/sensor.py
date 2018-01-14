'''sensor.py
主要用于分析传感器的数据

具体思路：
计算每个channel的阈值，
选取位于阈值之上的数据，
并获取开始与结束的时间；
但该时间并非真实啃食的时间。
'''
import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import os, re
from tqdm import tqdm

from .sensorImporter import process_powered_sheet
from .database import createNewSessionTable
def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def sensorDB(sensor_file, time_range, sessionID, episode_gap, dbCursor):
    '''sensorDB(sensor_file::string, time_range::string, sessionID::list, episode_gap::float, dbCursor::sqlit3.cursor):'''

    entryResult = []
    # 读取spike2导出的txt文件，详见'LimeOne/sensorImporter.py'
    for index, (ch_num, time_array, raw_array, power_array, _ ) in enumerate(process_powered_sheet(sensor_file, time_range, len(sessionID))):
        #print(ch_num, power_array)
        loc, scale = stats.norm.fit(np.log10(power_array)) # 对数据log后，做正态分布拟合[利用scipy.stats模块]
        thresh = 10**(loc+scale) if power_array.max() > 0.0005 else 0.0005 # 若最大值小于0.0005，则默认为没有啃食行为
        #TODO:distribution plot?

        bout = np.sign(power_array - thresh) # 位于阈值以上的数据变为1，以下的则为-1
        table = pd.DataFrame(   np.hstack((time_array[:,np.newaxis], bout[:,np.newaxis])),
                                columns=['time','bout'])

        try:
            # 以下操作提取出在阈值以上的时间点，并对其分割，同时，若end和下一个的start相聚小于episode_gap，则将两个bout融合。
            bout_time_pair = [(index, item[0],item[-1]) for index, item in enumerate(group_consecutive(table[table.bout > 0]['time'].values,step=episode_gap))]
        except IndexError: # 没有啃食行为
            print("with no chewing")
            bout_time_pair = [(0,0,0)]

        title=['start','end']
        createNewSessionTable(dbCursor, sessionID[ch_num]+'_Bout', title, bout_time_pair)
