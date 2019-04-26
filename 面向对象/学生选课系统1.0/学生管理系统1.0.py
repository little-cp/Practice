import pickle
import sys
import os
import hashlib

base_path = os.path.dirname(os.path.dirname(__file__))
sys.path.append(base_path)


class Password():  #用于加密
    def get_md5(s):  # 加密函数，将存储的密码变成密文
        a = hashlib.md5()
        a.update(bytes(s, encoding='utf-8'))
        a = a.hexdigest()
        return a


class Father(object):  # 父类
    def log_out(self):  # 退出
        exit('已退出选课系统')

    def check_course(self):  # 查看课程
        with open('课程信息.txt', 'rb') as f:
            while 1:
                try:
                    obj = pickle.load(f)
                    print('课程名：%s 价格：%s 周期：%s' % (obj.name, obj.price, obj.period))
                except EOFError:
                    break

    def write_file(self, file_path, mode_type, file_content):
        with open(file_path, mode_type, file_content) as f:
            pickle.dump(file_content, f)


class Course():
    def __init__(self, name, price, period):
        self.name = name
        self.price = price
        self.period = period


class Student(Father):
    operation_list = [('查看可选课程', 'check_to_choose'),
                      ('查看已选课程', 'check_chosen_course'),
                      ('选择课程', 'choose_course'),
                      ('退出', 'log_out')]

    def __init__(self, name):
        self.name = name
        self.course = []

    def check_to_choose(self):  # 查看可选课程
        self.check_course()

    def choose_course(self):  # 选课
        with open('课程信息.txt', 'rb') as f:
            i = 1
            l =[]
            dic = {self.name:l}
            while 1:
                try:
                    obj = pickle.load(f)
                    i += 1
                    l.append((obj.name, obj.price, obj.period))
                except EOFError:
                    break
            while 1:
                a = input('是否继续?(q或Q退出,其他任意键继续)\n')
                if a.upper() == 'Q':
                    break
                else:
                    for index, i in enumerate(l, 1):
                        print(index, i)
                    choice = input('输入数字选择对应课程：')
                    if choice.isdigit():
                        choice = int(choice)
                        self.course.append(l[choice - 1])
                        with open('选课信息.txt','ab') as f1:
                            pickle.dump(self,f1)
                        print('已选择：',self.course)

    def check_chosen_course(self):  # 查看已选课程
        with open('选课信息.txt','rb') as f:
            dic = {}
            while 1:
                try:
                    situation = pickle.load(f)
                    dic[situation.name] = situation.course
                except EOFError:
                    break
            print(self.name+':',dic[self.name])



class Admin(Father):
    operation_list = [('创建学生账号', 'create_stu'),
                      ('创建课程', 'create_course'),
                      ('查看全部课程', 'check_all_course'),
                      ('查看全部学生', 'check_stu'),
                      ('查看选课情况', 'check_situation'),
                      ('退出', 'log_out')]

    def __init__(self, name):
        self.name = name

    def create_stu(self):  # 创建学生账号
        while 1:
            a = input('是否继续?(q或Q退出,其他任意键继续)\n')
            if a.upper() == 'Q':
                break
            else:
                print('---创建学生账户---')
                account = input('设置用户名:').strip()
                key = input('设置密码:').strip()
                key = Password.get_md5(key)
                f = open('用户信息.txt', 'a', encoding='utf-8')
                f.write('\n%s|%s|Student' % (account, key))  # 追加至用户信息文件
                print('学生%s的信息创建成功' % account)
                f.close()
                stu_obj = Student(account)
                f1 = open('学生信息.txt', 'ab')
                pickle.dump(stu_obj, f1)
                f1.close()

    def create_course(self):  # 创建课程
        while 1:
            a = input('是否继续?(q或Q退出,其他任意键继续)\n')
            if a.upper() == 'Q':
                break
            else:
                name = input('输入要创建的课程名:').strip()
                price = input('输入课程价格:').strip()
                period = input('输入课程周期:').strip()
                course_obj = Course(name, price, period)
                with open('课程信息.txt', 'ab') as f:
                    pickle.dump(course_obj, f)
                print('课程创建成功')

    def check_all_course(self):  # 查看全部课程
        self.check_course()

    def check_stu(self):  # 查看全部学生
        with open('学生信息.txt', 'rb') as f:
            while 1:
                try:
                    stu = pickle.load(f)
                    print(stu.name+',',end='')
                except EOFError:
                    print('')
                    break

    def check_situation(self):
        with open('选课信息.txt','rb') as f:
            dic = {}
            while 1:
                try:
                    situation = pickle.load(f)
                    dic[situation.name] = situation.course
                except EOFError:
                    break
            for k,v in dic.items():
                print(k+':',v)


def login():  # 登录函数
    count = 3
    f = open('用户信息.txt', encoding='utf-8')
    while count > 0:
        print('----请登录系统-----')
        in_name = input('输入您的用户名:').strip()
        in_pwd = input('输入您的密码:').strip()
        in_pwd = Password.get_md5(in_pwd)  # 对用户输入的密码进行MD5运算
        for i in f:
            name, pwd, identity = i.strip().split('|')
            if in_name == name and in_pwd == pwd:  # 两个MD5值相比较
                print('%s：%s 登录成功' % (identity, name))
                return {'name': name, 'identity': identity}
        else:
            count -= 1
            if count > 0:
                print('用户名或密码错误,还有%s次机会' % count)
            if count == 0:
                quit('错误次数过多，已退出')
            continue


def entry():
    ret = login()
    if ret:
        print('正在跳转到主页')
        cls = getattr(sys.modules[__name__], ret['identity'])  # 反射拿到对应的类（Admin或Student）
        obj = cls(ret['name'])  # 实例化一个对应的对象
        while 1:
            for index, i in enumerate(cls.operation_list, 1):
                print(index, i[0])
            choice = input('输入数字执行对应功能：')
            if choice.isdigit():
                choice = int(choice)
                if choice in range(1, len(cls.operation_list) + 1):
                    operation = cls.operation_list[choice - 1][1]
                    getattr(obj, operation)()
                else:
                    print('输入数字有误，请重新输入！')
            else:
                print('请输入数字！')


entry()
