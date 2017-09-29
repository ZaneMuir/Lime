from special_items import   target_data_path, sampling_frequency, \
                            skip_time, powered_on_threshold_scale, powered_off_threshold_scale, \
                            powered_sheet_title, noise_span
import pandas as pd
import numpy as np
import re

def get_derivative(array, pos=0):
    ''' 计算导数'''
    #0: x_n-x_(n-1);
    #-1: x_(n-1)-x_n
    return np.insert(np.diff(array), pos if pos == 0 else len(array), 1)
    #np.diff(a, n=1, axis=-1)

def power_thresh(power_raw, ch_num, noise_range=None):
    ''' 阈值计算'''
    if noise_range is not None:
        print('Noise range as: %d-%d'%noise_range)
        noise_data = power_raw[noise_range[0]*sampling_frequency:noise_range[1]*sampling_frequency]
    else:
        noise_data = power_raw

    mean = noise_data.mean()
    sigma = noise_data.std()
    print(  'noise sigma as:',sigma,
            '\nnoise mean as', mean)

    on_threshold, off_threshold = powered_on_threshold_scale*sigma, powered_off_threshold_scale*sigma
    norm_raw = np.abs(power_raw - mean) #将数据的均值拉到0
    print('on_threshold:',on_threshold)

    on_derivative = get_derivative(np.sign(norm_raw-on_threshold))
    off_derivative = get_derivative(np.sign(norm_raw-off_threshold))

    return mean, on_threshold, off_threshold, on_derivative, off_derivative, sigma

def process_powered_sheet(filePath=target_data_path):
    ''' 处理power后的原始数据，包括读取、计算sigma、计算阈值，计算导数。
        return list(ch_num, DataFrame['time','raw','power','spike'], on_threshold, optimal_h)'''
    sheet_data = pd.read_csv(filePath, sep='\t')
    sheet_data = sheet_data[sheet_data.Time >= skip_time] # 去除前六十秒的数据
    time_span = sheet_data['Time'].values # 获取六十秒后数据的所有时间点

    normalized_data = []
    for ch_num, ch_title, power_title in powered_sheet_title:
        ch_raw = sheet_data[ch_title].values #获取原始数据
        power_raw = sheet_data[power_title].values #获取power后的数据

        print('='*6, 'Channel', ch_num, '='*6)
        mean, on_threshold, _, derivative, _, sigma = power_thresh(power_raw, ch_num, noise_range=noise_span)
        #NOTE: 不做off threshold

        optimal_h = 1.06*sigma*(len(ch_raw)**(-0.25))

        #NOTE: 这里的power是power_raw - mean
        matrix = np.hstack((time_span[:,np.newaxis], ch_raw[:,np.newaxis], power_raw[:,np.newaxis]-mean, derivative[:,np.newaxis]))
        normalized_data.append((ch_num, pd.DataFrame(matrix, columns=['time','raw','power','spike']), on_threshold, optimal_h))

    print('='*23)
    return normalized_data
