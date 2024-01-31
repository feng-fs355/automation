import pytest
def myfunc(n):
  return lambda a : a * n
def test_mydoubler():
  mydoubler = myfunc(2)
  print(f'{mydoubler(11)}  ', end="")
  print(f'{mydoubler(22)}  ', end="")
  print(f'{mydoubler(33)}  ', end="")

thisdict = {
  "brand": "Ford",
  "electric": False,
  "year": 1964,
  "colors": ["red", "white", "blue"]
}
print(thisdict)

@pytest.fixture()
def hello():
    return 123
def test_string(hello):
    assert hello == 123, "fixture should return 123"