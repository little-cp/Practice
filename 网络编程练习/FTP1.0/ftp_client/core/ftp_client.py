import socket
import json
import struct
import sys
import os

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

from core import auth
from tool import mkdir


class Ftp_client:
    ret = auth.login()

    def __init__(self, ip_port):
        '''
        负责初始化操作，
        :param ip_port:
        '''
        self.sock = socket.socket()
        self.address = ip_port
        # 登录
        if Ftp_client.ret:
            folder_path = os.path.join(base_path, Ftp_client.ret['name'])
            mkdir.mkdir(folder_path)  # 登录成功创建一个属于该用户的文件夹
            try:
                self.client_connect()
            except:
                self.client_close()
                raise

    def client_connect(self):
        self.sock.connect(self.address)

    def client_close(self):
        self.sock.close()

    def run(self):
        '''
        登陆成功后,执行客户端操作
        :return:
        '''
        while 1:
            cmd = input('请输入：(格式：操作|文件)\n').strip()
            if not cmd:
                continue
            try:
                operation, filename = cmd.split('|')
            except ValueError:
                print('未按照格式输入')
                continue
            if hasattr(self, operation):
                self.sock.sendall(cmd.encode('utf-8'))
                getattr(self, operation)(filename)
            else:
                print('没有此操作')

    def put(self, file):
        '''
        上传文件
        :param file:
        :return:
        '''
        file_path = os.path.join(base_path, 'db', file)
        if not os.path.isfile(file_path):
            print('文件:%s 不存在' % file_path)
            return
        else:
            filesize = os.path.getsize(file_path)

        head = {'文件名称': file,
                '文件大小': filesize}
        head_json = json.dumps(head)
        head_len = struct.pack('i', len(head_json))
        self.sock.sendall(head_len)
        self.sock.sendall(head_json.encode('utf-8'))
        with open(file_path, 'rb') as f:
            for line in f:
                self.sock.sendall(line)
            print('上传完成')

    def get(self, file):
        '''
        下载文件
        :param file:
        :return:
        '''
        head_len = struct.unpack('i', self.sock.recv(4))[0]
        head_json = self.sock.recv(head_len)
        head = json.loads(head_json.decode('utf-8'))
        file_size = head['文件大小']
        file_name = head['文件名称']
        if head['文件存在状态']:  #
            print('开始下载')
            recv_data = b''
            with open(os.path.join(base_path, Ftp_client.ret['name'], file_name), 'wb') as f:
                has_recv_len = 0
                while has_recv_len < file_size:
                    data = self.sock.recv(1024)
                    recv_data += data
                    has_recv_len += len(data)
                    f.write(data)
            print('下载完成')
        else:
            print('您要下载的文件不存在！')


a = Ftp_client(('127.0.0.1', 8800))
a.run()
