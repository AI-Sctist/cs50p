class Jar:
    def __init__(self, capacity: int = 12) -> None:
        if isinstance(capacity, int) and capacity >= 0:
            self._size = 0
            self._capacity = capacity
        else:
            raise ValueError("Not a non-negative integer")

    def __str__(self) -> str:
        return "🍪" * self.size

    def deposit(self, n: int) -> None:
        if self.size + n <= self.capacity:
            self._size += n
        else:
            raise ValueError("Overcapacity")

    def withdraw(self, n: int) -> None:
        if self.size - n >= 0:
             self._size -= n
        else:
            raise ValueError("Not enough cookies")

    @property
    def capacity(self) -> int:
        return self._capacity

    @property
    def size(self) -> int:
        return self._size
