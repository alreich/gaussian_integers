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

# Quick Look

The examples below are from ["The Gaussian Integers"](https://kconrad.math.uconn.edu/blurbs/ugradnumthy/Zinotes.pdf) by Keith Conrad


```python
>>> from gaussians import Zi, Qi
```

## The Division Theorem


```python
>>> alpha = Zi(27, -23)
>>> beta = Zi(8, 1)

>>> quot, rem = Zi.modified_divmod(alpha, beta)

>>> print(f"{beta * quot + rem} = {beta} * {quot} + {rem}")
```

    (27-23j) = (8+1j) * (3-3j) + -2j


## The Euclidean Algorithm


```python
>>> alpha = Zi(11, 3)
>>> beta = Zi(1, 8)

>>> gcd = Zi.gcd(alpha, beta, verbose=True)  # Prints intermediate results

>>> print(f"\ngcd({alpha}, {beta}) -> {gcd}")
```

       (11+3j) = (1+8j) * (1-1j) + (2-4j)
       (1+8j) = (2-4j) * (-2+1j) + (1-2j)
       (2-4j) = (1-2j) * (2+0j) + 0j
    
    gcd((11+3j), (1+8j)) -> (1-2j)


## Bezout's Theorem


```python
>>> a, x, y = Zi.xgcd(alpha, beta)

>>> print(f"a = {a}")
>>> print(f"{alpha * x  + beta * y} = {alpha} * {x} + {beta} * {y}")
```

    a = (1-2j)
    (1-2j) = (11+3j) * (2-1j) + (1+8j) * 3j


## True Division

If $\alpha, \beta \in \mathbb{Z}[i]$, then ${\large \frac{\alpha}{\beta}} \in \mathbb{Q}[i]$


```python
>>> a = Zi(4, 5)
>>> b = Zi(1, -2)
>>> a / b
```




    Qi('-6/5', '13/5')




```python
>>> print(f"{a} / {b} -> {a / b}")
```

    (4+5j) / (1-2j) -> (-6/5+13/5j)

