
class Complex:
    """Prosta implementacja liczby zespolonej: a + bi."""
    __slots__ = ("re", "im")

    def __init__(self, re=0.0, im=0.0):
        self.re = float(re)
        self.im = float(im)

    # --- Dodawanie ---
    def __add__(self, other):
        if isinstance(other, Complex):
            return Complex(self.re + other.re, self.im + other.im)
        if isinstance(other, (int, float)):
            return Complex(self.re + other, self.im)
        return NotImplemented

    def __radd__(self, other):
        # pozwala na: 2 + Complex(1, 3)
        return self.__add__(other)

    # --- Odejmowanie ---
    def __sub__(self, other):
        if isinstance(other, Complex):
            return Complex(self.re - other.re, self.im - other.im)
        if isinstance(other, (int, float)):
            return Complex(self.re - other, self.im)
        return NotImplemented

    def __rsub__(self, other):
        # pozwala na: 2 - Complex(1, 3)
        if isinstance(other, (int, float)):
            return Complex(other - self.re, -self.im)
        if isinstance(other, Complex):
            return Complex(other.re - self.re, other.im - self.im)
        return NotImplemented

    # --- Reprezentacja tekstowa ---
    def __repr__(self):
        return f"Complex({self.re}, {self.im})"

    def __str__(self):
        sign = "+" if self.im >= 0 else "-"
        return f"{self.re} {sign} {abs(self.im)}i"

    # --- Porównywanie (opcjonalnie, z tolerancją) ---
    def __eq__(self, other):
        if isinstance(other, Complex):
            return self.re == other.re and self.im == other.im
        if isinstance(other, (int, float)):
            return self.re == float(other) and self.im == 0.0
        return NotImplemented


if __name__ == "__main__":
    z1 = Complex(2, 3)      # 2 + 3i
    z2 = Complex(-1, 0.5)   # -1 + 0.5i

    print("z1 =", z1)                   # 2 + 3i
    print("z2 =", z2)                   # -1 + 0.5i
    print("z1 + z2 =", z1 + z2)         # (2-1) + (3+0.5)i = 1 + 3.5i
    print("z1 - z2 =", z1 - z2)         # (2+1) + (3-0.5)i = 3 + 2.5i
    print("z1 + 5  =", z1 + 5)          # 7 + 3i
    print("5 + z1  =", 5 + z1)          # 7 + 3i
    print("z1 - 1  =", z1 - 1)          # 1 + 3i
    print("1 - z1  =", 1 - z1)          # -1 - 3i
