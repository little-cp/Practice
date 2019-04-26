import socket
import json
import os,sys
import struct
import socketserver
import os
import sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)


class Ftp_Server:
    def __init__(self,ip_port):
        self.sock = socket.socket()
        self.address = ip_port

        try:
            self.server_bind()
            self.server_listen()
        except:
            self.server_close()
            raise
    def server_bind(self):
        self.sock.bind(self.address)
    def server_listen(self):
        self.sock.listen(5)
    def server_accept(self):
        return self.sock.accept()
    def server_close(self):
        self.sock.close()


    def run(self):
        while 1:
            print('server is working...')
            self.conn,self.addr = self.server_accept()
            print('from client',self.addr)
            while 1:
                try:
                    cmd = self.conn.recv(1024).decode()
                    print(cmd)
                    operation,filename = cmd.split('|')
                    getattr(self,operation)(filename)

                except Exception:
                    break


    def put(self,file):
        '''
        对应用户的上传
        :param file:
        :return:
        '''
        head_len = struct.unpack('i', self.conn.recv(4))[0]
        print(head_len)
        head_json = self.conn.recv(head_len)
        head = json.loads(head_json.decode('utf-8'))
        print(head)
        file_size = head['文件大小']
        file_name = head['文件名称']
        print(file_size)
        recv_data = b''
        file_path = os.path.join(base_path,'cloud',file_name)
        print(file_path)
        with open(file_path, 'wb') as f:
            has_recv_len = 0
            while has_recv_len < file_size:
                data = self.conn.recv(1024)
                recv_data += data
                has_recv_len += len(data)
                f.write(data)

    def get(self,file):
        '''
        对应用户的下载
        :param file:
        :return:
        '''
        status = True       #文件是否存在的状态标志
        file_path = os.path.join(base_path,'home',file)#拼出文件完整目录
        if not os.path.isfile(file_path):
            status = False
            filesize = 0
        else:
            filesize = os.path.getsize(file_path)
        print(status,111)
        head = {'文件存在状态':status,
                '文件名称': file,
                '文件大小': filesize}

        head_json = json.dumps(head)
        head_len = struct.pack('i', len(head_json))
        self.conn.sendall(head_len)
        self.conn.sendall(head_json.encode('utf-8'))
        if status:
            with open(file_path, 'rb') as f:
                for line in f:
                    self.conn.sendall(line)
        else:
            return

a = Ftp_Server(('127.0.0.1',8800))
a.run()

