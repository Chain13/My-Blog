from .base import *
from dotenv import load_dotenv
load_dotenv()
#noqa
DEBUG = False
ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS", "localhost").split(",")
SECRET_KEY = os.getenv("SECRET_KEY")
DATABASES = {
    'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
}