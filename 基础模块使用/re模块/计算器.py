import re


def deal_with(s):  # 处理两个+-符号连在一起的，分四种情况
    if '-+' in s:
        s = s.replace('-+', '-')
    if '+-' in s:
        s = s.replace('+-', '-')
    if '--' in s:
        s = s.replace('--', '+')
    if '++' in s:
        s = s.replace('++', '+')
    return s


def mul_div(exp):  # 处理 乘除法
    if '*' in exp:
        exp = exp.strip('()')
        a, b = exp.split('*')
        c = float(a) * float(b)
        return str(c)  # 转换成字符串
    elif '/' in exp:
        exp = exp.strip('()')
        a, b = exp.split('/')
        # print(a,b)
        c = float(a) / float(b)
        return str(c)


def calculate(exp):  # 计算带括号的最小子式
    while 1:
        res = re.search('\d+\.?\d*[*/]-?\d+\.?\d*', exp)  # 匹配乘除法
        if res:
            res = res.group().strip()
            ret = mul_div(res)  # 用定义好的乘除函数计算
            # print(ret)
            exp = exp.replace(res, ret, 1)
            # print(exp)
        else:
            break  # 算完该括号内所有乘除法
            # 计算加减法
    exp = deal_with(exp)  # 在计算加减之前,先做处理
    l = re.findall('[+-]?\d+\.?\d*', exp)  # 用findall,匹配带正负号的所有数字,这样更好算.不用乘除的那种方法
    sum = 0
    print(l)
    for i in l:
        i = float(i)  # 字符串转数字
        sum += i  # 统一用求和，减法 在匹配时 以负数 形式
    print(sum)
    return str(sum)  # 就是该括号内式子的值了,返回字符串类型


def core(s):
    s = s.replace(' ', '')  # 去掉算式中的空格，避免出错
    while 1:
        exp = re.search(r'\([^()]+\)', s)  # 先匹配最里层带括号的
        if exp:
            exp = exp.group()  # 如果匹配到，说明还有括号
            res = calculate(exp.strip('()'))  # 计算括号内式子的值
            s = s.replace(exp, res, 1)  # 将结果替换回原式
        else:  # 所有括号都去完了
            result = calculate(s)  # 再单独算一次
            break
    return result


s = ' 1 - 2 * ( (60-30 +(-40/5)  * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 )) - (-4*3)/ (16-3*2) )'
# s = '(60-30 -8 * (9-2*5/3 + 7 /3*99/4*2998 +10 * 568/14 ))'

a = core(s)
print(a)
print(eval(s))
