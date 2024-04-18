import os

def is_done(path):
    if not os.path.exists(path):
        return False
    with open(path) as _f:
        contents = _f.read()
    if "yes" in contents.lower():
        return True
    elif "no" in contents.lower():
        return False

class TestIsDone:

    def teardown(self):
        if os.path.exists("/tmp/test_file"):
            os.remove("/tmp/test_file")	

    def test_yes(self):
        with open("/home/idltest/Documents/GitHub/autotest/APP/tmp/test_file", "w") as _f:
            _f.write("yes")
        assert is_done("/home/idltest/Documents/GitHub/autotest/APP/tmp/test_file") is True

    def test_no(self):
        with open("/home/idltest/Documents/GitHub/autotest/APP/tmp/test_file", "w") as _f:
            _f.write("no")
        assert is_done("/home/idltest/Documents/GitHub/autotest/APP/tmp/test_file") is False