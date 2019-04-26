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
    header = sock.recv(4)
    data_len = struct.unpack('i',header)[0]
    if not data_len:
        print('输入命令有误，请重输！')
        continue
    print('数据长度：',data_len)
    recv_data = b''
    has_recv_len = 0
    while has_recv_len < data_len:
        message = sock.recv(1024)
        recv_data += message
        has_recv_len += len(message)
    print('收到:',recv_data.decode('gbk'))
sock.close()