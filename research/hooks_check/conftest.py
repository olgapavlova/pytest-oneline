import pytest

def i_am_here(function):
    """ Сигнал о том, что мы внутри конкретного хука.
    """
    name = function.__name__
    doc = function.__doc__.strip()
    print(f"\n- - - {name} - - -\n{doc}\n")

def pytest_configure(config):
    """ Срабатывает сразу после парсинга командной строки.
    """
    i_am_here(pytest_configure)
    
def pytest_addoption(parser):
    """ Добавляет ключ к возможным ключам запуска pytest.
    """
    i_am_here(pytest_addoption)

def pytest_itemcollected(item):
    """ Срабатывает сразу после того, как найден очередной тест-кейс (item).
    """
    i_am_here(pytest_itemcollected)

def pytest_collection_modifyitems(session, config, items):
    """ Фильтрует-сортирует список найденных тест-кейсов.
    """
    i_am_here(pytest_collection_modifyitems)

def pytest_report_teststatus(report, config):
    """ Меняет метку результата запуска тест-кейса.
    """
    if report.when == "call":
        i_am_here(pytest_report_teststatus)

def pytest_runtestloop(session):
    """ Запускается основной цикл тестирования и вывода результатов.
    """
    i_am_here(pytest_runtestloop)
    if session.config.getoption("collectonly"):
        print(f"В режиме --collect-only найдено тест-кейсов: {len(session.items)}")
