import pytest
from app.calc import add

@pytest.mark.parametrize("num1, num2, expected", [
    (5, 4, 9),
    (12, 13, 25),
    (25, 1000, 1025)
])
def test_add(num1, num2, expected):
    # sum = 8
    assert add(num1,num2) == expected