module specialItems

export sheetTitle, takenTime, eyedSpan, episodeGap, videoEpisodeGap, targetPath, eyePath, chartDirForCh, frequency, sessionID
##### 基本常量设置
const sessionID = "20171021002"

const sheetTitle = [(0,Symbol("1 CH_0"),Symbol("701 CH_0_P")),
                    (1,Symbol("2 CH_1"),Symbol("702 CH_1_P"))]

const frequency = 1000

const takenTime = (60,1800)  #seconds NOTE:跳过前60秒的数据，避免power引起的数据的扭曲; 跳过1800秒后的数据，方便统计数据。
const eyedSpan = [(60,800)]  #seconds NOTE: 人工分析的时间段

const episodeGap = 4         #seconds NOTE: episode聚类间隔时长
const videoEpisodeGap = 4    #seconds NOTE: 对视频采用episode分析



##### 地址设置
const basePath = splitdir(@__FILE__)[1]
const targetPath = joinpath(basePath, "data", "$(sessionID)_PW.txt")
const eyePath = joinpath(basePath, "data", "$(sessionID)_eye_10min.csv")
const chartDir = joinpath(basePath, "chart")
isdir(chartDir) || mkdir(chartDir)
#const chartDirForCh = ["$(chartDirRoot)0","$(chartDirRoot)1"]
#map(x -> isdir(x) || mkdir(x), chartDirForCh)

end
