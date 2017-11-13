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