import requests
from bs4 import BeautifulSoup
from getpass import getpass
import encrypt

login_page_url = "http://authserver.csuft.edu.cn/authserver/login?service=http%3A%2F%2Fjwgl.csuft.edu.cn%2F"
login_post_url = "http://authserver.csuft.edu.cn/authserver/login?service=http%3A%2F%2Fjwgl.csuft.edu.cn%2F"
table_page = "http://jwgl.csuft.edu.cn/jsxsd/xskb/xskb_list.do"


def login():
    username = input("学号：")
    # password = getpass("密码: ")
    password = input("密码: ")  # 开发环境不要用 getpass()
    _session = requests.session()
    response = _session.get(login_page_url)
    content = BeautifulSoup(response.text, "lxml")
    # 截取第二个 script 标签
    script = str(content.select('script')[1])
    script = script.replace(" ", "")
    script = script.replace("\n", "")
    salt = script.split("=")[3][1:1 + 16]  # TODO: 比较死板的取 pwdDefaultEncryptSalt 方法，待完善
    encrypted_password = encrypt.password_encrypt(salt, password)
    form_content = content.form.find_all("input")
    for input_tag in form_content:  # 表单中其他字段
        if input_tag.has_attr("name"):
            if input_tag["name"] == "lt":
                lt = input_tag["value"]
            elif input_tag["name"] == "dllt":
                dllt = input_tag["value"]
            elif input_tag["name"] == "execution":
                execution = input_tag["value"]
            elif input_tag["name"] == "_eventId":
                _eventID = input_tag["value"]
            elif input_tag["name"] == "rmShown":
                rm_shown = input_tag["value"]
    form_data = {
        "username": username,
        "password": encrypted_password,
        "lt": lt,
        "dllt": dllt,
        "execution": execution,
        "_eventId": _eventID,
        "rmShown": rm_shown
    }
    login_response = _session.post(login_post_url, data=form_data)
    return _session
