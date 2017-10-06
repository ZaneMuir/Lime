# coding: utf-8
from normalization import process_powered_sheet
from analysis import power_spectrum_with_fitting, group_consecutive,scatter_cluster
from special_items import cluster_k, sampling_frequency, chart_dir, eye_data_path, noise_span, episode_gap
from visualization import SATM, rawChartAllRange, R_raw, exportCSV

from analysis import horizontal_thresh_method as current_analysis_method

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
try:
    from tqdm import tqdm
except ImportError:
    tqdm = lambda x:x
import time as timer
import os

def main(forceThresh=None, isPreview=False):
    print('start')
    start_point = timer.time()
    #data normalization
    #power threshold

    #CHANGED: with new data return form:
    #for ch_num, data, on_thresh, optimal_h in process_powered_sheet(): #data as DataFrame['time','raw','power','spike']
    for ch_num, time_array, raw_array, power_array, on_thresh, extra in process_powered_sheet():
        if ch_num == 0: #BUG: 跳过Ch 0通道；仅仅是为了方便分析Ch 1的数据。
            continue

        print('#'*32)
        print('processing CH_%d'%ch_num)

        if forceThresh: # 强制使用外来设定的阈值
            on_thresh = forceThresh


        #CHANGED: modulize analysis system
        data = current_analysis_method(time_array, power_array, on_thresh)

        #NOTE: 预览全局数据与噪音区间
        rawChartAllRange(ch_num, data, on_thresh) # all range preview
        rawChartAllRange(ch_num, data, on_thresh, preview_range=noise_span, title='Noise.png') # noise

        if isPreview:
            continue # 若为预览模式则在此步退出

        #CHANGED: integrated into modulized system
        #NOTE: 不做KDE，仅对power后的数据减去阈值后取Sign值；由于历史原因，变量名就没有改。
        #kde_raw = np.sign(data['power'].values-on_thresh)
        #kde_result = pd.DataFrame(  np.hstack((data['time'].values[:,np.newaxis], kde_raw[:,np.newaxis])),
        #                            columns=['time','kde_spike'])


        #NOTE: 获取data rise 的点: 即将连续的时间点分类归组 ==> bout_time_pair: list[(start, end, name)]
        bout_time_array = group_consecutive(data[data.spike > 0]['time'].values, step=episode_gap) #CHANGED: variable name
        bout_time_pair = [(bout_time_array[index][0], bout_time_array[index][-1], 'bout_%d'%index) for index in range(len(bout_time_array))]

        #CHANGED: stop fitting and clustering
        #1. 函数拟合; 2. k均值聚类
        #codebook, scatter_result = scatter_cluster(ch_num,data,bout_time_pair)

        #optimize parameters
        #visualization
        # SATM
        #SATM(ch_num, codebook, scatter_result)

        # export csv
        #exportCSV(ch_num, bout_time_pair, scatter_result)
        #CHANGED: without fitting and clustering
        exportCSV(ch_num, bout_time_pair)


        # R_raw: isEyed True ==> 需要视频分析的数据
        #R_raw(ch_num, data, on_thresh, bout_time_pair, scatter_result, isEyed=True)
        #CHANGED: without fitting and clustering
        R_raw(ch_num, data, on_thresh, bout_time_pair, isEyed=True)


        print('CH_%d processed'%ch_num)

    print('all done!','%.2f'%((timer.time()-start_point)/60))

if __name__ == '__main__':
    main()

    #raw_chart_dir = chart_dir
    #for item in tqdm(range(11)):
    #    chart_dir = os.path.join(raw_chart_dir, 'setup_%d'%item)
    #    powered_on_threshold_scale = 8 + item
    #    print(chart_dir)
    #    print('power:',powered_on_threshold_scale)
    #    main()
