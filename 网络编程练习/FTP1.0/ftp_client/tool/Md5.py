import hashlib

def get_md5(s):              #加密函数，将存储的密码变成密文
    a = hashlib.md5()
    a.update(bytes(s,encoding='utf-8'))
    a = (a.hexdigest())
    return a

