from special_items import chart_dir, eye_data_path, eyed_span, video_episode_gap
from analysis import eye_data_episode
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os

def SATM(ch_num, codebook, scatter_result,title=None,inline=False):
    plt.figure(figsize=(30,30))
    plt.scatter(x=[x for _,x,_,_,_ in scatter_result ], y=[y for _,_,y,_,_ in scatter_result],s=50, c=['g' if c==1 else 'r' for _,_,_,_,c in scatter_result])
    for _,x,y, in codebook:
        plt.scatter(x=x,y=y,s=100,c='#808080')
    #plt.xlim(-3,7)
    if inline:
        plt.show()
    else:
        plt.savefig(os.path.join(chart_dir,'SATM_CH_%d.png'%ch_num), bbox_inches='tight')
    plt.close('all')

def R_raw(ch_num, data, on_thresh, bout_time_pair, scatter_result=None, isEyed=False, title=None, inline=False):
    plt.figure(figsize=(100,10))
    plt.plot(data['time'].values, data['power'].values,'pink')
    plt.plot(data['time'].values, np.ones(data['time'].values.shape)*on_thresh, c='#808080')

    bout_height = data['power'].values.max()

    if scatter_result is not None:
        for index in range(len(bout_time_pair)): #scatter_result:list[(A, tau, mean, name, genre)]
            if scatter_result[index][-1] == 1:
                color = 'g'
            else:
                color = 'r'
            target_time = data[(data.time>=bout_time_pair[index][0]) & (data.time<=bout_time_pair[index][1])]['time'].values
            plt.plot(target_time, np.zeros(target_time.shape)-on_thresh,c=color,linewidth=3)
    else:
        for index in range(len(bout_time_pair)): #scatter_result:list[(A, tau, mean, name, genre)]
            target_time = data[(data.time>=bout_time_pair[index][0]) & (data.time<=bout_time_pair[index][1])]['time'].values
            plt.plot(target_time, np.zeros(target_time.shape)-on_thresh,c='g',linewidth=3)


    plt.xlim(data['time'].values[0], data['time'].values[-1])
    if inline:
        plt.show()
    else:
        plt.savefig(os.path.join(chart_dir,'R_raw_CH_%d.png'%ch_num), bbox_inches='tight')


    if isEyed: #添加人工识别的结果
        eye = pd.read_csv(eye_data_path)
        for start,end in eye_data_episode(eye, episode_gap=video_episode_gap):
            plt.plot([start,end],[-on_thresh*1.5,-on_thresh*1.5],c='#888888',linewidth=5)

        for start, end in eyed_span:
            plt.xlim(start, end)
            plt.ylim(-3*on_thresh,3*on_thresh)
            if inline:
                plt.show()
            else:
                plt.savefig(os.path.join(chart_dir,'R_raw_CH_%d_%d_%d.png'%(ch_num,start,end)), bbox_inches='tight')
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
            plt.savefig(os.path.join(chart_dir,'preivew_R_raw_CH_%d.png'%ch_num), bbox_inches='tight')
    else:
        if inline:
            plt.show()
        else:
            plt.savefig(os.path.join(chart_dir,title), bbox_inches='tight')
    plt.close()

def exportCSV(ch_num, bout_time_pair, scatter_result=None,title=None): #REVIEW: optimization required
    if scatter_result == None:
        with open(os.path.join(chart_dir,'bout_time_CH_%d.csv'%ch_num),'w') as csv_file:
            csv_file.write('name,start,end,start_t,end_t\n')
            csv_file.write('\n'.join([','.join([str(bout_time_pair[index][2]),
                                                str(bout_time_pair[index][0]),
                                                str(bout_time_pair[index][1]),
                                                '%d:%.1f'%(int(bout_time_pair[index][0]/60),
                                                           bout_time_pair[index][0]%60),
                                                '%d:%.1f'%(int(bout_time_pair[index][1]/60),
                                                           bout_time_pair[index][1]%60)])
                                      for index in range(len(bout_time_pair))]))
    else:
        with open(os.path.join(chart_dir,'bout_time_CH_%d.csv'%ch_num),'w') as csv_file:
            csv_file.write('name,start,end,start_t,end_t,genre\n')
            csv_file.write('\n'.join([','.join([str(bout_time_pair[index][2]),
                                                str(bout_time_pair[index][0]),
                                                str(bout_time_pair[index][1]),
                                                '%d:%.1f'%(int(bout_time_pair[index][0]/60),
                                                           bout_time_pair[index][0]%60),
                                                '%d:%.1f'%(int(bout_time_pair[index][1]/60),
                                                           bout_time_pair[index][1]%60),
                                                str(scatter_result[index][-1])])
                                      for index in range(len(bout_time_pair))]))
