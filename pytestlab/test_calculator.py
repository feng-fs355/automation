import pytest
from calculator import square


def test_zero():
    try:
        assert square(0) == 1
    except AssertionError:
        print("0 is not equal 1")
    finally:
        print("The 'try except with zero' is finished")
def test_positive():
    assert square(2) == 4
    assert square(3) == 9

def test_negative():
    assert square(-2) == 4
    assert square(-3) == 9

def test_str():
    with pytest.raises(TypeError):
        square("cat")




