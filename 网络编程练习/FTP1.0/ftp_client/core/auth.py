

from  conf import settings
from  tool import Md5

def login():
    count = 3
    f = open(settings.userinfo,encoding='utf-8')
    content = f.readlines()
    while count > 0:
        print('----请登录系统-----')
        in_name = input('输入您的用户名:').strip()
        in_pwd = input('输入您的密码:').strip()
        in_pwd = Md5.get_md5(in_pwd)            #对输入的密码进行MD5操作
        for i in content:
            name,pwd,identity = i.strip().split('|')
            if in_name == name and in_pwd == pwd:
                print('%s：%s 登录成功'%(identity,name))
                return {'name':name,'identity':identity}
        else:
            count -= 1
            if count > 0:
                print('用户名或密码错误,还有%s次机会'%count)
            if count == 0:
                quit('错误次数过多，已退出')
            continue
