

def start():
    l = ['登录','注册','购物','退出']
    operation = {1:login,2:register,3:shop,4:quit}
    for i,j in enumerate(l,1):
        print(i,j);

    while 1:
        choice = int(input('请选择:'))
        if choice in operation.keys():
            return operation[choice]()
        else:
            print('请重新输入1-4之间的一个数')

def register():
    dic = {}
    print('---注册您的账户---')
    account = input('设置用户名:').strip()
    f = open('账户密码记录.txt',encoding='utf-8')
    content = f.readlines()
    for i in content:
        if account == i.split()[0]:
            print('用户名已被注册,请使用其它用户名')
            continue
    key = input('请设置密码:').strip()
    f = open('账户密码记录.txt','a',encoding='utf-8')
    f.write('\n%s %s'%(account,key))

def login():
    count = 3
    while count > 0:
        print('请登录系统')
        name = input('输入您的用户名:').strip()
        password = input('输入您的密码:').strip()
        f = open('账户密码记录.txt',encoding='utf-8')
        content = f.readlines()
        for i in content:
            if (name == i.split()[0]) and (password == i.split()[1]):
                print('%s登录成功'%name)
                return start()  #return跳出循环
        else:
            count -= 1
            print('用户名或密码输入有误,请重新输入\n'
                  '您还有%s次机会'%count)
            continue



def shop():
    goods = [['电脑', 1999], ['鼠标', 50], ['键盘', 200], ['路由器', 98]]  # 商品列表
    account = int(input('请先给您的账户充值:').strip())  # 提示充值
    shopping_list = []                 #购物清单
    print('-------商品列表如下-------')

    while 1:
        for i in goods:
            print(goods.index(i) + 1, i[0], i[1])  # 打印商品列表
        choice = input('输入商品序号:\n').strip()
        if choice.isdigit():  # 判断输入的是否为数字
            choice = int(choice)
            if 0 < choice <= len(goods):  # 避免数字超过列表长度
                print(goods[choice - 1])
                shopping_list.append(goods[choice - 1])  # 加入购物车
                print('已加购 ')
            else:
                print('序号输入有误,请重新输入')

        elif choice == 'n':
            print('结算，购物车如下:')
            print('商品', '  数量 ', ' 单价')  # 打印购物车
            price = 0
            for i in goods:
                if i in shopping_list:
                    amount = shopping_list.count(i)
                    print(i[0], ' * ', amount, ' ,', i[1])  # 统计同类商品个数
                    s = i[1] * amount
                    price = price + s  # 计算总价
            print('总金额：', price)
            while account < price:
                print('余额不足,请删除部分商品!')
                print(shopping_list)
                n = int(input('输入要删除的商品在清单中的序号:').strip())
                shopping_list.pop(n - 1)
                print(shopping_list)
                price = 0
                for i in shopping_list:
                    price += i[1]
                print('总价',price)
            print('可以购买\n', shopping_list)
            ensure = int(input('您是否直接结算？'
                           '1.结算'
                           '2.继续购物'))
            if ensure == 1:
                print('此次共消费：', price)
                print('账户余额：', account - price)
                break
            else:
                continue



        elif choice.upper() == 'Q':
            if len(shopping_list) > 0:
                print('已支付，您的购物清单如下:')
                print('商品', '  数量 ', ' 单价')
                price = 0
                for i in goods:
                    if i in shopping_list:
                        amount = shopping_list.count(i)
                        print(i[0], ' * ', amount, ' ,', i[1])  # 统计同类商品个数
                        s = i[1] * amount
                        price = price + s  # 计算总价
                print('此次共消费：', price)
                print('账户余额：', account - price)
                break
            else:
                print('您本次未购买商品')
                break


start()
