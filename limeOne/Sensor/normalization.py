from .special_items import powered_sheet_title
import pandas as pd
import os,re

def processTimeRange(timeRange):
    return list(map(lambda x:int(x), re.split(r'_',timeRange)))


def process_powered_sheet(arguments):
    ''' 读取spike2导出的sheet原始数据。
        return list(ch_num, raw_array, normalized_power_array, extra)
        currently, extra as tuple(None,)'''
    sheet_data = pd.read_csv(os.path.join(arguments['--input'],arguments['SENSORFILE']), sep='\t')
    taking_time = processTimeRange(arguments['--timeRange'])

    sheet_data = sheet_data[(sheet_data.Time >= taking_time[0]) & (sheet_data.Time <= taking_time[1])] # 去除前六十秒的数据
    time_span = sheet_data['Time'].values # 获取六十秒后数据的所有时间点

    normalized_data = []
    for ch_num, ch_title, power_title in powered_sheet_title:
        ch_raw = sheet_data[ch_title].values #获取原始数据
        power_raw = sheet_data[power_title].values #获取power后的数据

        normalized_data.append((ch_num, time_span, ch_raw, power_raw, (None,)))

    return normalized_data
