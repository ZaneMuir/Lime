import pandas as pd
from .analysis import eye_data_episode
import numpy as np
def main(eyeDataFilePath, eyeEpisode=None):
    #print(eyeDataFilePath)
    data = pd.read_csv(eyeDataFilePath)

    if eyeEpisode != 0:
        seg = eye_data_episode(data, episode_gap=eyeEpisode)
        return len(seg), np.sum([item[1]-item[0] for item in seg]),seg
    else:
        seg = data['end'].values - data['start'].values
        return seg.shape[0],seg.sum(),seg


if __name__ == '__main__':
    import sys
    print(main(*sys.argv[1:]))
