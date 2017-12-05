import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt

header = [  'time',
            'leftX','leftY','leftW','leftH','leftLabel',
            'rightX','rightY','rightW','rightH','rightLabel']

def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def poseOutput(array, filename):
    try:
        targetList = [ (item[0],item[-1]) for item in group_consecutive(array)]
    except IndexError:
        targetList = [(0,0)]
    with open(filename,'w') as targetFile:
        targetFile.write('start,end\n')
        for start, end in targetList:
            targetFile.write('%.3f,%.3f\n'%(start,end))

def poseCheck(filename,outputName, offset, scale = 1):
    data = pd.read_csv(filename)
    l_lower = data[(data.leftY != -1) & (data.time > offset)]['leftY'].values+data[(data.leftY != -1) & (data.time > offset)]['leftH'].values
    r_lower = data[(data.rightY != -1) & (data.time > offset)]['rightY'].values+data[(data.rightY != -1) & (data.time > offset)]['rightH'].values
    l_thresh = l_lower.mean() - l_lower.std()
    r_thresh = r_lower.mean() - r_lower.std()
    l_pool = []
    r_pool = []

    for index in range(len(data)):
        item = data.iloc[index]
        if item['leftY'] != -1:
            if item['leftY'] + item['leftH'] < scale*l_thresh:
                l_pool.append(item['time']-offset)

        if item['rightY'] != -1:
            if item['rightY'] + item['rightH'] < scale*r_thresh:
                r_pool.append(item['time']-offset)

    poseOutput(l_pool,outputName%0)
    poseOutput(r_pool,outputName%1)

def poseCheck_line(filename,outputName, offset, scale = 1):
    data = pd.read_csv(filename)
    left = data['left'].values
    right = data['right'].values
    l_thresh = left.mean() - left.std()
    r_thresh = right.mean() - right.std()
    l_pool = []
    r_pool = []

    for index in range(len(data)):
        item = data.iloc[index]
        if item['left'] != -1:
            if item['left'] < scale*l_thresh:
                l_pool.append(item['time']-offset)

        if item['right'] != -1:
            if item['right'] < scale*r_thresh:
                r_pool.append(item['time']-offset)

    poseOutput(l_pool,outputName%0)
    poseOutput(r_pool,outputName%1)

    plt.figure(figsize=(50,2))
    plt.plot(np.linspace(0,len(left)/25,len(left)),left)
    plt.plot([0,3600],[l_thresh,l_thresh])
    plt.xlim((0,3600))
    plt.savefig(os.path.splitext(outputName%0)[0]+'.png', bbox_inches='tight')

    plt.figure(figsize=(50,2))
    plt.plot(np.linspace(0,len(right)/25,len(right)),right)
    plt.plot([0,3600],[r_thresh,r_thresh])
    plt.xlim((0,3600))
    plt.savefig(os.path.splitext(outputName%1)[0]+'.png', bbox_inches='tight')
