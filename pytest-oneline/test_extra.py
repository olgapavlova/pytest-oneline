import pytest

@pytest.fixture
def i_am_here():
    return "я тут"

class Test_Extra:
    def test_fixture(self, i_am_here):
        'Тестируем фикстуру'
        assert i_am_here == "я тут"

    @pytest.mark.blabla
    def test_marks(self):
        'Тестируем метки'
        assert True 
