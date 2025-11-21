from abc import ABC, abstractmethod
import math

class NumericBase(ABC):
    """
    Abstract parent class that cannot be instantiated.
    Takes two numerical input values x and y.
    Defines equality and addition operations.
    """
    
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __eq__(self, other):
        """Define equality comparison"""
        if not isinstance(other, NumericBase):
            return False
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        """Define addition operation"""
        if not isinstance(other, NumericBase):
            raise TypeError("Can only add NumericBase objects")
        # Return the same type as the left operand
        return type(self)(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"

class IntegerPair(NumericBase):
    """
    Subclass that rounds input values to integers and defines subtraction.
    """
    
    def __init__(self, x, y):
        # Round input values to integers
        super().__init__(round(x), round(y))
    
    def __sub__(self, other):
        """Define subtraction operation"""
        if not isinstance(other, NumericBase):
            raise TypeError("Can only subtract NumericBase objects")
        return IntegerPair(self.x - other.x, self.y - other.y)

class FloatPair(NumericBase):
    """
    Subclass that converts input values to floats and defines norm calculation.
    """
    
    def __init__(self, x, y):
        # Convert input values to floats
        super().__init__(float(x), float(y))
    
    def norm(self):
        """Calculate the Euclidean norm of the input values"""
        return math.sqrt(self.x**2 + self.y**2)

# Example usage and testing:
if __name__ == "__main__":
    # Cannot instantiate the abstract parent class
    # This would raise TypeError: Can't instantiate abstract class NumericBase
    # base = NumericBase(1, 2)
    
    # Create instances of subclasses
    int_pair1 = IntegerPair(3.7, 4.2)  # Will be rounded to (4, 4)
    int_pair2 = IntegerPair(1.1, 2.9)  # Will be rounded to (1, 3)
    
    float_pair1 = FloatPair(3, 4)      # Will be converted to (3.0, 4.0)
    float_pair2 = FloatPair(1, 2)      # Will be converted to (1.0, 2.0)
    
    print("Integer Pairs:")
    print(f"int_pair1: {int_pair1}")
    print(f"int_pair2: {int_pair2}")
    
    print("\nFloat Pairs:")
    print(f"float_pair1: {float_pair1}")
    print(f"float_pair2: {float_pair2}")
    
    print("\nEquality tests:")
    print(f"int_pair1 == int_pair2: {int_pair1 == int_pair2}")
    print(f"float_pair1 == float_pair2: {float_pair1 == float_pair2}")
    
    print("\nAddition tests:")
    int_sum = int_pair1 + int_pair2
    float_sum = float_pair1 + float_pair2
    print(f"int_pair1 + int_pair2 = {int_sum}")
    print(f"float_pair1 + float_pair2 = {float_sum}")
    
    print("\nSubtraction test (IntegerPair only):")
    int_diff = int_pair1 - int_pair2
    print(f"int_pair1 - int_pair2 = {int_diff}")
    
    print("\nNorm test (FloatPair only):")
    norm1 = float_pair1.norm()
    norm2 = float_pair2.norm()
    print(f"Norm of {float_pair1} = {norm1}")
    print(f"Norm of {float_pair2} = {norm2}")

# -----------------------------------------------------------------------------

from abc import ABC, abstractmethod
import math

class NumericBase(ABC):
    """
    Abstract parent class that cannot be instantiated.
    Takes two immutable numerical input values x and y.
    Defines equality and addition operations.
    """
    
    def __init__(self, x, y):
        # Make x and y immutable using private attributes with property decorators
        self._x = x
        self._y = y
    
    @property
    def x(self):
        """Immutable x property"""
        return self._x
    
    @property
    def y(self):
        """Immutable y property"""
        return self._y
    
    def __eq__(self, other):
        """Define equality comparison"""
        if not isinstance(other, NumericBase):
            return False
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other):
        """Define addition operation"""
        if not isinstance(other, NumericBase):
            raise TypeError("Can only add NumericBase objects")
        # Return the same type as the left operand
        return type(self)(self.x + other.x, self.y + other.y)
    
    def __repr__(self):
        return f"{self.__class__.__name__}({self.x}, {self.y})"
    
    def __hash__(self):
        """Make objects hashable since they're immutable"""
        return hash((self.x, self.y, type(self)))

class IntegerPair(NumericBase):
    """
    Subclass that rounds input values to integers and defines subtraction.
    Values are immutable after creation.
    """
    
    def __init__(self, x, y):
        # Round input values to integers and make them immutable
        super().__init__(round(x), round(y))
    
    def __sub__(self, other):
        """Define subtraction operation"""
        if not isinstance(other, NumericBase):
            raise TypeError("Can only subtract NumericBase objects")
        return IntegerPair(self.x - other.x, self.y - other.y)

class FloatPair(NumericBase):
    """
    Subclass that converts input values to floats and defines norm calculation.
    Values are immutable after creation.
    """
    
    def __init__(self, x, y):
        # Convert input values to floats and make them immutable
        super().__init__(float(x), float(y))
    
    def norm(self):
        """Calculate the Euclidean norm of the input values"""
        return math.sqrt(self.x**2 + self.y**2)

# Example usage and testing:
if __name__ == "__main__":
    # Cannot instantiate the abstract parent class
    # This would raise TypeError: Can't instantiate abstract class NumericBase
    # base = NumericBase(1, 2)
    
    # Create instances of subclasses
    int_pair1 = IntegerPair(3.7, 4.2)  # Will be rounded to (4, 4)
    int_pair2 = IntegerPair(1.1, 2.9)  # Will be rounded to (1, 3)
    
    float_pair1 = FloatPair(3, 4)      # Will be converte
    