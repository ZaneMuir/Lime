'''eye_xlsx2csv.py
convert xlsx file into programming-friendly csv file

Usage: eye_xlsx2csv.py [FILE] [-o OUTPUT]

Options:
FILE: 输入的xlsx文件地址
-o OUTPUT: 输出的文件名, 若未申明则与输入文件文件名相同

example:
eye_xlsx2csv.py demo.xlsx
eye_xlsx2csv.py demo.xlsx -o abc.csv
eye_xlsx2csv.py demo.xlsx -o abc
'''

import xlrd
from docopt import docopt
import os


def exportCSV(data, csvName):
    if os.path.splitext(csvName)[1] != 'csv':
        csvName = os.path.splitext(csvName)[0] + '.csv'
    with open(csvName, 'w') as csvFile:
        csvFile.write( 'start,end\n')
        csvFile.write( '\n'.join( ['%.3f,%.3f'%tuple(item) for item in data] ) )
    print('export csv file:',csvName)
    return

def xlsx2csv(targetPath, csvName):
    book = xlrd.open_workbook(targetPath)
    sheet = book.sheet_by_index(0)
    nrows = sheet.nrows
    ncols = sheet.ncols

    start_array = sheet.col_values(1)[4:]
    end_array = sheet.col_values(2)[4:]
    note_array = sheet.col_values(3)[4:]

    print('data shape:',len(start_array), len(end_array),len(note_array))
    result_array = []
    for index in range(len(start_array)):
        if note_array[index] != '':
            print('remove point:',start_array[index],end_array[index],'with code:', note_array[index])
        else:
            result_array.append([start_array[index]/25, end_array[index]/25])

    #print(result_array)
    exportCSV(result_array, csvName)
    print('valid pairs:',len(result_array))
    print('done!')

if __name__ == '__main__':
    arguments = docopt(__doc__)
    if arguments['FILE'] == None:
        arguments['FILE'] = input("target file path:")
    #print(arguments)

    xlsx2csv(targetPath = arguments['FILE'],
        csvName = arguments['OUTPUT'] if arguments['-o'] else arguments['FILE'])
