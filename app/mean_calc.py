#リストの平均値を求める
def calc_mean(list):
    Mean = sum(list)/len(list)
    return Mean

#リストの最頻値を求める
def calc_mode(list):
    return statistics.mode(list)

#リストの分散を求める
def calc_var(list):
    return statistics.variance(list)

#リストの標準偏差を求める
def calc_stdev(list):
    return statistics.stdev(list)