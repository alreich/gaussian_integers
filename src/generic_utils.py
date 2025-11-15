# Generic Utilities

__author__ = "Alfred J. Reich, Ph.D."
__contact__ = "al.reich@gmail.com"
__copyright__ = "Copyright (C) 2024 Alfred J. Reich, Ph.D."
__license__ = "MIT"
__version__ = "1.0.0"

def generate_unit_strings(prefix='e', size=8):
    """Create generic list of unit strings, e.g., 'e1', 'e2', 'e3', ..."""
    if isinstance(prefix, str) and isinstance(size, int) and size > 0:
        count = 1
        result = ['1']
        for x in range(size - 1):
            result.append(prefix + str(count))
            count += 1
    else:
        raise TypeError(f"{prefix} is not a string or {size} is not an integer.")
    return result

def flatten(nested_list):
    """Returns a generator of a flat list."""
    for item in nested_list:
        if isinstance(item, list):
            yield from flatten(item)
        else:
            yield item

def is_power_of_two(n: int):
    """In binary representation, a power of two has exactly one '1' bit,
    and all other bits are '0'. So, when a power of two is decremented
    by one, all the '0' bits to the right of the '1' become '1', and the
    '1' bit becomes '0'. This means that, if n is a power of 2, a bitwise
    AND operation between n and n-1 will result in 0."""
    return n > 0 and (n & (n - 1)) == 0  # bitwise AND

def make_int_or_float(st: str):
    """Cast a string representation of a number into an integer or a float."""
    try:
        f_st = float(st)
    except:
        raise ValueError(f"{st} is not a float nor an int")
    i_st = int(f_st)
    return i_st if i_st == f_st else f_st

class ResettableValue:
    """A object with a 'current' value, that is initialized
    with a 'default' value. The object's value can be set to
    a 'new' value or 'reset' to its default value. All methods,
    except for 'new', are properties; and all methods, except for
    'default', return the current value."""

    def __init__(self, default_value):
        self._default_value = default_value
        self._current_value = default_value

    @property
    def current(self):
        return self._current_value

    @property
    def reset(self):
        self._current_value = self._default_value
        return self._current_value

    @property
    def default(self):
        return self._default_value

    def new(self, new_value):
        self._current_value = new_value
        return self._current_value

# This class is no longer used for this project, but might come in
# handy in the future.
class SetClassVariable:
    """A generic context manager to temporarily set a new value for a
    class variable, and then reset it back to its original value.
    It expects to use a getter/setter method to indirectly get/set
    the class variable, where calling the method without an argument
    will return the current value of the class variable, and calling
    with an argument will set the class variable to that value.
    """
    def __init__(self, getter_setter_method, new_value):
        self.get_set_method = getter_setter_method
        self.new_value = new_value
        self.original_value = None

    def __enter__(self):
        self.original_value = self.get_set_method()
        self.get_set_method(self.new_value)

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type:
            print(f"Something went wrong: {exc_value}")
        self.get_set_method(self.original_value)