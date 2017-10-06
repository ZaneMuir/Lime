# Usage
调整 ```special_items.py``` 文档中的各项参数；运行 ```power_protocol.py``` 文件。
完成后数据与图片将保存于```chart/{SessionName}_{N}_{Gap}_{NoiseRange}```文件夹内。

# Requirements:
- numpy
- pandas
- matplotlib
- sklearn
- scipy
- docopt
- xlrd
- seaborn [optional]
- tqdm [optional]

# ChangeLog
### v0.2 - 2017-10-05
- 对各个操作进一步模块化，可以更方便的调试不同的分析算法
- 支持对视频分析结果进行简单的episode算法聚类 [[jupyter notebook demo](demo/demo_video_episode.ipynb)]

### v0.1 - 2017-09-24
- 专为检验视频分析而定制: ie. 仅分析Ch1数据 [demo: demo720.mov]
- 支持任意Mac系统运行

### FUTURE
- [ ] 恢复支持对双[多]通道的分析
- [ ] 自动寻找噪音区间 [[jupyter notebook demo](demo/noise_checker.ipynb)]
