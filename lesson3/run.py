#  импорты из стандартной библиотеки
from datetime import datetime

# импорты сторонних библиотек
from wsgiref.simple_server import make_server

# импорты модулей текущего проекта
from urls import routes, fronts
from framework import Application

application = Application(routes, fronts)

with make_server('', 8080, application) as httpd:
    print(f"Запуск на порту 8080 - {datetime.now()}...")
    print("http://127.0.0.1:8080/")
    httpd.serve_forever()
