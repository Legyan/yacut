# Yacut

Сервис укорачивания ссылок

### Описание:

Yacut ассоциирует длинную пользовательскую ссылку с короткой, которую предлагает сам пользователь или предоставляет сервис.
При переходе по короткой ссылке происходит переадресация на исходный адрес.

Доступ к сервису предоставляется как с помощью графического интерфейса веб страницы, так и через API.

На странице сервиса находится форма с двумя полями: обязательным для исходного адреса и необязательным для предлагаемой пользователем короткой ссылки (не более 16 символов). Если пользователь не предоставил свой вариант короткой ссылки, она генерируется автоматически из шести случайных символов.

API дублирует функции веб сервиса, примеры запросов к API, варианты ответов и ошибок приведены в спецификации openapi.yml.

### Стек технологий 

![](https://img.shields.io/badge/Python-3.10-black?style=flat&logo=python) 
![](https://img.shields.io/badge/Flask-2.0.2-black?style=flat&logo=flask)
![](https://img.shields.io/badge/SQLAlchemy-1.4.29-black?style=flat)

### Запуск проекта

1. Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/Legyan/yacut.git
```

```
cd yacut
```

2. Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Для Linux/macOS

    ```
    source venv/bin/activate
    ```

* Для Windows

    ```
    source venv/scripts/activate
    ```

3. Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

4. Создать в корневой директории файл .env и заполнить его данными:

```
nano .env
```

```
FLASK_APP=yacut
FLASK_ENV=production
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<YOUR_SECRET_KEY>
```

5. Создать базу данных SQLite:

```
flask shell
```

```python
from yacut import db
db.create_all()
exit()
```

6. Запустить Flask приложение:

```
flask run
```

### Примеры запросов к API

#### 1. Запрос: POST /api/id/

```
{
  "url": "https://www.google.com/search?q=flask+documentation&ei=SWAXZPD2KYWBi-gPp-SyYA&ved"
}
```

#### Ответ: HTTP/1.1 201 Created

```
{
   "url": "https://www.google.com/search?q=flask+documentation&ei=SWAXZPD2KYWBi-gPp-SyYA&ved",
   "short_link": "http://localhost:8000/AaBbCc"
}
```

#### 2. Запрос: POST /api/id/

```
{
  "url": "https://www.google.com/search?q=flask+tutorial&ei=aWAXZPz1G86QkwWJ8qv4BQ",
  "custom_id": "flasktutor"
}
```

#### Ответ: HTTP/1.1 201 Created

```
{
   "url": "https://www.google.com/search?q=flask+tutorial&ei=aWAXZPz1G86QkwWJ8qv4BQ",
   "short_link": "http://localhost:8000/flasktutor"
}
```

#### 3. Запрос: GET /api/id/flasktutor

#### Ответ: HTTP/1.1 201 Created

```
{
   "url": "https://www.google.com/search?q=flask+tutorial&ei=aWAXZPz1G86QkwWJ8qv4BQ"
}
```

#### 4. Запрос: GET /api/id/djangotutor

#### Ответ: HTTP/1.1 404 Not Found

```
{
   "message": "Указанный id не найден"
}
```
