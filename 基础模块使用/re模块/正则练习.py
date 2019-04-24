import re

'''1.匹配整数或者小数'''
# a = re.findall('[-]?\d+(?:\.\d+)?','23123.43rtr-45.4yg')
# print(a)

'''2.匹配年月日'''
# a = re.findall('\d{4}-[0-9][0-9]-[0-9][0-9]','qw2018-08-12dhfg')
# print(a)

'''3.qq号'''
# a= re.findall('[1-9][\d+]{5,11}','cpp123456789iji')
# print(a)

'''4.手机号'''
# a = re.findall('1[3-9][0-9]{9}','78as67ad45131489498698wqe3232')
# print(a)

'''5.用户密码：数字字母下滑线'''
# a = re.findall('[\w]{8,10}','`/dhqwue_h233_iuy')
# print(a)

'''6.验证码'''
# a = re.findall('[a-zA-Z0-9]{4}','@#we4roi-uyo9)')
# print(a)


'''7.邮箱'''
# a = re.findall('\w+@\w+\.com','1231erer241@qq.com543erw')
# print(a)

'''8.1).'''
# s = '<a>wahaha</a>'
# a = re.findall(r'<\w+>(\w+)',s)
# print(a)
'''8.2).'''
# s = '<a>wahahah</a>'
# b = re.findall(r'<(\w+)>\w+',s)
# print(b)

'''9.'''
# s = '1 - 2 * ( (60-30 +(-40/5) * (9-2*5/3 + 7 /3*99/4*2998 +10 *568/14 )) - (-4*3)/ (16-3*2) )'
# exp = s.replace(' ','')
# print(exp)
# a = re.findall('\([^()]+\)',exp)
# print(a)

'''10.'''
# s = '9-2*5/3+7/3*99/4*2998+10*568/14'
# a = re.search(r'[-]?\d+(\.\d+)?[/*]-?\d+(\.\d+)?',s)
# print(a.group())

'''11.'''
# s = 'ewq232eThe Voice Of China ioc er cc'
# a = re.findall('(?:[A-Z](?:[a-z]+)?[\s]*)+',s)
# print(a)

'''12.'''
# s = '232dhttps://www.cnblog123.com4543ewqe'
# a = re.findall('(?:https|http)://www\.\w+\.com',s)
# print(a)

'''13.'''
# s = 'weqwe2018-01-0642342dsfsd'
# a = re.findall('\d{4}[- .][0-9][0-9][- .][0-9][0-9]',s)
# print(a)

'''14.'''
# s = 'weqeq11038419950744854Xvb110381199807118rtge'
# a = re.findall('[1-9][\d]{14}(?:\d{2}(?:\d|X))?',s)
# print(a)

'''15.'''


f = open('lianjia.html', 'r', encoding='utf-8')
content = f.read()
res = re.findall('<div class="info clear">.*?<a class="".*?>(?P<title>.*?)</a>.*?<span class="divide">/</span>(?P<type>.*?)<span class="divide">/</span>(?P<size>.*?)<span class="divide">/</span>', content, re.S)
print('匹配结果如下：')
print(res)
f.close()
