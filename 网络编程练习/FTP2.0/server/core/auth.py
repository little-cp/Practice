import os,sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from conf import settings
def login(self, data):
    '''
    登录认证函数
    :param self:
    :param data:
    :return:
    '''

    with open(settings.userinfo) as f:
        status_info = {}
        for i in f:
            user = i.strip().split('|')[0]
            pwd = i.strip().split('|')[1]
            if user == data['user'] and pwd == data['password']:
                status_info['status_code'] = 200
                status_info['user'] = data['user']
                status_info['status'] = self.status[200]
                status_info['user_dir'] = os.path.join(base_path, 'home')
                status_info['user_path'] = os.path.join(base_path, 'home', data['user'])
                print('有客户端连入')
                self.send_data(status_info)
                break
        else:
            status_info['status_code'] = 201
            status_info['status'] = self.status[201]
            self.send_data(status_info)



