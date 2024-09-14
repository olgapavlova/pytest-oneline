import pprint
import pytest
import inspect

""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    Hooks («хуки») для перенастройки строк отчёта о тест-кейсах.
    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """


""" Хуки инициации. Собирают данные и настраивают pytest.
"""

def pytest_configure(config):
    """ Срабатывает сразу после парсинга командной строки.
        Нужно получить конфигурацию как можно быстрее, поэтому здесь.
    """
    OneLine.config(config)

def pytest_addoption(parser):
    """ Добавляет ключ к возможным ключам запуска pytest.
        Ключ используется как булево значение.
    """
    group = parser.getgroup(OneLine.group, OneLine.description)
    group.addoption(str(OneLine.dashkey),
                    action="store_true",
                    help=OneLine.help)

def pytest_itemcollected(item):
    """ Срабатывает сразу после того, как найден очередной тест-кейс (item).
        Здесь используем, чтобы сразу подготовить данные для сбора строки.
    """
    #pprint.pprint(item.__dict__)
    #print("\n\n\n")
    item.oneline = OneLine(item)


""" Хуки формирования строки. Реализуют логику символов и надписей.
"""


def pytest_collection_modifyitems(session, config, items):
    """ Меняет состав и параметры найденных тест-кейсов.
        Запускается, как только все тесты найдены.
    """
    if OneLine.on:
        for item in items:
            item._nodeid = item.oneline.format()

def pytest_report_teststatus(report, config):
    """ Меняет метку результата запуска тест-кейса.
    """
    # TODO Обрабатывать ситуацию SKIPPED
    if report.when == 'call' and OneLine.on:
        match report.outcome:
            case 'passed':  signs = ['+', 'Всё хорошо']
            case 'skipped': signs = ['/', 'Так и надо']
            case 'failed':  signs = ['!', 'Опаньки']
            case _:         signs = ['', '']
        return (report.outcome, *signs)


""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
    Вспомогательные классы, не относящиеся к фреймворку pytest.
    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """

class OneLine:
    """ Методы и функции для работы со строкой отчёта.
    """
    # TODO Возможно, нужно разделить на два класса — конфигурацию и item.

    group = "oneline"
    description = "ключи для настройки вывода"
    _key = "Ы"
    _dash = "-"
    _help = "адаптировать строку отчёта по вкусу"
    _on = None
    _dashkey = None
    _file_prefix = None

    def __init__(self, item):
        self._item = item
        self._init_doc()
        self._init_module()
        self._init_class()
        self._init_function()
        self._init_params()

    def _init_doc(self):
        self.doc = self._item._obj.__doc__ if self._item._obj.__doc__ else ''

    def _init_module(self):
        node = self._item.nodeid
        file = node.split(':')[0]
        file_name = file.split('.')[0]
        associated_module_name = file_name.replace(self.file_prefix, '')
        # TODO Возможно, можно сделать проще через .python_files
        self.module = associated_module_name

    def _init_class(self):
        if self._item._instance:
            full_class_name = self._item._instance.__class__.__name__
            associated_class_name = full_class_name.replace('Test_', '')
            # TODO Совсем нехорошо зашивать сюда 'Test_', лучше использовать .python_classes
            self.cls = associated_class_name
        else:
            self.cls = ''

    def _init_function(self):
        pass

    def _init_params(self):
        pass

    def _format_params(self):
        pass

    def format(self):
        line = []
        line.append(f"{self.module}")
        if self.cls: line.append(f"{self.cls}")
        if len(self.doc) > 27: shortdoc = self.doc[:27] + '...'
        else: shortdoc = self.doc
        line.append(f"{shortdoc:<30}")
        return ' → '.join(line)

    @classmethod
    def config(cls, config=None):
        """ Вызываем в первом же хуке, получившем config.
            Дальше используем как Singleton через свойство .on.
        """
        if config is not None:
            cls._config = config
            cls._on = config.getoption(cls._key)
        else:
            raise Exception("Нет данных конфигурации, а нужны.")

    @classmethod
    @property
    def on(self):
        if self._on is not None:
            return self._on
        else:
            raise Exception("Не установлен статус OneLine при запуске.")

    @classmethod
    @property
    def key(cls):
        return cls._key

    @classmethod
    @property
    def dashkey(cls):
        if cls._dashkey is None:
            cls._dashkey = cls._dash + cls._key
        return cls._dashkey

    @classmethod
    @property
    def help(cls):
        return cls._help

    @classmethod
    @property
    def file_prefix(cls):
        if cls._file_prefix is None:
            cls._file_prefix = 'test_'
            # TODO Расширить до использования .python_files
        return cls._file_prefix

