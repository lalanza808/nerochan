from secrets import token_urlsafe
from datetime import timedelta
from os import getenv, getcwd

from dotenv import load_dotenv

load_dotenv()

# Site meta
SITE_NAME = getenv('SITE_NAME', 'nerochan')
SECRET_KEY = getenv('SECRET_KEY', token_urlsafe(12))
SERVER_NAME = getenv('SERVER_NAME', '127.0.0.1:5000')

# Services
XMR_WALLET_PASS = getenv('XMR_WALLET_PASS')
XMR_WALLET_RPC_USER = getenv('XMR_WALLET_RPC_USER')
XMR_WALLET_RPC_PASS = getenv('XMR_WALLET_RPC_PASS')
XMR_WALLET_RPC_PORT = getenv('XMR_WALLET_RPC_PORT', 8000)
XMR_WALLET_NETWORK = getenv('XMR_WALLET_NETWORK')
XMR_DAEMON_URI = getenv('XMR_DAEMON_URI')
XMR_DAEMON_HOST, XMR_DAEMON_PORT = XMR_DAEMON_URI.split('://')[1].split(':')
REDIS_HOST = getenv('REDIS_HOST', 'localhost')
REDIS_PORT = getenv('REDIS_PORT', 6379)
DATA_PATH = getenv('DATA_PATH', f'{getcwd()}/data')

# Sessions
SESSION_LENGTH = int(getenv('SESSION_LENGTH', 300))
PERMANENT_SESSION_LIFETIME = timedelta(minutes=SESSION_LENGTH)
MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50 MB

# Development
TEMPLATES_AUTO_RELOAD = True
