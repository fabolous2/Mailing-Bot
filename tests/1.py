import re

password_pattern = r'^[a-zA-Z0-9_.+-] + $'
pwd = input('Pwd: ')
print(re.match(password_pattern, pwd))