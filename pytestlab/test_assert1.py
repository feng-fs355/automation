import pytest

@pytest.fixture()
def some_data():
    return 42
def test_some_data(some_data):
    """Return value for fixture"""
    assert some_data == 42

def test_inc_data(some_data):
    """Use fixture return value in a test"""
    inc_data = some_data + 1
    assert inc_data == 43


##def test_zero_division():
##    with pytest.raises(ZeroDivisionError):
##        1 / 0

#@pytest.mark.parametrize("a,b,c,expected", [
#    (0, 1, 3, "Is not triangle"),
#    (1, 1, 1, "Its a 3 the same triangle"),
#    (2, 2, 3, "2 the same triangle"),
#    (3, 4, 5, "90% dgree triangle"),
#    (4, 5, 6, "normal triangle")
#])
#def test_type_triangle(a, b, c, expected):
#   assert expected == type_of_triange(a, b, c)
