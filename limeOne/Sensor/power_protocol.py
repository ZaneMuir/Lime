# coding: utf-8
from .normalization import process_powered_sheet
from .analysis import group_consecutive
#from .special_items import chart_dir, eye_data_path, episode_gap
from .visualization import R_raw, exportCSV

from .analysis import horizontal_log_thresh_method as current_analysis_method

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import time as timer
import os

try:
    from halo import Halo
except ImportError:
    class Halo(object):
        """docstring for Halo."""
        def __init__(self, **args):
            super(Halo, self).__init__()

        start = stop = lambda x:x
        info = warn = succeed = lambda x,text:print(text)


def main(arguments, isPreview=False, needEye=True):
    print('start')
    start_point = timer.time()

    for ch_num, time_array, raw_array, power_array, _ in process_powered_sheet(arguments):
        #if ch_num == 0:
        #    continue

        spinner = Halo(text='processing CH_%d'%ch_num, spinner='dots')
        spinner.start()

        #data = current_analysis_method(time_array, power_array, on_thresh)
        data, on_thresh = current_analysis_method(ch_num, time_array, power_array,arguments['--output'])
        spinner.info('channel %d on_thresh as %f'%(ch_num,on_thresh))
        spinner.start()

        if isPreview:
            continue # 若为预览模式则在此步退出

        #NOTE: 获取data rise 的点: 即将连续的时间点分类归组 ==> bout_time_pair: list[(start, end, name)]
        try:
            bout_time_array = group_consecutive(data[data.spike > 0]['time'].values, step=int(arguments['--episode']))
            bout_time_pair = [(bout_time_array[index][0], bout_time_array[index][-1], 'bout_%d'%index) for index in range(len(bout_time_array))]
        except IndexError:
            spinner.warn('with no chewing!!!')
            continue

        exportCSV(ch_num, bout_time_pair, arguments['--output'])

        try:
            R_raw(ch_num, data, on_thresh, bout_time_pair, arguments ,isEyed=needEye)
        except FileNotFoundError:
            spinner.warn(text='CH_%d has no eye data: %s'%(ch_num,eye_data_path%ch_num))
            spinner.start()

        spinner.succeed(text='CH_%d processed'%ch_num)

    print('all done!','%.2f'%((timer.time()-start_point)))

if __name__ == '__main__':
    main()
