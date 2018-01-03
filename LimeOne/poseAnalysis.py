import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from .database import createNewSessionTable

def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def posePlot(name, thresh, array):
    plt.figure(figsize=(50,2))
    plt.plot(np.linspace(0,len(array)/25,len(array)),array)
    plt.plot([0,3600],[thresh,thresh])
    plt.xlim((0,3600))
    plt.savefig(name, bbox_inches='tight')

def poseCheck_DB(dbCursor, session_name, sessionID, offset, output='.', ncage=2, scale = 1):
    dbCursor.execute("SELECT * FROM %s"%('POSE_'+session_name))
    raw = dbCursor.fetchall()

    title = ['frame','time']+['p%d'%(i+1) for i in range(ncage)]
    data = pd.DataFrame(raw, columns=title)

    pbar = tqdm(total=len(data)*ncage)


    for each in range(ncage):
        array = data['p%d'%(each+1)].values
        thresh = array.mean() - array.std()
        pool = []
        for index in range(len(data)):
            item = data.iloc[index]
            if item['p%d'%(each+1)] < scale*thresh:
                pool.append(item['time'] - offset)
            pbar.update(1)
        targetList = [ (int(index), float(item[0]),float(item[-1])) for index, item in enumerate(group_consecutive(pool)) ]
        title = ['start','end']
        createNewSessionTable(dbCursor, sessionID[each]+"_Climb", title, targetList)

        posePlot(os.path.join(output,sessionID[each]+"_Climb.png"),thresh, array)
    pbar.close()

    return
