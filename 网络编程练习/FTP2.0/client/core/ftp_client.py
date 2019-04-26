import getpass
import time
import socket
import json
import os, sys
import hashlib
import struct

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)


class Client(object):
    def __init__(self):
        #     '''
        #     负责初始化操作，
        #     :param ip_port:
        #     '''
        self.sock = socket.socket()
        ip_port = ('127.0.0.1', 8800)
        self.address = ip_port

    def client_connect(self):
        self.sock.connect(self.address)

    def client_close(self):
        self.sock.close()

    def recv_data(self):
        '''
        与服务器交互，接收数据
        :return:
        '''
        info_json_size = struct.unpack('i', self.sock.recv(4))[0]
        info_json = self.sock.recv((info_json_size))
        info = json.loads(info_json)
        return info

    def send_data(self, data):
        '''
        与服务器交互，发送数据
        :param data:
        :return:
        '''
        info_json = json.dumps(data).encode()
        info_json_size = struct.pack('i', len(info_json))
        self.sock.sendall(info_json_size)
        self.sock.sendall(info_json)

    def create_localfolder(self, user):
        '''
        登录成功之后，自动在db创建一个与用户名同名的文件夹
        下载的文件存储在这个里面
        :param user:
        :return:
        '''
        path = os.path.join(base_path, 'db', user)
        isExists = os.path.exists(path)  # 判断路径是否存在
        if not isExists:  # 如果不存在则创建目录
            os.makedirs(path)
            return True
        else:
            print('目录已存在')  # 如果目录存在则不创建，并提示目录已存在
            return False

    def progress_bar(self, has_recv, file_size):
        '''
        进度条
        :param has_recv:
        :param file_size:
        :return:
        '''
        num = int(has_recv / file_size * 100)
        bar = '\r%s>%s%%\n' % ('=' * num, num) if num == 100 else '\r%s>%s%%' % ('=' * num, num)
        print(bar, end='')

    def _mkdir(self, data):
        '''
        与服务器交互，新建文件夹
        :param data:
        :return:
        '''

        mk_data = {
            'action_type': data['choice'][0],
            'choice': data['choice'],
            'user_path': data['user_path'],
            'user': data['user'],
        }
        self.send_data(mk_data)

    def _put(self, data):
        '''
        上传 客户端
        :param data:
        :return:
        '''
        file_path = os.path.join(base_path, 'db', data['choice'][1])
        if not os.path.isfile(file_path):
            print('文件:%s 不存在' % file_path)
            return
        else:
            filesize = os.path.getsize(file_path)
        put_data = {
            'action_type': data['choice'][0],
            'file': data['choice'][1],
            'file_size': filesize,
            'choice': data['choice'],
            'user_path': data['user_path'],
            'user': data['user'],
        }
        self.send_data(put_data)
        print('开始上传')
        md = hashlib.md5()
        with open(file_path, 'rb') as f:
            for line in f:
                self.sock.sendall(line)
                md.update(line)
            print('上传成功')
            hash_value = md.hexdigest()
        check_responce = self.recv_data()
        if check_responce['hash'] == hash_value:
            print('文件一致')
        else:
            print('文件不一致')

    def _get(self, data):
        '''
        下载 客户端
        :param data:
        :return:
        '''
        get_data = {
            'action_type': data['choice'][0],
            'choice': data['choice'],
            'file': data['choice'][1],
            'user_path': data['user_path'],
            'user': data['user'],
        }
        self.send_data(get_data)
        ret_data = self.recv_data()
        if ret_data['file_status']:
            print('开始下载')
            recv_data = b''
            file_size = ret_data['filesize']
            md = hashlib.md5()
            with open(os.path.join(base_path, 'db', ret_data['user'], ret_data['file']), 'wb') as f:
                has_recv_len = 0
                while has_recv_len < file_size:
                    file_data = self.sock.recv(1024)
                    recv_data += file_data
                    time.sleep(0.02)
                    self.progress_bar(has_recv_len, file_size)
                    # 调用进度条函数
                    has_recv_len += len(file_data)
                    md.update(file_data)
                    f.write(file_data)
                self.progress_bar(has_recv_len, file_size)
                # 再次调用进度条函数
                print('下载完成')
                hash_value = md.hexdigest()
                check_msg = {}
                check_msg['hash'] = hash_value
                self.send_data(check_msg)
                check_response = self.recv_data()
                if check_response['check_file']:
                    print('文件一致')
                else:
                    print('文件不一致')
        else:
            print('文件不存在')

    def run(self, data):
        '''
        与服务器交互
        :param data:
        :return:
        '''
        while 1:
            user_dir = (data['user_path'].replace(data['user_dir'], ''))
            choice = input('[%s@%s#]' % (data['user'], user_dir)).strip().split()
            data['choice'] = choice
            if hasattr(self, '_%s' % choice[0]):
                getattr(self, '_%s' % choice[0])(data)
            else:
                print('command not found')

    def initialize(self):
        '''初始化后的操作'''
        self.client_connect()
        while 1:
            user, pwd = input('login:').strip(), input('password:')
            # user,pwd = 'c','c'
            if not user: continue
            log_info = {
                'action_type': 'login',
                'user': user,
                'password': pwd,
            }
            self.send_data(log_info)
            ret = self.recv_data()

            if ret.get('status_code') == 201:
                print(ret.get('status'))

            else:
                self.create_localfolder(user)
                self.run(ret)
