# Purpose and Usage
将人工分析的xlsx结果转换成“分析友好”的csv格式。
特别的，xlsx需要满足以下几点：[具体可参见demo.xlsx文件]
1. 所有数据从B5单元格开始
2. B列为start的帧数，C列为end的帧数，D列为人工筛选的结果
3. 对于人工筛选的结果一列，所有标记均会在处理时将所在行的数据去除，标记仅作为error code

```
eye_xlsx2csv.py
convert xlsx file into programming-friendly csv file

Usage: eye_xlsx2csv.py [FILE] [-o OUTPUT]

Options:
FILE: 输入的xlsx文件地址
-o OUTPUT: 输出的文件名, 若未申明则与输入文件文件名相同

Example:
eye_xlsx2csv.py demo.xlsx
eye_xlsx2csv.py demo.xlsx -o abc.csv
eye_xlsx2csv.py demo.xlsx -o abc
```



# Requirements
