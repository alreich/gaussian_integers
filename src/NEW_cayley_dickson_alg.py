from abc import ABC  #, abstractmethod

class CayleyDicksonBase(ABC):

    def __init__(self, real, imag):
        self._re = real
        self._im = imag

    @property
    def real(self):
        return self._re

    @property
    def imag(self):
        return self._im

    def __repr__(self):
        return f"{self.__class__.__name__}({self.real}, {self.imag})"

    def __hash__(self):
        return hash((self.real, self.imag, type(self)))


class Zi(CayleyDicksonBase):

    def __init__(self, real, imag):
        if isinstance(real, (float, int)):
            if imag is None:
                super().__init__(round(real), 0)
            elif isinstance(imag, (float, int)):
                super().__init__(round(real), round(imag))
            else:
                raise Exception(f"Inputs incompatible: {real} and {imag}")
        elif isinstance(real, complex):
            if imag is None:
                super().__init__(round(real.real), round(real.imag))
            elif isinstance(imag, (complex, Zi)):
                super().__init__(Zi(real, None), Zi(imag, None))
            else:
                raise Exception(f"Inputs incompatible: {real} and {imag}")
        elif isinstance(real, Zi):
            if imag is None:
                super().__init__(real.real, real.imag)
            elif isinstance(imag, (complex, Zi)):
                super().__init__(Zi(real, None), Zi(imag, None))
            else:
                raise Exception(f"Inputs incompatible: {real} and {imag}")

        elif real is None:
            if imag is None:
                super().__init__(0, 0)
            else:
                raise Exception(f"If re is None, then im must be None. But im = {imag}")
        else:
            raise Exception("We should never get to this point in the code")

    def __eq__(self, other):
        if isinstance(other, Zi):
            return self.real == other.real and self.imag == other.imag
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

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


class Qi(CayleyDicksonBase):

    def __init__(self, real, imag):
        super().__init__(float(real), float(imag))

    def norm(self):
        """Square of the usual norm."""
        return self.real ** 2 + self.imag ** 2


# Example usage and testing:
if __name__ == "__main__":

    print("=== Zi and Qi Demo ===\n")

    print("=== End of Demo ===\n")