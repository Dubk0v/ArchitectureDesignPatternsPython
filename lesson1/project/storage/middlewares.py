# слои middleware

from datetime import date


def middleware_date(request):
    request['date'] = date.today()


def middle_css(request):
    with open('templates/css/style.css') as file:
        css_file = file.read()
        request['style'] = css_file


middlewares = [middleware_date, middle_css]