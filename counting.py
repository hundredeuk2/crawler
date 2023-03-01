def cal(num):

    if num[-1] == "만":
        num = int(float(num[:-1])*10000)
    elif num[-1] == "천":
        num = int(float(num[:-1])*1000)
    elif num[-1] == "백":
        num = int(float(num[:-1])*100)
    else:
        num = int(num)
    num //=  40
    return num