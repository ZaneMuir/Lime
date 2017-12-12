module analysis
using DataFrames
using Distributions

import specialItems: frequency

export horizontal_log_thresh_method

#=  目前计算阈值的方法
    对power的数据取log10, 用标准正态分布函数拟合[参考维基百科正态分布词条],
    得到mu(loc)和sigma(scale).
    阈值取10^(mu+sigma)'=#
function horizontal_log_thresh_method(timeArray, powerArray)
    logData = log10.(powerArray)
    fitModel = fit(Normal,logData)
    mu, sigma = params(fitModel)
    on_thresh = maximum(powerArray) < 0.0005 ? 0.0005 : 10^(mu+sigma)

    dataSheet = DataFrame([timeArray, powerArray, sign.(powerArray .- on_thresh)],[:time, :power, :thresh])
    #distribution_plot(ch_num, dataSheet, on_thresh)

    return dataSheet, on_thresh
end

#=python风格的分割数组
    运算效率感人
    对arr = 260072-element Array{Int64,1}, pos = 88-element Array{Int64,1}
    耗时 0.000545 seconds (136 allocations: 1.996 MiB)
=#
function split!(arr::AbstractArray, pos::AbstractArray)
    #TODO: boundaryCheck

    target = Array{Array}(length(pos)+1)
    target[1] = arr[1:pos[1]]

    for index = 1:length(pos)
        startIndex = pos[index]+1
        endIndex = index == length(pos) ? break : pos[index+1]
        target[index+1] = arr[startIndex:endIndex]
    end
    target[end] = arr[pos[end]+1:end]
    return target
end

#= 寻找datarise的点，并将时间点分割 =#
function group_consecutive(dataSheet; step=4, inname=:thresh, outname=:time)
    pos = find(x->x>0, dataSheet[inname])
    outArray = dataSheet[outname]
    posRisePos = find(x->x>step*frequency, diff(pos))
    posRange = split!(pos, posRisePos)

    boutArray = Array{Array{Float64,1}}(length(posRange))
    for index = 1:length(posRange)
        boutArray[index] = Array{Float64,1}([outArray[posRange[index][1]],outArray[posRange[index][end]]])
    end
    return boutArray
end

end  # module analysis
