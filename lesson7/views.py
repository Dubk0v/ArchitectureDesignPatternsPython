from datetime import date

from framework.templates import render
from patterns.сreational_patterns import Engine, Logger
from patterns.structural_patterns import FrameRoute, FrameDebug
from patterns.behavioral_patterns import ListView, CreateView, EmailNotifier, SmsNotifier
from urllib.parse import unquote
from mappers import MapperRegistry
from framework.unitofwork import UnitOfWork


site = Engine()
logger = Logger('main')
routes = {}
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)


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
@FrameRoute(routes=routes, url='/courses-list/')
class CoursesList:
    @FrameDebug(name='CoursesList')
    def __call__(self, request):
        logger.log('Список курсов')
        try:
            category = site.find_category_by_id(int(request['request_params']['id']))
            return '200 OK', render('course_list.html', objects_list=category.courses, name=category.name,
                                    id=category.id)
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

                # Добавляем наблюдателей на курс
                course.observers.append(email_notifier)
                course.observers.append(sms_notifier)

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


@FrameRoute(routes=routes, url='/area-list/')
class AreaListView(ListView):
    query_set = site.areas
    template_name = 'area-list.html'


@FrameRoute(routes=routes, url='/area-creation/')
class AreaCreateView(CreateView):
    template_name = 'area-creation.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        city = data['city']
        city = site.decode_value(city)
        address = data['address']
        address = site.decode_value(address)
        phone_number = data['phone_number']
        phone_number = site.decode_value(phone_number)

        new_obj = site.create_area(name, city, address, phone_number)
        site.areas.append(new_obj)


@FrameRoute(routes=routes, url='/add-student/')
class AddStudentByCourseCreateView(CreateView):
    template_name = 'add-student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        print(data)

        course_name = unquote(data['course_name'])
        course = site.get_course(course_name)

        student_name = unquote(data['student_name'])
        student = site.get_student(student_name)
        course.add_student(student)


@FrameRoute(routes=routes, url='/student-list/')
class StudentListView(ListView):
    queryset = site.students
    template_name = 'student-list.html'