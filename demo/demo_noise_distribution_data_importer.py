import pandas as pd
import numpy as np
from tqdm import tqdm

target_array = [
    ['20170906_000','/Users/zane/Documents/MyDocuments/Plans/4-Horizon/Contagious_Behavior/bout_analysis/data/20170906_000.txt'],
    ['20170906_001','/Users/zane/Documents/MyDocuments/Plans/4-Horizon/Contagious_Behavior/bout_analysis/data/20170906_001.txt'],
    ['20170906_003','/Users/zane/Documents/MyDocuments/Plans/4-Horizon/Contagious_Behavior/bout_analysis/data/20170906_003.txt'],
    ['20170907_001','/Users/zane/Documents/MyDocuments/Plans/4-Horizon/Contagious_Behavior/bout_analysis/data/20170907_001.txt'],
    ['20170907_002','/Users/zane/Documents/MyDocuments/Plans/4-Horizon/Contagious_Behavior/bout_analysis/data/20170907_002.txt']]

title_array = [
    [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']],
    [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']],
    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']],
    [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']],
    [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']],
    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]]
#20170906_000:              [[0,'1 CH_0','702 CH_0_P'],[1,'2 CH_1','701 CH_1_P']]
#20170906_003:              [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#20170906_001,20170907_ :   [[0,'1 CH_0  ','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]
#FUTURE:                    [[0,'1 CH_0','701 CH_0_P'],[1,'2 CH_1','702 CH_1_P']]

def getData():
    result = [] #list([sessionName, chName, DataFrame(['time','raw','power'])])
    for index in tqdm(range(len(target_array))):
        sessionName = target_array[index][0]
        raw_sheet = pd.read_csv(target_array[index][1], sep='\t')
        time_array = raw_sheet['Time'].values
        for chName, raw_title, power_title in title_array[index]:
            raw_array = raw_sheet[raw_title].values
            power_array = raw_sheet[power_title].values
            data = pd.DataFrame(np.hstack((time_array[:,np.newaxis],raw_array[:,np.newaxis],power_array[:,np.newaxis])),
                columns=['time','raw','power'])
            result.append([sessionName,chName,data])
    return result
