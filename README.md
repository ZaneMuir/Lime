# Usage
调整 ```special_items.py``` 文档中的各项参数；运行 ```power_protocol.py``` 文件。\
完成后数据与图片将保存于chart文件夹内。

# Requirements:
- numpy
- pandas
- matplotlib
- sklearn
- scipy
- seaborn [optional]
- tqdm [optional]

# ChangeLog
### v1.1 - Processing
- [ ] 对各个操作进一步模块化，可以更方便的调试不同的分析算法[[jupyter notebook demo](demo/demo_v1_1.ipynb)]
- [ ] 支持对双[多]通道的分析
- [ ] 支持对视频分析结果进行简单的episode算法聚类 [[jupyter notebook demo](demo/demo_video_episode.ipynb)]
- [ ] 自动寻找噪音区间 [[jupyter notebook demo](demo/noise_checker.ipynb)]

### v1.0 - 2017-09-24
- [x] 专为检验视频分析而定制，仅分析Ch1数据 [demo: demo720.mov]
- [x] 支持任意Mac系统运行
