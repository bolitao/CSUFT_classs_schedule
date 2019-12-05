import base64
from Crypto.Cipher import AES
import random

aes_chars = "ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678"


def random_str(length):
    ret = ""
    for i in range(length):
        ret += random.choice(aes_chars)
    return ret


def pad(password):  # 把密码补充成符合 AES-128 CBC 规范形式
    password = random_str(64) + password
    password_length = len(password)
    add_count = AES.block_size - password_length % AES.block_size
    if add_count == 0:
        add_count = AES.block_size
    _pad = chr(add_count)
    return password + _pad * add_count


def password_encrypt(aes_key, user_password):
    iv = random_str(16)
    user_password = pad(user_password).encode("utf8")
    # if len(user_password) % AES.block_size != 0:
    #     user_password = user_password + iv[0:AES.block_size - len(user_password) % AES.block_size]
    # encrypted_content = random_str(64) + user_password
    aes_key = str(aes_key.strip())
    cipher = AES.new(aes_key.encode("utf8"), AES.MODE_CBC, iv.encode("utf8"))
    return base64.b64encode(cipher.encrypt(user_password))
