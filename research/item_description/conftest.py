import pytest
from pprint import pprint

def pytest_itemcollected(item):
    """ Срабатывает сразу после того, как найден очередной тест-кейс (item).
        Посмотрим на все атрибуты этого объекта.
    """
    print("\n\n")
    pprint(item.__dict__)
    print("\n\n")
