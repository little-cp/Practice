import socket
import struct
sock = socket.socket()
sock.connect(('127.0.0.1',8800))
first = sock.recv(1024)
print(first.decode('utf-8'))

while 1:

    cmd = input('>>>')
    sock.sendall(cmd.encode('utf-8'))
    if cmd == 'q':
        break
    if len(cmd) == 0:
        continue
    print('输入有误，请重输！')
    message = sock.recv(1024)
    print('收到:',message.decode('gbk'))
sock.close()