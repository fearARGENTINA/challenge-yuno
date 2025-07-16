import os
from enum import Enum, auto
from urllib.parse import urljoin

OAUTH2_NAME = os.environ.get('OAUTH2_NAME')
CLIENT_ID = os.environ.get('CLIENT_ID') 
CLIENT_SECRET = os.environ.get('CLIENT_SECRET') 
ACCESS_TOKEN_URL = os.environ.get('ACCESS_TOKEN_URL') 
AUTHORIZE_URL = os.environ.get('AUTHORIZE_URL') 
API_BASE_URL = os.environ.get('API_BASE_URL')
USERINFO_URL = os.environ.get('USERINFO_URL') 
CLIENT_SCOPE = os.environ.get('CLIENT_SCOPE')
REDIRECT_URI = urljoin(os.environ.get('SITE_URL'), os.environ.get('OAUTH_REDIRECT_PATH'))
FILEBEAT_HOST = os.environ.get('FILEBEAT_HOST')
FILEBEAT_PORT = int(os.environ.get('FILEBEAT_PORT'))

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT'))
POSTGRES_DB = os.environ.get('POSTGRES_DB')
POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

SQLALCHEMY_DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

JWT_SECRET = os.environ.get('JWT_SECRET')
JWT_DURATION = int(os.environ.get('JWT_DURATION'))

class Role(Enum):
    ADMIN = auto()
    USER = auto()
    GUEST = auto()

DEFAULT_ROLE = Role.GUEST
DEFAULT_ADMIN_EMAIL = os.environ.get('DEFAULT_ADMIN_EMAIL')