# Групповой проект API "YaMDb"
### Описание проекта:

**Проект YaMDb собирает отзывы пользователей на произведения (например: книги, музыка, фильмы), дает возможность комментировать чужие отзывы, а также позволяет ставить произведениям оценку и формировать тем самым ретинги произведений.**


## Используемые технологии и библиотеки:
>Python 3.9

>Django 3.2

>djangorestframework 3.12.4

>PyJWT 2.1.0

>django-filter 23.1

## Как запустить проект:
#### Клонировать репозиторий и перейти в него в командной строке:
>git clone https://github.com/mr-shifty/api_yamdb.git

#### Создать и активировать виртуальное окружение, установить зависимости:
>python -m venv venv

>source venv/Scripts/activate

>python -m pip install --upgrade pip

>pip install -r requirements.txt

#### Выполнить миграции:
>python manage.py migrate

#### Запустить проект:
>python manage.py runserver

##### В проекте доступны следующие эндпоинты:
* http://127.0.0.1:8000/api/v1/auth/signup/ - Получение кода подверждения на email


* http://127.0.0.1:8000/api/v1/auth/token/ - Получение токена для авторизации


* http://127.0.0.1:8000/api/v1/categories/ - Работа с категориями, доступны запросы Get, Post и Del

* http://127.0.0.1:8000/api/v1/genres/ - Работа с жанрами, доступны запросы Get, Post и Del

* http://127.0.0.1:8000/api/v1/titles/ - Работа со произведениями, доступны запросы Get, Post, Patch и Del

* http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/ - Работа с отзывами , доступны запросы Get, Post, Patch и Del

* http://127.0.0.1:8000/api/v1/titles/{title_id}/reviews/{review_id}/comments/ - Работа с комментариями , доступны запросы Get, Post, Patch и Del

* http://127.0.0.1:8000/api/v1/users/ - Создание пользователя и получение информации о всех пользователях. Доступны запросы Get, Post

* http://127.0.0.1:8000/api/v1/users/{username}/ - Получение информации о конкретном пользователе и редактирование информации о нем. Доступны доступны запросы Get, Postm Del

* http://127.0.0.1:8000/api/v1/users/me/ - Получение и изменение своих данных, доступны запросы Get, Patch

#### Работа выполнялась в команде.
##### Авторы:
**Павел Мельников** | **Эдуард Насыров** | **Валерия Лаврикова**