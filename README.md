# Gaussian Integers and Gaussian Rational Numbers

This module defines two classes, **Zi** and **Qi**, the Gaussian integers and Gaussian rational numbers, respectively.

Mathematically, the integers are denoted by $\mathbb{Z}$, the rational numbers by $\mathbb{Q}$, and the complex numbers by $\mathbb{C}$.

$\mathbb{C} \equiv \lbrace a + bi: a, b \in \mathbb{R} \rbrace$ where $\mathbb{R}$ is the set of real numbers and $i^2 = -1$.

The **Gaussian integers** are denoted by $\mathbb{Z}[i] \equiv \lbrace n + mi: n, m \in \mathbb{Z} \rbrace \subset \mathbb{C}$,

and the **Gaussian rationals** are denoted by $\mathbb{Q}[i] \equiv \lbrace r + si: r, s \in \mathbb{Q} \rbrace \subset \mathbb{C}$.

NOTE:

* Python uses $j$ instead of $i$ to represent complex numbers
* Although, both **Zi** and **Qi** are subclasses of **numbers.Complex**, and $\mathbb{Z}[i] \subset \mathbb{Q}[i] \subset \mathbb{C}$, the class **Zi** is **not** a subclass of the class **Qi**.

For more information, see the two Jupyter notebooks in the notebooks directory.

For a quick look, see the examples following the plot of Gaussian primes, below.

