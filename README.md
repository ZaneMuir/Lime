# Usage
调整 ```special_items.py``` 文档中的各项参数；运行 ```power_protocol.py``` 文件。
完成后数据与图片将保存于```chart/{SessionName}_{Gap}_{Ch_Num}```文件夹内。

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
- halo [optional]

# ChangeLog
### v1.0 - processing
- [ ] 纠正数学模型的错误

### v0.3 - 2017-10-08
- [x] eye excel converter
- [x] 恢复对双[多]通道的分析
  - [x] misc process
  - [x] image export
  - [x] eye data import
- [x] 利用log后的数据求sigma[[jupyter notebook demo](https://nbviewer.jupyter.org/github/ZaneMuir/Lime/blob/master/demo/demo_data_distribution.ipynb)]
- [x] 时间切片，只选取60-1800秒
- [x] Windows 友好
- [x] 精简代码，增加注释

### v0.2 - 2017-10-05
- [x] 对各个操作进一步模块化，可以更方便的调试不同的分析算法
- [x] 支持对视频分析结果进行简单的episode算法聚类 [[jupyter notebook demo](https://nbviewer.jupyter.org/github/ZaneMuir/Lime/blob/master/demo/demo_video_episode.ipynb)]

### v0.1 - 2017-09-24
- [x] 专为检验视频分析而定制: ie. 仅分析Ch1数据 [demo: demo720.mov]
- [x] 支持任意Mac系统运行
