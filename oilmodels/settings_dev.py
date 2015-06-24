from settings import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'openoil_dev',
        'USER': 'openoil',
        'PASSWORD': DB_PASS,
        'HOST': 'localhost',
    }
}
