import time
struct_time = time.localtime()
user_info = {'user': None, 'status': False}  # 存用户名和登录状态


def main():  # 首页,进行交互
    l = ['请登录', '请注册', '文章页面', '日记页面', '评论页面', '收藏页面', '注销', '退出程序']
    print('欢迎来到博客园首页')
    for i, j in enumerate(l, 1):
        print(i, j)
    d = {1: login, 2: register, 3: article, 4: diary,
         5: comment, 6: collection, 7: logout, 8: quit}

    choice = input('请选择:')
    if choice.isdigit():
        choice = int(choice)
        if choice in d.keys():
            return d[choice]()
        else:
            print('请输入1-8之间的一个数')
    else:
        print('您的输入有误!请重新输入!')


def log(fn):  # 日志装饰器
    def inner(*args, **kwargs):
        fn_name = fn.__name__  # 拿到函数名
        clock = time.strftime("%Y-%m-%d %H:%M:%S", struct_time)  # 拿到调用时间
        f = open('日志.txt', 'a', encoding='utf-8')
        f.write('%s %s 访问 %s\n' %
                (clock, user_info['user'], fn_name))  # 将函数名,调用时间追加到日志文件中
        ret = fn(*args, *kwargs)
        return ret
    return inner


def status(fn):  # 判断登录状态装饰器
    def inner(*args, **kwargs):
        if user_info['status']:
            return fn(*args, **kwargs)
        else:
            print('您还未登录')
            print('正在为您跳转到首页')
            time.sleep(1)
            main()
    return inner


def login():
    count = 3
    f = open('注册信息.txt', encoding='utf-8')
    content = f.readlines()
    while count > 0:
        print('----请登录系统-----')
        name = input('输入您的用户名:').strip()
        password = input('输入您的密码:').strip()
        for i in content:
            if name == i.split()[0] and password == i.split()[1]:
                print('登陆成功')
                user_info['user'] = name
                user_info['status'] = True
                print('正在为您跳转到首页')
                time.sleep(1)
                return main()
        else:
            count -= 1
            if count > 0:
                print('用户名或密码错误,还有%s次机会' % count)
            if count == 0:
                quit('错误次数过多，已退出')
            continue


def register():
    dic = {}
    f = open('注册信息.txt', encoding='utf-8')
    for i in f:
        name,pwd = i.split()
        dic[name] = pwd  # 用字典存账户密码
    while 1:
        print('---注册您的账户---')
        account = input('设置用户名:').strip()
        if account in dic.keys():
            print('用户名已被注册,请使用其它用户名')
            continue
        else:
            key = input('请设置密码:').strip()
            f = open('注册信息.txt', 'a', encoding='utf-8')
            f.write('\n%s %s' % (account, key))  # 追加至register文件
            f.flush()
            f.close()
            user_info['user'] = account
            user_info['status'] = True
            print('已为您自动登录')
            print('正在跳转到首页...')
            time.sleep(1)
            return main()


@status
@log
def article():
    print('欢迎 %s 用户访问文章页面' % user_info['user'])


@status
@log
def diary():
    print('欢迎 %s 用户访问日记页面' % user_info['user'])


@status
@log
def comment():
    print('欢迎 %s 用户访问评论页面' % user_info['user'])


@status
@log
def collection():
    print('欢迎 %s 用户访问收藏页面' % user_info['user'])


def logout():  # 注销,先判断是否登录
    if user_info['status'] is True:
        user_info['status'] = False
        print('已注销')
    else:
        print('您尚未登录')


while 1:
    main()
