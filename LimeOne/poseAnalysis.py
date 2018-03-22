u"""
poseAnalysis.

主要包含了对视频数据处理的函数

主要的思路为：
计算每个区域灰度的阈值(mean-std)，
然后选取在阈值以下的时刻，
从而获得攀爬的起始与终止时间。
"""

import pandas as pd
import numpy as np
import os
from tqdm import tqdm
import matplotlib.pyplot as plt
from .database import createNewSessionTable


def group_consecutive(a, step=1):
    """
    Group consecutive numbers in an array.

    modified from https://zhuanlan.zhihu.com/p/29558169
    """
    return np.split(a, np.where(np.diff(a) > step)[0] + 1)


def posePlot(name, thresh, array):
    u"""显示中间过程的图像，x轴为时间，y轴为灰度值，横线为阈值."""
    plt.figure(figsize=(50, 2))
    plt.plot(np.linspace(0, len(array)/25, len(array)), array)
    plt.plot([0, 3600], [thresh, thresh])
    plt.xlim((0, 3600))
    plt.savefig(name, bbox_inches='tight')


def poseCheck_DB(dbCursor, session_name, sessionID,
                 offset, output='.', ncage=2, scale=1):
    u"""
    分析视频数据.

    poseCheck_DB(
        dbCursor::sqlite3.cursor,
        session_name::string,
        sessionID::list,
        offset::float, 视频中“开始”的时刻
        output::string, 图像输出的目录
        ncage::int, 总的笼数
        scale::int
    )
    """
    # 获取视频原始数据
    dbCursor.execute("SELECT * FROM %s" % ('POSE_'+session_name))
    raw = dbCursor.fetchall()

    # 转化为DataFrame，之所以没有用pandas自带的sql读取，
    # 是因为pandas有时候会有一些奇奇怪怪的meta信息出来
    title = ['frame', 'time']+['p%d' % (i+1) for i in range(ncage)]
    data = pd.DataFrame(raw, columns=title)

    pbar = tqdm(total=len(data)*ncage)  # 初始化tqdm进度条

    for each in range(ncage):  # 对每只老鼠做以下操作：
        array = data['p%d' % (each+1)].values  # 获取该只老鼠的视频信息
        thresh = array.mean() - array.std()  # 计算阈值
        pool = []
        for index in range(len(data)):  # 对所有的数据进行历遍
            item = data.iloc[index]
            if item['p%d' % (each+1)] < scale*thresh:  # 若灰度值小于阈值
                pool.append(item['time'] - offset)   # 则记录时刻(并减去offset值)
            pbar.update(1)
        # 此时得到的pool为一维的数组，包含大量连续的时刻点(increment: 0.001)
        # 利用一下语句分割并格式化为新的列表： [(index, start, end), ...]
        targetList = [(int(index), float(item_t[0]), float(item_t[-1]))
                      for index, item_t in enumerate(group_consecutive(pool))]

        title = ['start', 'end']  # 新表格的title
        createNewSessionTable(dbCursor, sessionID[each]+"_Climb",
                              title, targetList)  # 创建新的表格

        posePlot(os.path.join(output, sessionID[each]+"_Climb.png"),
                 thresh, array)  # 绘制中间信息的图像
    pbar.close()

    return
