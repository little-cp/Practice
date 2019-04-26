import socketserver
import struct
import json, hashlib
import os, sys, time

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

from conf import settings
from core import auth


class Myserver(socketserver.BaseRequestHandler):
    status = {200: "登录成功",
              201: '用户名或密码错误',
              300: '文件存在',
              301: '文件不存在'
              }

    def recv_data(self):
        info_json_size = struct.unpack('i', self.request.recv(4))[0]
        info_json = self.request.recv((info_json_size))
        info = json.loads(info_json)
        return info

    def send_data(self, data):
        info_json = json.dumps(data).encode()
        info_json_size = struct.pack('i', len(info_json))
        self.request.sendall(info_json_size)
        self.request.sendall(info_json)

    def _mkdir(self, data):
        '''
        创建文件夹 服务端
        :param data:
        :return:
        '''

        abs_path = os.path.join(base_path, 'home', data['user'], data['choice'][-1])
        # print('abs_path',abs_path)
        isExists = os.path.exists(abs_path)  # 判断结果
        if not isExists:
            os.makedirs(abs_path)  # 如果不存在则创建目录
            return True
        else:  # 如果目录存在则不创建
            return False

    def _put(self, data):
        '''
        上传 服务端
        :param data:
        :return:
        '''

        file_path = os.path.join(data['user_path'], data['file'])
        file_size = data['file_size']
        md = hashlib.md5()
        with open(file_path, 'wb') as f:
            recv_data = b''
            has_recv_len = 0
            print('正在上传')
            while has_recv_len < file_size:
                file_data = self.request.recv(4096)
                time.sleep(0.02)
                num = int(has_recv_len / file_size * 10)
                print('\r %s>%s' % ('-' * num, has_recv_len / file_size * 100), end='')
                recv_data += file_data
                has_recv_len += len(file_data)
                md.update(file_data)
                f.write(file_data)
            print('\r %s>%.2f%%' % ('-' * 2 * num, float(has_recv_len / file_size * 100)))
            print('上传完成')
        hash_value = md.hexdigest()

        check_msg = {}
        check_msg['hash'] = hash_value
        self.send_data(check_msg)

    def _get(self, data):
        '''下载 服务端'''
        file_path = os.path.join(base_path, 'cloud', data['file'])  # 拼出文件完整目录
        if not os.path.isfile(file_path):  # 先判断要下载的文件是否存在
            data['file_status'] = False
            data['filesize'] = 0
        else:
            data['file_status'] = True
            data['filesize'] = os.path.getsize(file_path)
        self.send_data(data)
        md = hashlib.md5()
        if data['file_status']:
            with open(file_path, 'rb') as f:
                for line in f:
                    self.request.sendall(line)
                    md.update(line)  # 发送同时加密
            hash_value = md.hexdigest()  # 得到服务端文件hash值
            check_responce = self.recv_data()
            if check_responce['hash'] == hash_value:  # 判断客户端文件hash是否相等
                check_responce['check_file'] = True
            else:
                check_responce['check_file'] = False
            self.send_data(check_responce)
        else:
            return

    def handle(self):

        log_info = self.recv_data()
        auth.login(self, log_info)  # 调用登录函数
        while 1:
            cmd_data = self.recv_data()  # 进入交互
            if hasattr(self, '_%s' % cmd_data['action_type']):
                getattr(self, '_%s' % cmd_data['action_type'])(cmd_data)
