Для запуска проекта необходимо:

1. Установить зависимости:
   pip install -r requirements.txt

2. Создать в корневой директории проекта файл .env, добавить в него переменную SECRET_KEY.
   Далее нужо сгенерировать ключ для проекта, и установить значение переменной.

3. Првести миграции: python manage.py migrate

4. Добавить данные в базу:
   python manage.py loaddata discount_fixtures.json
   python manage.py loaddata group_fixtures.json
   python manage.py loaddata product_fixtures.json
   python manage.py loaddata user_fixtures.json

5. Запустить преокт командой:
   python manage.py runserver

6. Активировать "систему начисления скидок":
   celery -A store_project.celery_app worker -B --loglevel=info

7. Далее эндпоинты системы можно тестировать воспользовавшись коллекцией Postman.

8. Автоматизированые тесты к проекту можно запустить командой:
   python manage.py test
