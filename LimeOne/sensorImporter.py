import pandas as pd
import os,re

powered_sheet_title = [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#NOTE: after 170907, all '1 CH_0  ' change into '1 CH_0'
#20170906_000:              [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
#20170906_003:              [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#20170906_001,20170907_ :   [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#FUTURE:                    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]


def processTimeRange(timeRange):
    return list(map(lambda x:int(x), re.split(r'_',timeRange)))

def process_powered_sheet(sensor_file, time_range):
    ''' 读取spike2导出的sheet数据。
        return list(ch_num, raw_array, normalized_power_array, extra)
        currently, extra as tuple(None,)'''
    sheet_data = pd.read_csv(sensor_file, sep='\t')
    taking_time = processTimeRange(time_range)

    sheet_data = sheet_data[(sheet_data.Time >= taking_time[0]) & (sheet_data.Time <= taking_time[1])] # 去除前六十秒的数据
    time_span = sheet_data['Time'].values # 获取六十秒后数据的所有时间点

    normalized_data = []
    
    for ch_num, ch_title, power_title in powered_sheet_title:
        ch_raw = sheet_data[ch_title].values #获取原始数据
        power_raw = sheet_data[power_title].values #获取power后的数据

        normalized_data.append((ch_num, time_span, ch_raw, power_raw, (None,)))

    return normalized_data
