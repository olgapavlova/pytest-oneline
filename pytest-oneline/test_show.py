import pytest 

def test_pass():
    'Всегда проходит.'
    assert True

def test_fail():
    'Всегда падает.'
    assert False

@pytest.mark.xfail
def test_xfail():
    'Всегда падает, но это неважно.'
    assert False

@pytest.mark.skip
def test_skip():
    'Всегда пропускаем.'
    assert True

class Test_Demo:
    def test_class_name(self):
        'Покажем имя класса, когда оно есть.'
        assert True

    @pytest.mark.parametrize("a, b",
        [(1, 2), ("one", "two")],
        ids = ["цифры", "буквы"])
    def test_params(self, a, b):
        'Выведем параметры тестовой функции.'
        assert True
