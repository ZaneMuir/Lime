from .analysis import eye_data_episode
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

import os,re
def processTimeRange(timeRange):
    return list(map(lambda x:int(x), re.split(r'_',timeRange)))

def R_raw(ch_num, data, on_thresh, bout_time_pair, arguments, isEyed=False, title=None, inline=False):
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
        plt.savefig(os.path.join(arguments['--output']+str(ch_num),'R_raw_CH_%d.png'%ch_num), bbox_inches='tight')


    if isEyed: #添加人工识别的结果
        try:
            eye = pd.read_csv(arguments['eyeDataFile']%ch_num)
        except FileNotFoundError:
            plt.close()
            raise FileNotFoundError
        for start,end in eye_data_episode(eye, episode_gap=int(arguments['--episode'])):
            plt.plot([start,end],[-on_thresh*0.5,-on_thresh*0.5],c='#888888',linewidth=5)

        start, end = processTimeRange(arguments['--timeRange'])
        plt.xlim(start, end)
        plt.ylim(-on_thresh,2*on_thresh)
        if inline:
            plt.show()
        else:
            plt.savefig(os.path.join(arguments['--output']+str(ch_num),'R_raw_CH_%d_%d_%d.png'%(ch_num,start,end)), bbox_inches='tight')
    plt.close()

def exportCSV(ch_num, bout_time_pair, chart_dir, title=None): #REVIEW: optimization required
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
