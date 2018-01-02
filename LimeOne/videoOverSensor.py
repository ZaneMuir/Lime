import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
def group_consecutive(a,step=1):
    ''' group consecutive numbers in an array
        modified from https://zhuanlan.zhihu.com/p/29558169'''
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)

def expandFrame(Frame):
    result = np.zeros(60*60*25)
    for index in range(len(Frame)):
        start = int(Frame.iloc[index]['start'])
        end = int(Frame.iloc[index]['end'])
        result[start:end] = 1
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
