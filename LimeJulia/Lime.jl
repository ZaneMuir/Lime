module LimeOne

end  # module LimeOne

using DocOpt
using SQLite
using DataFrames

const version = v"1.2.0-dev"
const doc = """
Lime $version
analysis program for chewing behavior of Zhang's Lab.

Usage:
    lime.py [options] SENSORFILE [VIDEOFILE]

Options:
    -b DATABASENAME --database=DATABASENAME     # database file path [default: chewing.db]
    -c GAP --climbEpisode=GAP                   # climbing episode gap length, unit as second [default: 0]
    --debug                                     # debug mode
    -d DATE --date=DATE                         # session date [default: YYYYMMDD]
    -e GAP --episode=GAP                        # episode gap length, unit as second [default: 4]
    -f FOOD --food=FOOD                         # food weight data, unit as gram [default: 2.000_1.000]
    -i INDIR --input=INDIR                      # data directory [default: data]
    -l LENGTH --length=LENGTH                   # session length, unit as minute [default: 60]
    -m MICESEQ --miceSequence=MICESEQ           # mice sequence, from left to right [default: C1M1/C1M2/C1M3/C1M4]
    -n NCAGE --cageSum=NCAGE                    # total mice number in this session [default: 2]
    -o OUTDIR --output=OUTDIR                   # chart directory [default: chart]
    -p POSEANA --poseAnalysis=POSEANA           # need pose analysis only? [default: True]
    -r RANGE --timeRange=RANGE                  # checking range, unit as second [default: 60_3600]
    -t TIME --startTime=TIME                    # start time point [default: HHMM]
    -u SETUP --setup=SETUP                      # setup prefix, one of "TtC_NN","TtC_NH", "TtC_HH", "TtV_NN","TtV_NH", "TtV_HH" [default: TtV_NN]
    -v OFFSET --videoOffset=OFFSET              # video offset, aligning with sensor time, counts as second [default: 0.0]
    -w WIDTH --width=WIDTH                      # target area width, unit as px [default: 20]

typical command for 4-mice setup:
```lime.py -d 20171213 -t 1430 -u TtC_NH -n 4 -m C1M1/C2M1/C1M2/C2M2 -v 17 -f 3.653_3.142/3.653_3.142/3.653_3.142/3.653_3.142 20171213001_PW.txt 20171213001.mov```

tips: easier for editing to write these commands into an sh file.
"""
arguments = docopt(doc, version=version)

#=
{"--cageSum": "4",
 "--climbEpisode": "0",
 "--database": None,
 "--date": "20171213",
 "--debug": True,
 "--episode": "4",
 "--food": "3.653_3.142",
 "--input": "data",
 "--length": "60",
 "--miceSequence": "C1M1/C2M1/C1M2/C2M2",
 "--output": "chart",
 "--poseAnalysis": "True",
 "--setup": "TtC_NH",
 "--startTime": "1430",
 "--timeRange": "60_3600",
 "--videoOffset": "17",
 "--width": "20",
 "SENSORFILE": "20171213001_PW.txt",
 "VIDEOFILE": "20171213001.mov"}
=#
# debug mode
if arguments["--debug"]
    print(arguments)
    print("\n")
end

# if output directory not exists, create one.
if ! isdir(arguments["--output"])
    mkdir(arguments["--output"])
end

if ! isfile(joinpath(arguments["--input"], arguments["--database"]))
    # there is no database file, then create one here
    #TODO: create new database
end

# connect with sqlite3 database
sqldb = SQLite.DB(joinpath(arguments["--input"], arguments["--database"]))

# pre-parsing
sessionName = match(r"(\d{11})_PW\.txt",arguments["SENSORFILE"])[:1]
mice = split(arguments["--miceSequence"], "/")
sessionID = [   arguments["--setup"] * "_" *
                mice[i] * (i%2 == 1 ? "_L_" : "_R_") *
                arguments["--date"] * "_" * arguments["--startTime"] * "_" *
                arguments["--length"]
                for i = 1:parse(arguments["--cageSum"])]
oppositeMouseIndex = x -> x + (-1) ^ x


#=
# 如果输入了视频文件，则分析视频。
if isempty(arguments["VIDEOFILE"])
    print("step 1/4: video analysis, SKIP\n")
else
    print("step 1/4: video analysis\n")
    LimeOne.videoMain #TODO
end

# 对视频选取的数据是否需要分析
if arguments["--poseAnalysis"]
    print("step 2/4: pose analysis\n")
    LimeOne.poseCheck #TODO
else:
    print("step 2/4: pose analysis, SKIP\n")

print("step 3/4: sensor analysis")
result = LimeOne.finalMain #TODO

#TODO 生成summary表格中的条目信息
session_summary_info = []

LimeOne.createNewSessionSummaryEntry #TODO

print("ALL DONE!")
=#
