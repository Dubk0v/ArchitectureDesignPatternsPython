from jinja2 import FileSystemLoader
from jinja2.environment import Environment

def render_(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры
    :return:
    """
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    # Пример использования
    output_test = render_('index.html', name_company='ООО Сладкоежка')
    print(output_test)
