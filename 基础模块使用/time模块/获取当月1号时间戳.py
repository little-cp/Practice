def get_day01():
    import time
    now = time.strftime('%Y%m')     #拿到当前时间,只显示年,月,这样日就默认为1
    day01= time.strptime(now,'%Y%m')    #本月一号的结构化时间
    timestamp = time.mktime(day01)      #所要的时间戳
    return timestamp

ret =get_day01()
print(ret)