import login
import table_parse

if __name__ == '__main__':
    table_data = table_parse.parse_table(login.login())
    print(table_data)
