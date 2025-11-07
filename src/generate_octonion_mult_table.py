#!/usr/bin/env python
# coding: utf-8

# EXECUTABLE PYTHON SCRIPT

# Derives and prints  Wikipedia's Octonion Multiplication Table
# (see https://en.wikipedia.org/wiki/Octonion#Multiplication)

from cayley_dickson_integers import Zi

# Create dictionary of Octonion units
octonion_units_dict = {
    # Key = Unit Name
    # Value = Unit octonion in Zi form
    'e0': Zi.from_string("1").increase_order(3),
    'e1': Zi.from_string("i").increase_order(3),
    'e2': Zi.from_string("j").increase_order(3),
    'e3': Zi.from_string("k").increase_order(3),
    'e4': Zi.from_string("L"),
    'e5': Zi.from_string("I"),
    'e6': Zi.from_string("J"),
    'e7': Zi.from_string("K")
}

# Create a reverse dictionary from the one above,
# then create a reverse dictionary of the negative units,
# and use that to augment the original reverse dictionary
rev = {val: key for key, val in octonion_units_dict.items()}
negs = {-z: '-' + e for z, e in rev.items()}
rev.update(negs)

def octmul(a, b):
    """A convenience function for multiplying two octonion units and
    obtaining the resulting octonion unit."""
    return rev[octonion_units_dict[a] * octonion_units_dict[b]]

# Extract a list of the octonion unit names
octonion_unit_names = list(octonion_units_dict.keys())

# Print the table's column headings
header = '   '
for x in octonion_unit_names:
    header += f"{x:>3} "
print(header)

# Print the table's rows
for x in octonion_unit_names:
    row = x + ' '
    for y in octonion_unit_names:
        row += f"{octmul(x, y):>3} "
    print("-"*34)
    print(row)


# END OF FILE
