## Установка
1. Клонировать репозиторий:

`git clone https://github.com/e-chrome/pd_diploma.git`

2. Создать .env файл:

```
# Django
SECRET_KEY='the!most!secret!key'
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Postgres
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=diplom
POSTGRES_HOST=pgdb
POSTGRES_PORT=5432

# Redis
REDIS_BROKER_DB=1
REDIS_BACKEND_DB=2
REDIS_HOST=redis
REDIS_PORT=6379

# Email
EMAIL_HOST=
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
EMAIL_PORT=
```

3. Запустить контейнер:

 `docker-compose up -d --build`

**Приложение доступно по адресу:**

http://127.0.0.1:8000/
