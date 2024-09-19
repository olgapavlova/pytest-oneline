import pytest
from pprint import pprint

def pytest_runtest_protocol(item):
    """ Запускает протокол обработки конкретного тест-кейса.
        Посмотрим, что внутри.
    """
    pprint(item.__dict__)

def pytest_runtest_logreport(report):
    """ Отвечает за формирование строки отчёта. 
        Посмотрим на все атрибуты этого объекта.
    """
    if report.when == "setup":
        print("\n")
        pprint(report.__dict__)
        print("\n")
