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

    entryResult = []
    for index, (ch_num, time_array, raw_array, power_array, _ ) in enumerate(process_powered_sheet(sensor_file, time_range)):

        loc, scale = stats.norm.fit(np.log10(power_array))
        thresh = 10**(loc+scale) if power_array.max() > 0.0005 else 0.0005
        #TODO:distribution plot?

        bout = np.sign(power_array - thresh)
        table = pd.DataFrame(   np.hstack((time_array[:,np.newaxis], bout[:,np.newaxis])),
                                columns=['time','bout'])

        try:
            bout_time_pair = [(index, item[0],item[-1]) for index, item in enumerate(group_consecutive(table[table.bout > 0]['time'].values,step=episode_gap))]
        except IndexError:
            print("with no chewing")
            bout_time_pair = [(0,0,0)]

        title=['start','end']
        createNewSessionTable(dbCursor, sessionID[ch_num]+'_Bout', title, bout_time_pair)
