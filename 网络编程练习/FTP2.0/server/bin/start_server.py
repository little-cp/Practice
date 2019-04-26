import os
import sys
import socketserver
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from core import ftp_server
if __name__ == '__main__':

    sock = socketserver.ThreadingTCPServer(('127.0.0.1',8800),ftp_server.Myserver)
    print('server is working.....')
    sock.serve_forever()
