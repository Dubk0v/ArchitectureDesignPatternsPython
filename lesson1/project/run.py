from wsgiref.simple_server import make_server

from framework.main import Framework
from storage.urls import routes
from storage.middlewares import middlewares

application = Framework(routes, middlewares)

with make_server('', 8080, application) as httpd:
    print("Запуск через порт 8080...(http://127.0.0.1:8080/)")
    httpd.serve_forever()
