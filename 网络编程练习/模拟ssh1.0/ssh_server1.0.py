

import struct
import socket
import subprocess
sock = socket.socket()
sock.bind(('127.0.0.1',8800))
sock.listen(5)

while 1:
    print('server is working...')
    conn, addr = sock.accept()
    print('连接已建立')
    conn.sendall('欢迎'.center(10,'-').encode('utf-8'))
    while 1:
        try:
            message = conn.recv(1024)
            s = message.decode('utf-8')
            if s == 'q':
                print('对方断开连接')
                break
            print(s)
            a = subprocess.Popen(s, shell=True,
            stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            reaction = a.stdout.read()
            print('len',len(reaction))
            print(len(reaction))
            conn.sendall(reaction)
        except Exception as e:
            break
    conn.close()
