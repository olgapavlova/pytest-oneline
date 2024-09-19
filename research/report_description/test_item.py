import pytest 

def test_pass():
    'Всегда проходит.'
    assert True

def test_xfail():
    'Предсказуемо падает.'
    assert False

@pytest.mark.skipif(True, reason="пропускаем")
def test_skipif():
    'Условно пропускаем.'
    assert False

@pytest.mark.skip
def test_skip():
    'Безусловно пропускаем.'
    assert True
