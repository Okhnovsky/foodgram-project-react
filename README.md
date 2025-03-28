# Foodgram

**Foodgram** - веб-приложение, являющееся продуктовым помощником с множеством рецептов приготовления  различных блюд. В Foodgram можно создавать собственные рецепты и делиться ими с другими людьми. Также можно подписываться на других пользователей и сохранять понравившиеся рецепты в избранное. Для удобства предусмотрена возможность скачивания списка необходимых продуктов для приготовления выбранных произведений кулинарного искусства.


## Действующий ip адрес:
158.160.58.167



## Процесс развертывания проекта:
Клонируйте репозиторий.
```
git clone <репозиторий>
```
Установите и активируйте виртуальное окружение.
```
python -m venv venv
source venv\Scripts\activate
```
Установите зависимости:
```
cd ../backend
pip install -r requirements.txt
```
Создать файл .env и заполнить его:
```
DB_ENGINE='django.db.backends.postgresql' # указываем, что работаем с postgresql
DB_NAME='postgres' # имя базы данных
POSTGRES_USER='postgres' # логин для подключения к базе данных
POSTGRES_PASSWORD='postgres' # пароль для подключения к БД (установите свой)
DB_HOST='127.0.0.1' # название сервиса (контейнера)
DB_PORT='5432' # порт для подключения к БД
```

## Запуск проекта на удаленном сервере:
Скорректировать и переместить на сервер конфигурационные файлы `docker-compose.yml` и `nginx.conf` из каталога `infra/`
Запустите docker compose:
```
sudo docker-compose up
```
Создайте миграции в контейнере приложения `backend`
```
sudo docker-compose exec -it backend python manage.py makemigrations users
sudo docker-compose exec -it backend python manage.py migrate
sudo docker-compose exec -it backend python manage.py makemigrations recipes
sudo docker-compose exec -it backend python manage.py migrate
```
Cоздайте суперпользователя
```
sudo docker-compose exec backend python manage.py createsuperuser
```
и импортируйте ингредиенты: 
```
sudo docker-compose exec backend python manage.py load_ingridients
```
Соберите статику:
```
sudo docker-compose exec backend python manage.py collectstatic
```


## Эндпоинты:
Описание всех запросов можно найти в документации API сервиса
в директории infra
```
cd infra
```
выполните команду 
```
docker-compose up
```
По адресу http://localhost/api/docs/ будет доступна документация проекта.

## Технологии:
- Python 3.9
- Django 2.2.19
- Django REST framework 3.12.4
- PostgreSQL 15.0

**Авторы**:  
[Александр Охновский](https://github.com/Okhnovsky)
