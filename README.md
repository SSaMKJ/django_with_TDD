# 파이썬을 이용한 클린 코드를 위한 테스트 주도 개발
    책을 보며 django를 익히는 중.

- 모델 생성 후 makemigration 을 통해서 DB의 테이블을 만든다.
    - python3 manage.py makemigration
    - python3 manage.py migrate --run-syncdb
    
- sqlite3 초기화
    - rm db.mysqlite3
    - python3 manage.py migrate --noinput
    
- static 파일 모으기
    - settings.py 에 아래 코드 추가
```python
settings.py

STATIC_URL = '/static/'
STATIC_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'static'))
```
- 그런 뒤에 terminal 에서 아래 코드 실행
```bash
$> python3 manage.py collectstatic
```    

# app 추가하기
```bash
django-admin startapp myapp
```

# virtualenv 만드는 방법
- 일단 없으면 설치.
```bash
pip3 install virtualenv
```    

- 서버와 같은 폴더 구조를 사용하도록 한다.
```bash
$ virtualenv --python=python3 ../virtualenv # 경로를 잘 잡아 줘야 한다.
$ ls
bin include lib
```

- 하나의 독립된 "가상 파이썬 환경"이라고 할 수 있다. 이 환경을 실행하려면 activate라는 스크립트를 실행하면 된다.

```bash
$ which python3
/usr/bin/python3
$ source ../virtualenv/bin/activate
$ which python # virtualenv 의 파이썬 경로로 변경된 것을 확인.
/workspace/virtualenv/bin/python
(virtualenv)$ python3 manage.py test lists
[...]
```
- 하나의 독립된 가상 파이썬 환경이 잘 등록되었다.
- 필요한 패키지를 추가 할 수 있다.
```bash
(virtualenv)$ pip install django==1.11
[...] 
```
- 내보내기.
```bash
(virtualenv)$ pip freeze > requirements.txt
(virtualenv)$ deactivate # 나갈 때 사용하는 명령어
$ cat requirements.txt
Django==1.11
$ git add requirements.txt
$ git commit -m "requirements.txt를 virtualenv에 추가"
$ git push
```
- 모든 곳에서 동일한 환경의 파이썬 환경을 가질 수 있다.

# MySQL 설정

- 설치
```bash
$ pip install pymysql
- pythonanywhere 에서는 --user 옵션을 붙여줘야 한다.
$ pip install --user pymysql
```

- 설정 추가
```python
settings.py
import pymysql

pymysql.install_as_MySQLdb()
```

- db 설정 변경
   - 기본적으로 아래와 같다.
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```
- 이렇게 변경한다.
```python
settings.py

import pymysql

pymysql.install_as_MySQLdb()

...


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'django_locker', # DB명
        'USER': '', # 데이터베이스 계정
        'PASSWORD': '', # 계정 비밀번호
        'HOST': '', # 데이테베이스 주소(IP)
        'PORT': '', # 데이터베이스 포트(보통은 3306)
    }
}
```

- 그 뒤에 마이그레이션 해 준다.
```bash
$ python manage.py makemigrations
$ python manage.py migrate
```

- pythonanywhere
   - MySQL DB를 띄웠다.
   - db도 만들었다. 이름을 넣으면 내 id$이름 식으로 자동으로 만들어진다.
   - 비밀번호도 입력하였다.
   - settings 폴더를 분리하였다.
   - stage.py 파일을 만들고 github 에는 추가하지 않았다.
   - 사이트에서 경로에 맞게끔 파일을 업로드 하였다.
   - /var/www/jonathan7324_pythonanywhere_com_wsgi.py 파일을 수정하여 setting을 변경해 주었다.
   - 서버 리스타트.
   - MySQL로 변경하는 작업을 성공하였다.
   
- MySQL로 변경한 뒤 테스트
   - 이상하게 MySQL로는 테스트가 안되었다.
   - db.sqlite3를 테스트 db로 사용하였다.
   
- 한글 깨짐 문제.
   - 테이블을 만들 때 아래와 같이 해 준다.
   
```mysql
CREATE DATABASE django_todo CHARACTER SET utf8 COLLATE utf8_general_ci;
```