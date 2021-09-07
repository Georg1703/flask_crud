**Для запуска проекта у вас должен быть установлен:**

    1. Python 3.7<
    2. PostgreSQL

**После скачивания репозитория нужно:**

    1. Создать и запустить venv
    2. Установить зависимости из requirements.txt (Не забываем обновить pip)
    3. Создать файл flask_crud_app/instance/config.py c переменными
        SECRET_KEY='', 
        SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://db_user:db_password@db_host/db_name'
    4. Задать значение для двух констант 
        FLASK_CONFG=development, 
        FLASK_APP=run.py
    4. Запустить команду  `flask db upgrade` для синхронизации с бд
    5. Запустить приложение командой: `flask run`
    6. Перейти в браузере по url localhost:5000
    7. Использовать данные - email=admin@admin.com, pass=admin, для авторизации

**Чтобы просмотреть результаты решения второй задачи нужно переходить по  url 'http://localhost:5000/asynchronous'. Сравнить с результатом решения той же задачи только в синхронном режиме можно по url 'http://localhost:5000/synchronous'.**