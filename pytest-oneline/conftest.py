import pytest
from dataclasses import dataclass

""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 
    Hooks («хуки») для перенастройки строк отчёта о тест-кейсах.
    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """


""" Хуки инициации. Собирают данные и настраивают pytest.
"""

def pytest_configure(config):
    """ Срабатывает сразу после парсинга командной строки.
        Нужно получить конфигурацию как можно быстрее, поэтому здесь.
    """
    OneLineState(config)

def pytest_addoption(parser):
    """ Добавляет ключ к возможным ключам запуска pytest.
        Ключ используется как булево значение.
    """
    op = OneLinePreset()
    group = parser.getgroup(op.group, op.description)
    group.addoption(str(op.dashkey),
                    action="store_true",
                    help=op.helpp)

def pytest_itemcollected(item):
    """ Срабатывает сразу после того, как найден очередной тест-кейс (item).
        Здесь используем, чтобы сразу подготовить данные для сбора строки.
    """
    item.oneline = OneLineItem(item)


""" Хуки формирования строки. Реализуют логику символов и надписей.
"""


def pytest_collection_modifyitems(session, config, items):
    """ Меняет состав и параметры найденных тест-кейсов.
        Запускается, как только все тесты найдены.
    """
    if OneLineState().on:
        for item in items:
            item._nodeid = item.oneline.format()

def pytest_report_teststatus(report, config):
    """ Меняет метку результата запуска тест-кейса.
    """
    # TODO Обрабатывать ситуацию SKIPPED
    if report.when == 'call' and OneLineState().on:
        match report.outcome:
            case 'passed':  signs = ['+', 'Всё хорошо']
            case 'skipped': signs = ['/', 'Так и надо']
            case 'failed':  signs = ['!', 'Опаньки']
            case _:         signs = ['', '']
        return (report.outcome, *signs)

def pytest_runtestloop(session):
    """ Запускается основной цикл тестирования и вывода результатов.
        Для режима --collect-only срабатывает только сам хук. 
    """
    if session.config.option.collectonly:
        print("\n".join([i._nodeid for i in session.items]))


""" * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *  
    Вспомогательные классы, не относящиеся к фреймворку pytest.
    * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * """


@dataclass
class OneLinePreset:
    """ Настройки системы. Датакласс.
    """
    key: str = "Ы"
    dash: str = "-"
    helpp: str = "Вывод строк отчёта в своём формате" 
    group: str = "Ключи плагина OneLine"
    description: str = "Потихоньку добавляем то, что нужно." 
    file_prefix: str = "test_"  # TODO Расширить до использования .python_files

    @property
    def dashkey(self):
        return self.dash + self.key


class OneLineState:
    """ Состояние системы. Контейнер для config. Singleton.
    """
    instance = None

    def __new__(cls, config=None):
        if cls.instance is None:
            instance = super().__new__(cls)
            cls.instance = instance
        return cls.instance

    def __init__(self, config=None):
        if config is not None:
            self.config = config
            self.preset = OneLinePreset()
            self.on = bool(config.getoption(self.preset.key))
        else:
            if self.config is None:
                raise OneLineException("Нет данных конфигурации, а нужны.")

    @classmethod
    def __getattr__(cls, name):
        try:
            return getattr(cls, "_" + name)
        except Exception:
            raise OneLineException(f"Атрибут {name} в классе OneLineState не существует.")


class OneLineItem:
    """ Методы и функции для работы со строкой отчёта.
    """
    def __init__(self, item):
        self.item = item  # Родительская строка
        self._init_doc()
        self._init_module() # .module — имя тестируемого модуля без префикса "test_" и окончания ".py"
        self._init_class()  # .cls — тест-класс тестирующей функции
        self._init_function()  # .function — название тестирующей функции без префикса "test_"
        self._init_params()

    def _init_doc(self):
        self.doc = getattr(self.item._obj, "__doc__", "")

    def _init_module(self):
        node = self.item.nodeid  # В этой точке nodeid ещё не менялся
        file = node.split(':')[0]
        file_name = file.split('.')[0]
        associated_module_name = file_name.replace(OneLinePreset().file_prefix, '')
        self.module = associated_module_name

    def _init_class(self):
        if self.item._instance:
            full_class_name = self.item._instance.__class__.__name__
            associated_class_name = full_class_name.replace('Test_', '')
            # TODO Совсем нехорошо зашивать сюда 'Test_', лучше использовать .python_classes
            self.cls = associated_class_name
        else:
            self.cls = None

    def _init_function(self):
        self.function = self.item.name.replace(OneLinePreset().file_prefix, '').split('[')[0]

    def _init_params(self):
        try:
            self.params = self.item.callspec.params
        except Exception:
            self.params = None


    def _format_params(self):
        pass

    def format(self):
        self._preformat()
        format_template = "{o.module} | {o.cls}{o.function:5} • {o.doc:25} {o.params}"
        return format_template.format(o=self) 

    def _preformat(self):
        self._preformat_doc()
        self._preformat_params()
        self._preformat_cls()

    def _preformat_cls(self):
        if self.cls is not None:
            self.cls = self.cls + ' → '
        else:
            self.cls = ''

    def _preformat_doc(self):
        if (len(self.doc) > 25): self.doc = self.doc[:23] + "..."

    def _preformat_params(self):
        if self.params is not None:
            self.params = '(' + ', '.join([str(a) + '=' + str(b) for a, b in self.params.items()]) + ')'
        else:
            self.params = ''

class OneLineException(Exception):
    pass
