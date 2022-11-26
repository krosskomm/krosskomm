
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--=bv_qdf&8__(y1eiv*!mgj0f__sz%ezkfx7%-cxxy$rkr@&$0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'krossk',
        'USER':'postgres',
        'PASSWORD':'solaris88MA',
        'HOST':'127.0.0.1',
        'PORT':'5432',
    }
}