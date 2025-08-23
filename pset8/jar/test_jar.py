from jar import Jar
import pytest


def test_init():
    jar = Jar(10)
    assert jar.capacity == 10

    with pytest.raises(ValueError):
        Jar(9.5)

    with pytest.raises(ValueError):
        Jar(-1)


def test_str():
    jar = Jar(10)
    jar.deposit(10)
    assert str(jar) == "🍪" * 10


def test_deposit():
    jar = Jar(10)
    jar.deposit(10)

    assert jar.size == 10

    with pytest.raises(ValueError):
        jar.deposit(1)


def test_withdraw():
    jar = Jar(12)
    jar.deposit(12)
    jar.withdraw(10)

    assert jar.size == 2

    with pytest.raises(ValueError):
        jar.withdraw(3)
