import os
import math
import uiautomator2 as Device

def test_sqrt():
    num = 25
    assert math.sqrt(num) ==5
def test_strip():
    a = " Hello, World! "
    print(a.strip())  # returns "Hello, World!"
def test_helo():
    a = "Hello, PYTEST"
    print(a.lower())
def test_replace():
    a = "Hello, World!"
    print(a.replace("H", "J"))
def test_bool():
    print(bool("Hello"))
    print(bool(15))