from datetime import date
from storage.views import Index, About, Contacts, PageNotExists

routes = {
    '/': Index(),
    '/about/': About(),
    '/contacts/': Contacts(),
    '/404/': PageNotExists(),
}
