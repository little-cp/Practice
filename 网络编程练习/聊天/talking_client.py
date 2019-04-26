import socket

sock = socket.socket()
sock.connect(('127.0.0.1',8800))

while 1:
    first = sock.recv(1024)
    print(first.decode('utf-8'))
    cont = input('输入：')
    sock.sendall(cont.encode('utf-8'))
    if cont == 'q':
        break
    message = sock.recv(1024)
    if message.decode('utf-8') == 'q':
        print('对方断开')
        break
    print('收到:',message.decode('utf-8'))
sock.close()