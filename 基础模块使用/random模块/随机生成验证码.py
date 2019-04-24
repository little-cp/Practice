def v_code(n=6):  #定义验证码函数,位数默认为6
    import random
    s = ''
    for i in range(n):#循环n次
        lower = random.choice([chr(random.randint(97,122))])#随机生成小写
        upper = random.choice([chr(random.randint(65,90))])#随机生成大写
        num = str(random.randint(0,9))    #随机生成一个0-9之间的整数
        choice = random.choice([lower,upper,num])#随机从上面3个中选一个
        s += choice
    return s

print(v_code())


