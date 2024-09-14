import pprint
import pytest
import inspect

def pytest_addoption(parser):
    # TODO Вынести название ключа в отдельную переменную?
    group = parser.getgroup("Ы")
    group.addoption("-Ы", action="store_true", help="адаптировать строку по вкусу")


def pytest_itemcollected(item):
    """ Срабатывает сразу после того, как найден очередной item (тест).
        Здесь используем, чтобы сразу подготовить данные item для сбора строки.
    """
    pprint.pprint(item.__dict__)
    print("\n\n\n")
    item.oneline = OneLine(item)
    #item._nodeid = item.oneline.doc


def pytest_report_collectionfinish(config, items):
    """ Срабатывает в конце поиска тестов.
    """
    return pytest_report_collectionfinish.__doc__.strip()


def pytest_report_header(config):
    """ Возвращает заголовок отчёта (вторая строчка после описания платформы).
    """
    if OneLine.on(config):
        pprint.pprint(config.__dict__)
        print("\n\n\n")
        return pytest_report_header.__doc__.strip() 

def pytest_collection_modifyitems(session, config, items):
    """ Меняет состав и параметры найденных тест-кейсов.
        Запускается, как только все тесты найдены.
    """
    if OneLine.on(config):
        for item in items:
            item._nodeid = item.oneline.doc

def pytest_runtest_logstart(nodeid, location):
    #print(f"\nnodeid: {nodeid}\n")
    pass

def pytest_report_teststatus(report, config):
    """ Меняет метку результата теста.
    """
    # TODO Обрабатывать ситуацию SKIPPED
    if report.when == 'call' and OneLine.on(config):
        result = [report.outcome, '', '']
        if report.outcome == 'passed': 
            result[1:3] = ['+', 'Всё хорошо']
        if report.outcome == 'skipped':
            result[1:3] = ['/', 'Так и надо']
        if report.outcome == 'failed':
            result[1:3] = ['!', 'Опаньки']
        #pprint.pprint(report.__dict__)
        return tuple(result)

def pytest_runtest_setup(item):
    #item._nodeid = item.oneline.doc
    pass

def pytest_runtest_call(item):
    #item._nodeid = item.oneline.doc
    pass

def pytest_runtest_makereport(item, call):
    # print(item.oneline.doc, call)
    # item._nodeid = item.oneline.doc
    pass

class OneLine:
    """ Методы и функции для работы со строкой отчёта.
    """
    def __init__(self, item):
        self._init_doc(item)

    def __str__(self):
        return ''

    def __call__(self):
        return ''

    def _init_doc(self, item):
        self.doc = item._obj.__doc__ if item._obj.__doc__ else ''

    @classmethod
    def on(cls, config):
        return config.getoption("Ы") == True
