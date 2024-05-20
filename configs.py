import os
from dotenv import load_dotenv

load_dotenv()

LDAP_SERVER = os.getenv('LDAP_SERVER')
LDAP_BASE_DN = os.getenv('LDAP_BASE_DN')
LDAP_USER_DN = os.getenv('LDAP_USER_DN')
LDAP_USER_PASSWORD = os.getenv('LDAP_USER_PASSWORD')
SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')
SERVER_TOKEN = os.getenv('SERVER_TOKEN')
