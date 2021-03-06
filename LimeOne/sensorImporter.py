u"""
sensorImporter.

主要包含读取spike2的txt文件的函数
"""
import pandas as pd
# import os
import re

# powered_sheet_title = [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# NOTE: after 170907, all '1 CH_0  ' change into '1 CH_0'
# 20170906_000:         [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
# 20170906_003:         [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# 20170906_001,20170907_[[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
# FUTURE:               [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]


def powered_sheet_title(n):
    u"""txt文件的title."""
    [[i, '%d CH_%d' % (i+1, i), '7%02d CH_%d_P' % (i+1, i)] for i in range(n)]


def processTimeRange(timeRange):
    return list(map(lambda x: int(x), re.split(r'_', timeRange)))


def process_powered_sheet(sensor_file, time_range, ncage):
    u"""
    读取spike2导出的sheet数据.

    return list(ch_num, raw_array, normalized_power_array, extra)
    currently, extra as tuple(None,)
    """
    sheet_data = pd.read_csv(sensor_file, sep='\t')
    taking_time = processTimeRange(time_range)  # 获取需要分析的时间段

    sheet_data = sheet_data[(sheet_data.Time >= taking_time[0]) &
                            (sheet_data.Time <= taking_time[1])]  # 截取需分析时段的数据
    time_span = sheet_data['Time'].values  # 获取所有的时间点

    normalized_data = []

    # 对每个channel：
    for ch_num, ch_title, power_title in powered_sheet_title(ncage):
        ch_raw = sheet_data[ch_title].values  # 获取原始数据
        power_raw = sheet_data[power_title].values  # 获取power后的数据

        # 整合
        normalized_data.append((ch_num, time_span, ch_raw, power_raw, (None,)))

    return normalized_data
