import pytest


@pytest.fixture
def setup_up_pre_and_post_conditions():
    print("Pre condition 1") # 1
    yield
    print("Post condition 3") # 3

def test(setup_up_pre_and_post_conditions):
    print("Body of test 2") #2
