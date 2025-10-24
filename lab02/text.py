
class fibonacci:
    def __init__(self, steps: int):
        if steps < 0:
            raise ValueError("steps musi być liczbą nieujemną")
        self._steps_total = steps
        self._yielded = 0
        self._a = 0  # F0
        self._b = 1  # F1

    def __iter__(self):
        return self

    def __next__(self):
        if self._yielded >= self._steps_total:
            raise StopIteration
        # Zwracamy bieżący wyraz i przesuwamy parę (a, b)
        value = self._a
        self._a, self._b = self._b, self._a + self._b
        self._yielded += 1
        return value


# ===== PRZYKŁAD UŻYCIA =====
if __name__ == "__main__":
    print(list(fibonacci(0)))   # []
    print(list(fibonacci(1)))   # [0]
    print(list(fibonacci(2)))   # [0, 1]
    print(list(fibonacci(7)))   # [0, 1, 1, 2, 3, 5, 8]
