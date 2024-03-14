# Gaussian Integers and Gaussian Rational Numbers

This module defines two classes, **Zi** and **Qi**, the Gaussian integers and Gaussian rational numbers, respectively.

In mathematical notation, the integers are denoted by $\mathbb{Z}$, the rational numbers by $\mathbb{Q}$, and the complex numbers by $\mathbb{C}$.

The **Gaussian integers** are defined as $\mathbb{Z}[i] = \lbrace a + bi: a, b \in \mathbb{Z} \rbrace$,

and the **Gaussian rationals** are defined as $\mathbb{Q}[i] = \lbrace r + si: r, s \in \mathbb{Q} \rbrace$.

For detailed information, see the two Jupyter notebooks in the notebooks directory.

For a quick look, see the examples following this plot of Gaussian primes.

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

