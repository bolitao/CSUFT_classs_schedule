from getpass import getpass

import ics
import login
import table_parse

if __name__ == '__main__':
    username = input("学号: ")
    # password = input("密码: ")
    password = getpass("密码: ")  # getpass() 仅用于非开发环境
    class_info = table_parse.parse_table(login.login(username, password))
    ics.info_to_ics(class_info, username)
