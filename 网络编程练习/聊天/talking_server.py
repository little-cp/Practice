import socket
#
# sock = socket.socket()
# sock.bind(('127.0.0.1',8800))
# sock.listen(5)
# conn , addr = sock.accept()
# print('连接已建立')
# conn.sendall('欢迎'.encode('utf-8'))
# data = conn.recv(1024)
# print('收到:',data.decode('utf-8'))
# conn.sendall('开始聊天吧'.encode('utf-8'))
# print('聊天开始'.center(20,'-'))
# while 1:
#     content = input('输入：')
#     conn.sendall(content.encode('utf-8'))
#     message = conn.recv(1024)
#     print('收到：',message.decode('utf-8'))

'''
可退出版
'''

import socket

sock = socket.socket()
sock.bind(('127.0.0.1',8800))
sock.listen(5)


while 1:
    print('server is working...')
    conn, addr = sock.accept()
    print('连接已建立')
    while 1:
        try:
            conn.sendall('欢迎'.encode('utf-8'))
            message = conn.recv(1024)
            if message.decode('utf-8') == 'q':
                print('对方断开连接')
                break
            print('收到了：', message.decode('utf-8'))
            response = input('输入：').encode('utf-8')
            conn.sendall(response)
            if response.decode('utf-8') == 'q':
                break
        except Exception as e:
            break
    conn.close()
