from abc import ABC  #, abstractmethod

class CDalgBase(ABC):

    def __init__(self, real, imag):
        self._re = real
        self._im = imag

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    def __eq__(self, other):
        if isinstance(other, CDalgBase):
            return self.real == other.real and self.imag == other.imag
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.real}, {self.imag})"

    def __hash__(self):
        """Make objects hashable since they're immutable"""
        return hash((self.real, self.imag, type(self)))


class Zi(CDalgBase):

    def __init__(self, real, imag):
        super().__init__(round(real), round(imag))

    def __add__(self, other):
        if isinstance(other, Zi):
            return Zi(self.real + other.real, self.imag + other.imag)
        else:
            raise TypeError("Can only add Zi objects")

    def __sub__(self, other):
        if isinstance(other, Zi):
            return Zi(self.real - other.real, self.imag - other.imag)
        else:
            raise TypeError("Can only subtract Zi objects")


class Qi(CDalgBase):

    def __init__(self, real, imag):
        super().__init__(float(real), float(imag))

    def norm(self):
        """Square of the usual norm."""
        return self.real ** 2 + self.imag ** 2


# Example usage and testing:
if __name__ == "__main__":

    print("=== Zi and Qi Demo ===\n")

    print("=== End of Demo ===\n")