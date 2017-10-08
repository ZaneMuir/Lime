from special_items import chart_dir, eye_data_path,  video_episode_gap, eyed_span
from analysis import eye_data_episode, countWithRange
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os


#TODO: 添加注释。。。
def distribution_plot(ch_num, dataSheet, title='distribution_plot.png'):
    uData, dataCount, auc = countWithRange(dataSheet)

    plt.figure(figsize=(20,10))
    plt.semilogx(uData, dataCount)
    plt.plot([on_thresh, on_thresh],[0,dataCount.max()])
    #plt.xlim(0,dataCount[-1]*0.005)
    plt.savefig(os.path.join(chart_dir+str(ch_num),title), bbox_inches='tight')
    plt.close()

def R_raw(ch_num, data, on_thresh, bout_time_pair, isEyed=False, title=None, inline=False):
    plt.figure(figsize=(100,10))
    plt.plot(data['time'].values, data['power'].values,'pink')
    plt.plot(data['time'].values, np.ones(data['time'].values.shape)*on_thresh, c='#808080')

    bout_height = data['power'].values.max()

    for index in range(len(bout_time_pair)): #scatter_result:list[(A, tau, mean, name, genre)]
        target_time = data[(data.time>=bout_time_pair[index][0]) & (data.time<=bout_time_pair[index][1])]['time'].values
        plt.plot(target_time, np.zeros(target_time.shape),c='g',linewidth=5)

    plt.xlim(data['time'].values[0], data['time'].values[-1])
    plt.ylim(-on_thresh,2*on_thresh)
    if inline:
        plt.show()
    else:
        plt.savefig(os.path.join(chart_dir+str(ch_num),'R_raw_CH_%d.png'%ch_num), bbox_inches='tight')


    if isEyed: #添加人工识别的结果
        try:
            eye = pd.read_csv(eye_data_path%ch_num)
        except FileNotFoundError:
            plt.close()
            raise FileNotFoundError
        for start,end in eye_data_episode(eye, episode_gap=video_episode_gap):
            plt.plot([start,end],[-on_thresh*0.5,-on_thresh*0.5],c='#888888',linewidth=5)

        for start, end in eyed_span:
            plt.xlim(start, end)
            plt.ylim(-on_thresh,2*on_thresh)
            if inline:
                plt.show()
            else:
                plt.savefig(os.path.join(chart_dir+str(ch_num),'R_raw_CH_%d_%d_%d.png'%(ch_num,start,end)), bbox_inches='tight')
    plt.close()

def rawChartAllRange(ch_num, data, on_thresh, preview_range=None, title=None, inline=False):
    plt.figure(figsize=(100,10))
    plt.plot(data['time'].values, data['power'].values,'pink') # power
    plt.plot(data['time'].values, np.ones(data['time'].values.shape)*on_thresh, c='#808080') # thresh
    if preview_range is not None:
        plt.xlim(preview_range)
        plt.ylim(data['power'].values.min() if data['power'].values.min()<on_thresh else -1*np.abs(on_thresh), data[(data.time>preview_range[0]) & (data.time<preview_range[1])]['power'].values.max())
    if title is None:
        if inline:
            plt.show()
        else:
            plt.savefig(os.path.join(chart_dir+str(ch_num),'preivew_R_raw_CH_%d.png'%ch_num), bbox_inches='tight')
    else:
        if inline:
            plt.show()
        else:
            plt.savefig(os.path.join(chart_dir+str(ch_num),title), bbox_inches='tight')
    plt.close()

def exportCSV(ch_num, bout_time_pair, title=None): #REVIEW: optimization required
    with open(os.path.join(chart_dir+str(ch_num),'bout_time_CH_%d.csv'%ch_num),'w') as csv_file:
        csv_file.write('name,start,end,start_t,end_t\n')
        csv_file.write('\n'.join([','.join([str(bout_time_pair[index][2]),
                                            str(bout_time_pair[index][0]),
                                            str(bout_time_pair[index][1]),
                                            '%d:%.1f'%(int(bout_time_pair[index][0]/60),
                                                       bout_time_pair[index][0]%60),
                                            '%d:%.1f'%(int(bout_time_pair[index][1]/60),
                                                       bout_time_pair[index][1]%60)])
                                  for index in range(len(bout_time_pair))]))
