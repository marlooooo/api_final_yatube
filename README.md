# api_final
api final

## API v1 к проекту [yatube](https://github.com/marlooooo/hw05_final)


### Как запустить проект:

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/marlooooo/api_final_yatube.git
```

```
cd api_final_yatube
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

Выполнить миграции:

```
python3 manage.py migrate
```

Запустить проект:

```
python3 manage.py runserver
```

  
# Примеры запросов
Документация проекта доступна по [адресу](http://127.0.0.1:8000/redoc/) 

###Пример GET запроса:  
```
GET api/v1/groups/
```
```http://127.0.0.1:8000/api/v1/groups/```  
###Пример ответа:
```
[
    ...
    {
        "id": 0,
        "title": "string",
        "slug": "string",
        "description": "string"
    }
    ...
]
```