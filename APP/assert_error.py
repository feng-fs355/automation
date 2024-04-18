
def divide(x, y):
    assert y != 0, "Cannot divide by zero"
    return x / y

try:
    result = divide(10, 0)
except AssertionError as error:
    print("AssertionError occurred:", error)
    print("Error message:", error.args[0])