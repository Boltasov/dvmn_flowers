# Версия для разработки

Нужен python версии 3.x (у меня 3.10).

## Комментарий
Сейчас продублировал папки `imgs` и `css` в:
1) `shop/templates` 
и
2) `shop/media`, `shop/static` соответственно. 

Первый вариант был изначально. С ним удобно запускаются в браузере html-файлы. Второй вариант предлагаю использовать для разработки, т.к. это, вроде, стандарт отрасли. 

## Шаги по запуску
Скачать репозиторий
```commandline
git clone ссылка-на-этот-репозиторий
```

Войти в папку проекта, если ещё не в ней:
```commandline
cd dvmn_flowers
```

Установить зависимости:
```commandline
pip install -r requirements.txt
```

Применить миграции, чтобы создать БД:
```commandline
python manage.py migrate
```

Создать себе пользователя:
```commandline
python manage.py createsuperuser
```

Запуск
```commandline
python manage.py runserver
```

По умолчанию админка должна быть доступна по адресу http://127.0.0.1:8000/admin/
