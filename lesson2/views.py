import os
from datetime import datetime

from framework.templates import render


def index_view(request):
    data = {'name_company': 'ООО',
            'products': ['1', '2', '3']}

    return '200 OK', render('index.html', **data)


def about_view(request):
    # Просто возвращаем текст
    return '200 OK', render('about.html')


def contact_view(request):
    # Проверка метода запроса
    if request.get('method') == 'POST':
        now = datetime.now()
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        print(f'Нам пришло сообщение от {email} с темой {title} и текстом {text}')
        path = os.path.dirname(os.path.abspath(__file__))
        with open(f'{path}/messages/message_{now.strftime("%d%m%Y")}_{now.strftime("%H.%M.%S")}.txt', 'w') as message_file:
            message_file.write(f'Нам пришло сообщение от {email} с темой \n {title} \n и текстом \n {text}')
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')


def not_found_404_view(request):
    print(request)
    return '404 WHAT', [b'404 not found!']
