module visualization
using CSV

import specialItems: chartDir, sessionID

export exportcsv

function exportcsv(chNum::Int, boutArray::Array{Array{Float64,1}})
    title = "name,start,end,start_t,end_t\n"
    body = ""
    int2time = x -> "$(Int(fld(x,60))):$(rem(x,60))"
    for i = 1:length(boutArray)
        body *= "bout_$i,$(boutArray[i][1]),$(boutArray[i][2]),$(int2time(boutArray[i][1])),$(int2time(boutArray[i][2]))\n"
    end
    fileName = "$(sessionID)_$(chNum)_bout.csv"
    write(joinpath(chartDir,fileName), title*body)

end

end  # module visualization