![alt text](https://github.com/alreich/gaussian_integers/blob/main/gaussian_integers_plot.png?raw=true)

# Gaussian Integers


```python
>>> from gaussians import Zi, Qi
# >>> from fractions import Fraction
>>> from math import floor, ceil
```

## Instantiating Gaussian Integers

* In general, the constructor is, ``Zi(a, b)``, where ``a`` and ``b`` are integers or floats; floats are rounded
* ``Zi() = Zi(0) = Zi(0, 0) = 0``
* If ``a`` is an integer or float, then ``Zi(a) = Zi(round(a), 0)``
* If ``a`` is complex, then ``Zi(a) = Zi(a, _) = Zi(round(a.real), round(a.imag))``; a second argument is ignored
* ``eye``, ``two``, and ``units`` are static methods that produce, respectively, ``i = Zi(0, 1)``, ``Zi(1, 1)``, and the set ``{1, -1, i, -i}``

### Examples


```python
>>> z = Zi(2, -3)
>>> print(f"{z = }")
>>> print(f"z = {z}")  # printed/string representations are same as usual Python complex numbers
```

    z = Zi(2, -3)
    z = (2-3j)



```python
>>> zero = Zi()       ; print(f"{ zero = }    = {zero}")
>>> one  = Zi(1)      ; print(f"{  one = }    = {one}")

>>> two   = Zi.two()  ; print(f"{  two = } = {two}")  # norm = 2
>>> i     = Zi.eye()  ; print(f"{    i = } = {i}")
>>> units = Zi.units(); print(f"{units = }")
```

     zero = Zi(0)    = 0
      one = Zi(1)    = 1
      two = Zi(1, 1) = (1+1j)
        i = Zi(0, 1) = 1j
    units = [Zi(1), Zi(-1), Zi(0, 1), Zi(0, -1)]



```python
>>> a = Zi(2-3j); print(f"{a = } = {a}")  # Zi created from a single complex argument
>>> b = Zi(-2.8, 5.2); print(f"{b = } = {b}") # floats are rounded
```

    a = Zi(2, -3) = (2-3j)
    b = Zi(-3, 5) = (-3+5j)


## Properties of Gaussian Integers

The usual properties of complex numbers are also supported for Gaussian integers:

* real part
* imaginary part
* conjugate
* norm

### Examples


```python
>>> print(f"{z = }")

>>> print(f"{z.real = }")
>>> print(f"{z.imag = }")
>>> print(f"{z.conjugate = }")
>>> print(f"{z.norm = }")
>>> print(f"{z.is_unit = }")
```

    z = Zi(2, -3)
    z.real = 2
    z.imag = -3
    z.conjugate = Zi(2, 3)
    z.norm = 13
    z.is_unit = False


## Univariate Functions of Gaussian Integers

The following operations can be performed on a Gaussian integer:

* compute absolute value
* convert to string
* convert to standard Python complex number
* negate

### Examples


```python
>>> print(f"{abs(z) = }")
>>> print(f"{str(z) = }")
>>> print(f"{complex(z) = }")
>>> print(f"{-z = }")
```

    abs(z) = 3.605551275463989
    str(z) = '(2-3j)'
    complex(z) = (2-3j)
    -z = Zi(-2, 3)


## Arithmetic

Most of the usual arithmetic operations that can be performed on complex number are supported, such as infix operators and in-place assignment operators.

Additionally, arithmetic can mix standard Python integers with Gaussian integers.

### Examples

The following infix operators are supported: ``+``, ``-``, ``*``, ``**``, ``/``, ``//``, ``%``


```python
>>> a = Zi(4, 10)
>>> b = Zi(1, -2)
>>> c = a * b

>>> print(f"{a + b = }")
>>> print(f"{a - b = }")
>>> print(f"{a * b = }")
>>> print(f"{a / b = }")  # In general, truediv will return a Gaussian rational,
>>> print(f"{c / b = }")  #     unless b | c, in which case, a Zi is returned.
>>> print(f"{a // b = }")  # floordiv uses round instead of floor.
>>> print(f"{c % b = }")
>>> print(f"{a**2 = }")
>>> print(f"{a**0 = }")
>>> print(f"{a**-1 = }")  # This will yield a Gaussian rational, except for units
>>> print(f"{i**-1 = }")  # 1/i = -i
```

    a + b = Zi(5, 8)
    a - b = Zi(3, 12)
    a * b = Zi(24, 2)
    a / b = Qi('-16/5', '18/5')
    c / b = Zi(4, 10)
    a // b = Zi(-3, 4)
    c % b = Zi(0)
    a**2 = Zi(-84, 80)
    a**0 = Zi(1)
    a**-1 = Qi('1/29', '-5/58')
    i**-1 = Zi(0, -1)


Mixed integer and Gaussian integer arithmetic is supported.


```python
>>> print(f"{a + 2 = }")
>>> print(f"{a - 2 = }")
>>> print(f"{a * 2 = }")
>>> print(f"{a / 2 = }\n")

>>> print(f"{2 + a = }")
>>> print(f"{2 - a = }")
>>> print(f"{2 * a = }")
>>> print(f"{2 / a = }")
```

    a + 2 = Zi(6, 10)
    a - 2 = Zi(2, 10)
    a * 2 = Zi(8, 20)
    a / 2 = Zi(2, 5)
    
    2 + a = Zi(6, 10)
    2 - a = Zi(-2, -10)
    2 * a = Zi(8, 20)
    2 / a = Qi('2/29', '-5/29')


In-place assignment operators, ``+=``, ``-=``, and ``*=`` are also supported.

Here's an example that uses ``+=``:


```python
>>> zi_sum = Zi()
>>> int_sum = 0  # Also works for floats or complex (e.g., 0.0 or (0j))

>>> for k in range(5):
>>>     int_sum += k
>>>     zi_sum  += Zi(k, k)

>>> print(int_sum, zi_sum)
```

    10 (10+10j)


## Number Theory with Gaussian Integers

Many of the examples below are from ["The Gaussian Integers"](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf) by Keith Conrad

### The Modified Division Theorem

For $\alpha, \beta \in \mathbb{Z}[i]$ with $\beta \ne 0$, there are $\gamma, \rho \in \mathbb{Z}[i]$ such that $\alpha = \beta \gamma + \rho$ and $N(\rho) \le (1/2)N(\beta)$.

**Example**


```python
>>> help(Zi.modified_divmod)
```

    Help on function modified_divmod in module gaussians:
    
    modified_divmod(a, b)
        The divmod algorithm, modified for Gaussian integers.
        
        Returns q & r, such that a = b * q + r, where
        r.norm < b.norm / 2. This is the Modified Division
        Theorem described in 'The Gaussian Integers' by Keith Conrad
    



```python
>>> alpha = Zi(27, -23)
>>> beta = Zi(8, 1)

>>> gamma, rho = Zi.modified_divmod(alpha, beta)

>>> print(f"{beta * gamma + rho} = {beta} * {gamma} + {rho}")

>>> print(f"\nN({rho}) = {rho.norm} and (1/2)*N({beta}) = {(1/2) * beta.norm}")
```

    (27-23j) = (8+1j) * (3-3j) + -2j
    
    N(-2j) = 4 and (1/2)*N((8+1j)) = 32.5


### Greatest Common Divisor (GCD)

**The Euclidean Algorithm**

Let $\alpha, \beta \in \mathbb{Z}[i]$ be non-zero, then we can recursively apply the Division Theorem to obtain the Greatest Common Divisor (GCD) of $\alpha$ and $\beta$.

**Example**


```python
>>> help(Zi.gcd)
```

    Help on function gcd in module gaussians:
    
    gcd(a, b, verbose=False)
        A gcd algorithm for Gaussian integers.
        Returns the greatest common divisor of a & b.
        
        This function implements the Euclidean algorithm for Gaussian integers.
    



```python
>>> alpha = Zi(11, 3)
>>> beta = Zi(1, 8)

>>> gcd = Zi.gcd(alpha, beta, verbose=True)  # Prints intermediate results

>>> print(f"\ngcd({alpha}, {beta}) -> {gcd}")
```

       (11+3j) = (1+8j) * (1-1j) + (2-4j)
       (1+8j) = (2-4j) * (-2+1j) + (1-2j)
       (2-4j) = (1-2j) * 2 + 0
    
    gcd((11+3j), (1+8j)) -> (1-2j)


### The Extended Euclidean Algorithm (xGCD)

**Bezout's Theorem**

Let $\delta$ be the GCD of $\alpha, \beta \in \mathbb{Z}[i]$, then $\delta = \alpha x + \beta y$ for some $x, y \in \mathbb{Z}[i]$.

**Example**


```python
>>> help(Zi.xgcd)
```

    Help on function xgcd in module gaussians:
    
    xgcd(alpha, beta)
        The Extended Euclidean Algorithm for Gaussian Integers.
        
        Three values are returned: gcd, x, & y, such that
        the Greatest Common Divisor (gcd) of alpha & beta can be
        written as gcd = alpha * x + beta * y. x & y are called
        Bézout's coefficients.
    



```python
>>> delta, x, y = Zi.xgcd(alpha, beta)  # Use alpha & beta from above

>>> print(f"alpha = {alpha} and beta = {beta}")
>>> print(f"delta = {delta}, x = {x}, and y = {y}\n")
>>> print(f"==> {alpha * x  + beta * y} = {alpha} * {x} + {beta} * {y}")

>>> print(f"\n  Note: gcd({alpha},{beta}) = {Zi.gcd(alpha, beta)}")
```

    alpha = (11+3j) and beta = (1+8j)
    delta = (1-2j), x = (2-1j), and y = 3j
    
    ==> (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j
    
      Note: gcd((11+3j),(1+8j)) = (1-2j)


### True Division

Let $\alpha, \beta \in \mathbb{Z}[i]$. If $\beta \mid \alpha$ then $\alpha / \beta \in \mathbb{Z}[i]$, otherwise $\alpha / \beta \in \mathbb{Q}[i]$

**Examples**


```python
>>> alpha = Zi(4, 5)
>>> beta = Zi(1, -2)

>>> alpha / beta
```




    Qi('-6/5', '13/5')




```python
>>> print(f"{alpha} / {beta} -> {alpha / beta}")
```

    (4+5j) / (1-2j) -> (-6/5+13/5j)


### Congruence Modulo

Let $\alpha, \beta, \gamma \in \mathbb{Z}[i]$. If $\gamma \ \vert \ (\alpha - \beta)$, then we say that "$\alpha$ is congruent to $\beta$ modulo $\gamma$", written as $\alpha \equiv \beta \text{ mod } \gamma$.

**Examples**


```python
>>> help(Zi.congruent_modulo)
```

    Help on function congruent_modulo in module gaussians:
    
    congruent_modulo(a, b, c)
        This method returns two values: The first value is True or False,
        depending on whether x is congruent to y modulo z;
        the second value is result of computing (a - b) / c.
    



```python
>>> alpha = Zi(1, 12)
>>> beta = Zi(2, -1)
>>> gamma = Zi(3, 1)

>>> print(f"Test Value: ({alpha} - {beta} / {gamma} -> {(alpha - beta) / gamma}\n")

>>> cong, test = Zi.congruent_modulo(alpha, beta, gamma)

>>> print(f"cong = {cong}")
>>> print(f"test = {test}")
```

    Test Value: ((1+12j) - (2-1j) / (3+1j) -> (1+4j)
    
    cong = True
    test = (1+4j)


An example of non-congruence:


```python
>>> delta = Zi(3, 2)
>>> cong, test = Zi.congruent_modulo(alpha, beta, delta)
>>> print(f"cong = {cong}")
>>> print(f"test = {test} is not a Zi")
```

    cong = False
    test = (23/13+41/13j) is not a Zi


### Relatively Prime

Let $\alpha, \beta \in \mathbb{Z}[i]$. If the only factors $\alpha$ and $\beta$ have in common are units (i.e., $1, -1, i, -i$) then they are called *relatively prime*.

**Examples**


```python
>>> help(Zi.is_relatively_prime)
```

    Help on function is_relatively_prime in module gaussians:
    
    is_relatively_prime(a, b) -> bool
        Returns True if a and b are relatively prime, otherwise it returns false.
    



```python
>>> alpha = Zi(4, 5)
>>> alpha_conj  = alpha.conjugate

>>> Zi.is_relatively_prime(alpha, alpha_conj)
```




    True




```python
>>> alpha = Zi(11, 3)
>>> beta = Zi(1, 8)

>>> Zi.is_relatively_prime(alpha, beta)
```




    False



### Gaussian Primes

See [this link for a definition](https://en.wikipedia.org/wiki/Gaussian_integer#Gaussian_primes) of a Gaussian prime, and see [this link for the algorithm](https://mathworld.wolfram.com/GaussianPrime.html) used here to determine whether a Gaussian integer is prime or not.

**Examples**


```python
>>> help(Zi.is_gaussian_prime)
```

    Help on function is_gaussian_prime in module gaussians:
    
    is_gaussian_prime(x) -> bool
        Return True if x is a Gaussian prime.  Otherwise, return False.
        x can be an integer or a Gaussian integer.
        
        See https://mathworld.wolfram.com/GaussianPrime.html
    



```python
>>> gints = [alpha, beta, gamma, Zi(2, 0), Zi(3, 0), Zi(5, 0), Zi(7, 0), Zi(0, 2), Zi(0, 3)]

>>> for gi in gints:
>>>     print(f"Is {gi} a Gaussian prime? {Zi.is_gaussian_prime(gi)}")
```

    Is (11+3j) a Gaussian prime? False
    Is (1+8j) a Gaussian prime? False
    Is (3+1j) a Gaussian prime? False
    Is 2 a Gaussian prime? False
    Is 3 a Gaussian prime? True
    Is 5 a Gaussian prime? False
    Is 7 a Gaussian prime? True
    Is 2j a Gaussian prime? False
    Is 3j a Gaussian prime? True


## Miscellaneous

In addition, the following methods are supported. See the respective doc strings for more information.

* **random** -- Returns a random Gaussian integer
* **associates** -- Returns the three associates of a given Gaussian integer
* **is_associate** -- Returns True if two Gaussian integers are associates
* **to_gaussian_rational** -- Converts a Gaussian integer to an equivalent Gaussian rational
* **norms_divide** -- Returns True if one of two Gaussian integers evenly divides the other
* **from_array** -- Returns a Gaussian integer constructed from a two-element array

## Gaussian Rationals

The implementation of the class of Gaussian rationals, ``Qi``, has constructors, accessors, and arithmetic that is similar to those of the class of Gaussian integers, ``Zi``.

So, only the additions and differences are documented below.

The class ``Qi`` is implemented as a pair of [fractions.Fraction](https://docs.python.org/3/library/fractions.html).


```python
>>> r = Qi(2, 3.4)
>>> s = Qi("4/6", "-1/7")

>>> print(f"{r = }")
>>> print(f"{s = }")
```

    r = Qi('2', '17/5')
    s = Qi('2/3', '-1/7')


### Inverses


```python
>>> r_inv = r.inverse

>>> print(f"{r_inv = }")
```

    r_inv = Qi('50/389', '-85/389')



```python
>>> print(f"{r * r_inv = } = {r * r_inv}")
```

    r * r_inv = Zi(1) = 1


### Floor & Ceiling


```python
>>> print(f"{s = }")
>>> print(f"{floor(s) = }")
>>> print(f"{ceil(s) = }")
```

    s = Qi('2/3', '-1/7')
    floor(s) = Zi(0, -1)
    ceil(s) = Zi(1)


### String to Rational

The statis method ``Qi.string_to_rational`` parses a valid Gaussian rational string and returns the cooresponding ``Qi`` instance.


```python
>>> str(Qi('1/2', '-3/5'))
```




    '(1/2-3/5j)'




```python
>>> Qi.string_to_rational('(1/2-3/5j)')
```




    Qi('1/2', '-3/5')


