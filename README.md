# bmstu-food
## Запуск приложения в режиме отладки
Для запуска приложения в системе необходимо установить Docker.
Команда для запуска выглядит следующим образом:
`docker compose up`
После первого запуска рекомендуется создать суперпользователя. Сделать это можно выполнив следующую последовательность команд:
Подключение к консоли контейнера для выполнения команд внутри среды развернутого приложения: 
`docker exec -it bmstu-food-django-1`
Создание суперпользователя:
`python manage.py createsuperuser`
Далее выполняется стандартная процедура создания суперпользователя Django

##Запуск приложения в продакшн
Необходимо создать файлы окружения .env.prod и .env.email в корневой директории репозитория.
Пример содержания файла .env.prod:
```
DEBUG=1
DB_USER: user
DB_PASSWORD: password
DB_NAME: bmstu-food
DB_HOST: postgres
DB_PORT: '5432'
PGADMIN_DEFAULT_EMAIL: admin@admin.com
PGADMIN_DEFAULT_PASSWORD: password
POSTGRES_USER: user
POSTGRES_PASSWORD: password
POSTGRES_DB: bmstu-food
```
Измените значения DB_USER, DB_PASSWORD, PGADMIN_DEFAULT_EMAIL, PGADMIN_DEFAULT_PASSWORD, POSTGRES_USER, POSTGRES_PASSWORD под свои нужды

Пример содержания файла .env.email:
```
EMAIL_HOST_USER: bmstufood@gmail.com
EMAIL_HOST_PASSWORD: 'abcd efgh ijkl mnop'
```
Измените значения EMAIL_HOST_USER, EMAIL_HOST_PASSWORD значениями свой почты, с которой будет осуществляться рассылка сообщения и API ключом почты