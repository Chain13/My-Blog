from .base import *
#noqa
DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]
SECRET_KEY = os.getenv("SECRET_KEY")
# Development-specific apps and middlewares
INSTALLED_APPS += [
	"debug_toolbar",
]
MIDDLEWARE += [
	"debug_toolbar.middleware.DebugToolbarMiddleware",
]
# Email backend for development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend:"