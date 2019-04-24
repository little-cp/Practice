'''开哥的思路,感觉更简洁'''


def kaige(total_money, n):
    import random
    l = range(1, total_money * 100)
    money = []
    s = random.sample(l, n - 1)
    s.append(total_money * 100)  # 分别在一头一尾插入0和红包总金额
    s.insert(0, 0)
    s.sort()  # 排序
    # print(s)
    # print(len(s))
    for i in range(len(s) - 1):  # 这里得len-1,因为加了加了一头一尾
        m = float(s[i + 1] - s[i]) / 100
        money.append(m)
    print('红包已抢完!记录如下:')
    print(money)
    best = max(money)  # 手气最好
    number = money.index(best)
    print('第%s个人手气最好,抢到了%s元' % (number + 1, best))


kaige(200, 5)

'''这个算法是看的网上的分析'''


def red_envelope(total_money, n, min_money=0.01):  # 总金额,人数,规定最小红包金额,默认1分
    import random
    print('红包总金额:%s 红包个数:%s 红包金额下限%s' % (total_money, n, min_money))
    total_money = float(total_money)
    n = int(n)
    l = []
    left = total_money  # 剩余金额
    i = 1
    while i < n:
        max_money = left - min_money * (n - i)  # 给剩下的每个人预留0.01
        k = int((n - i) / 2)  # k近似为剩余人数的一半
        if n - i <= 2:
            k = n - i
        max_money = max_money / k  # 保证每次最大红包都大约为平均值(总金额/总人数)的2倍
        money = random.randint(int(min_money * 100), int(max_money * 100))
        money = float(money) / 100  # 到小数点后两位
        left -= money
        print("第%d个人抢到红包为:%.2f, 红包余额:%.2f" % (i, money, left))  # 逐个打印每人抢到的金额,以及余额
        l.append(money)  # 将金额存入列表
        i += 1

    print("第%d个人拿到红包为:%.2f, 余额:%.2f" % (i, left, 0.00))  # 打印最后一个人的
    l.append(int(left * 100) / 100)  # 转成最多小数点后两位
    best = max(l)  # 找到最大红包
    number = l.index(best) + 1  # 找到对应序号
    print('红包已抢完!第%s个人手气最佳,抢到了%s元' % (number, best))
    return l

# red_envelope(200,5)
