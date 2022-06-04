from datetime import date

from framework.templates import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import FrameRoute, FrameDebug

site = Engine()
logger = Logger('main')
routes = {}


# контроллер - главная страница
@FrameRoute(routes=routes, url='/')
class Index:
    @FrameDebug(name='Index')
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


# контроллер "О проекте"
@FrameRoute(routes=routes, url='/about/')
class About:
    @FrameDebug(name='About')
    def __call__(self, request):
        return '200 OK', render('about.html')


# контроллер - Расписания
@FrameRoute(routes=routes, url='/study-programs/')
class StudyPrograms:
    @FrameDebug(name='StudyPrograms')
    def __call__(self, request):
        return '200 OK', render('study-programs.html', data=date.today())


# контроллер 404
class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


# контроллер - список курсов
@FrameRoute(routes=routes, url='/course_list/')
class CoursesList:
    @FrameDebug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No courses have been added yet'


# контроллер - создать курс
@FrameRoute(routes=routes, url='/course-add/')
class CreateCourse:
    category_id = -1

    @FrameDebug(name='CreateCourse')
    def __call__(self, request):
        if request['method'] == 'POST':
            # метод пост
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))

                course = site.create_course('record', name, category)
                site.courses.append(course)

            return '200 OK', render('course_list.html', objects_list=category.courses,
                                    name=category.name, id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_course.html', name=category.name, id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


# контроллер - создать категорию
@FrameRoute(routes=routes, url='/category-add/')
class CreateCategory:

    @FrameDebug(name='CategoryCreation')
    def __call__(self, request):

        if request['method'] == 'POST':
            # метод пост
            print(request)
            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html', categories=categories)


# контроллер - список категорий
@FrameRoute(routes=routes, url='/category-list/')
class CategoryList:

    @FrameDebug(name='CategoryList')
    def __call__(self, request):
        logger.log('Список категорий')
        return '200 OK', render('category_list.html', objects_list=site.categories)


# контроллер - копировать курс
@FrameRoute(routes=routes, url='/category-copy/')
class CopyCourse:
    @FrameDebug(name='CopyCourse')
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']
            old_course = site.get_course(name)
            if old_course:
                new_name = f'copy_{name}'
                new_course = old_course.clone()
                new_course.name = new_name
                site.courses.append(new_course)

            return '200 OK', render('course_list.html', objects_list=site.courses)
        except KeyError:
            return '200 OK', 'No courses have been added yet'
