t0 = time()
push!(LOAD_PATH, splitdir(@__FILE__)[1])
import specialItems:episodeGap
import normalization:process_powered_sheet
import analysis:horizontal_log_thresh_method, group_consecutive
import visualization: exportcsv

@time for (chNum, timeArray, chArray, powerArray, _) in process_powered_sheet()

    dataSheet, onThresh = horizontal_log_thresh_method(timeArray, powerArray)
    #info("Channel $chNum\nonThresh as: ",onThresh)

    boutArray = group_consecutive(dataSheet, step=episodeGap)

    exportcsv(chNum,boutArray)

    #TODO: plot figures
end
println("  wall time: $(time()-t0) seconds")
