import os
import sys

base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)
from core import ftp_client

if __name__ == '__main__':
    ftp_client.Client().initialize()
