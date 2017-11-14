# local

from settings.base import *

DEBUG = True

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_todo', # DB명
        'USER': 'root', # 데이터베이스 계정
        'PASSWORD': '', # 계정 비밀번호 helloworld12;
        'HOST': '127.0.0.1', # 데이테베이스 주소(IP)
        'PORT': '3306', # 데이터베이스 포트(보통은 3306)
    }
}
