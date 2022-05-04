# api_yamdb
Проект YaMDb собирает отзывы пользователей на произведения

### Как запустить проект:

* Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/...
```
```
cd yatube_api
```

* Cоздать и активировать виртуальное окружение:

```
python -m venv venv
```
```
source venv/Script/activate
```
*
```
python -m pip install --upgrade pip
```

* Установить зависимости из файла requirements.txt:
```
pip install -r requirements.txt
```

* Выполнить миграции:
```
python manage.py migrate
```

* заполнить  тестовые данные:
```
python manage.py importcsv
```

*Запустить проект:
```
python manage.py runserver
```
