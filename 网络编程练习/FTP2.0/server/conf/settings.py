import os,sys
base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(base_path)

userinfo = os.path.join(base_path,'db','用户信息.txt')
