from getpass import getpass
from webclient import create_user

identifier 
user = input("User: ")
password = getpass(prompt="Your password: ")
response = create_user(user, password)
print(response.status_code)
