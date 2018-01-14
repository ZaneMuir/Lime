import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from .database import createNewSessionTable
def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def expandFrame(Frame, duration):
    result = np.zeros(duration*60*25)
    for index in range(len(Frame)):
        start = int(Frame.iloc[index]['start'])
        end = int(Frame.iloc[index]['end'])
        result[start:end] = 1
    return result

def mainDB(sessionID, dbCursor, duration, output):
    result = []

    for each in sessionID:
        chewing_result = []
        dbCursor.execute("SELECT * FROM %s"%each+'_Climb')
        climb = pd.DataFrame(dbCursor.fetchall(),columns=['n','start','end'])
        dbCursor.execute("SELECT * FROM %s"%each+'_Bout')
        bout = pd.DataFrame(dbCursor.fetchall(),columns=['n','start','end'])

        climbarray = expandFrame(climb[['start','end']]*25//1,duration)
        boutarray = expandFrame(bout[['start','end']]*25//1, duration)

        plt.figure(figsize=(50,2),dpi=300)
        plt.plot(np.linspace(0,duration*60,duration*60*25),boutarray)
        plt.plot(np.linspace(0,duration*60,duration*60*25),climbarray+0.25)

        for index in range(len(bout)):
            start = int(bout.iloc[index]['start'] * 25 // 1)
            end = int(bout.iloc[index]['end'] * 25 // 1)

            if 1 in climbarray[start:end]:
                boutarray[start:end] = 0

        plt.plot(np.linspace(0,duration*60,duration*60*25),boutarray+0.5)
        plt.xlim((0,3600))
        plt.savefig(os.path.join(output,each+'.png'), bbox_inches='tight')

        b_duration = boutarray.sum() / 25
        b_count = np.where(np.diff(boutarray) == -1)[0].shape[0]

        c_duration = climbarray.sum() /25
        c_count = np.where(np.diff(climbarray) == -1)[0].shape[0]

        title = ['start','end']
        times = np.linspace(0,3600,boutarray.shape[0])
        temp = pd.DataFrame(np.hstack((times[:,np.newaxis], boutarray[:,np.newaxis])), columns=['time','bout'])
        chewing_result = [(index, item[0],item[-1]) for index, item in enumerate(group_consecutive(temp[temp.bout == 1]['time'].values))]
        createNewSessionTable(dbCursor, each+'_Chew', title, chewing_result)

        result.append((b_count, b_duration, c_count, c_duration))
    return result



def main(ChewFilePath, EyeFilePath, outputName=None ,arguments=None):
    duration = count = 0

    chewFrame = pd.read_csv(ChewFilePath)[['start','end']]*25//1
    eyeFrame = pd.read_csv(EyeFilePath)[['start','end']]*25//1

    chewArray = expandFrame(chewFrame)
    eyeArray = expandFrame(eyeFrame)

    plt.figure(figsize=(50,2),dpi=300)
    plt.plot(np.linspace(0,3600,60*60*25),chewArray)
    plt.plot(np.linspace(0,3600,60*60*25),eyeArray+0.25)

    for index in range(len(chewFrame)):
        start = int(chewFrame.iloc[index]['start'])
        end = int(chewFrame.iloc[index]['end'])
        if 1 in eyeArray[start:end]:
            chewArray[start:end] = 0

    plt.plot(np.linspace(0,3600,60*60*25),chewArray+0.5)
    plt.xlim((0,3600))
    if outputName:
        plt.savefig(os.path.join(outputName,'chewing_plot.png'), bbox_inches='tight')
    else:
        plt.show()

    duration = chewArray.sum() / 25
    count = np.where(np.diff(chewArray) == -1)[0].shape[0]
    return duration, count




if __name__ == '__main__':
    import sys
    main(*sys.argv[1:])
