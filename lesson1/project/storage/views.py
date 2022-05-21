from framework.templator import render


class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', style=request.get('style', None))


class About:
    def __call__(self, request):
        return '200 OK', render('about.html', style=request.get('style', None))


class Contacts:
    def __call__(self, request):
        return '200 OK', render('contacts.html', style=request.get('style', None))


class PageNotExists:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'
