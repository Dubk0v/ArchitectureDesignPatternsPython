from wsgiref.simple_server import make_server

from framework.core import Framework
from urls import routes, fronts


application = Framework(routes, fronts)

with make_server('', 8080, application) as httpd:
    print("http://127.0.0.1:8080/")
    httpd.serve_forever()
