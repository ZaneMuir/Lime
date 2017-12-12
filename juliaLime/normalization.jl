module normalization

using DataFrames
using CSV

import specialItems: targetPath, takenTime, sheetTitle, frequency
export process_powered_sheet

#=导入数据文件=#
function process_powered_sheet(filePath = targetPath)
    const dataSheet = CSV.read(filePath, nullable=false, delim='\t')[takenTime[1]*frequency:takenTime[2]*frequency,:]
    const timeSpan = dataSheet[:Time]
    normalizedData = Array{Tuple}(2)
    for (chNum, chTitle, powerTitle) in sheetTitle
        chRaw = dataSheet[chTitle]
        powerRaw = dataSheet[powerTitle]

        normalizedData[chNum+1] = (chNum, timeSpan, chRaw, powerRaw, nothing)
    end
    return normalizedData
end
end
