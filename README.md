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

## The Modified Division Theorem

For $\alpha, \beta \in \mathbb{Z}[i]$ with $\beta \ne 0$, there are $\gamma, \rho \in \mathbb{Z}[i]$ such that $\alpha = \beta \gamma + \rho$ and $N(\rho) \le (1/2)N(\beta)$.


```python
>>> alpha = Zi(27, -23)
>>> beta = Zi(8, 1)

>>> gamma, rho = Zi.modified_divmod(alpha, beta)

>>> print(f"{beta * gamma + rho} = {beta} * {gamma} + {rho}")

>>> print(f"\nN({rho}) = {rho.norm} and (1/2)N({beta}) = {(1/2) * beta.norm}")
```

    (27-23j) = (8+1j) * (3-3j) + -2j
    
    N(-2j) = 4 and (1/2)N((8+1j)) = 32.5


## The Euclidean Algorithm

Let $\alpha, \beta \in \mathbb{Z}[i]$ be non-zero, then we can recursively apply the Division Theorem to obtain the Greatest Common Divisor (GCD) of $\alpha$ and $\beta$.


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


## Bezout's Theorem

Let $\delta$ be the GCD of $\alpha, \beta \in \mathbb{Z}[i]$, then $\delta = \alpha x + \beta y$ for some $x, y \in \mathbb{Z}[i]$.


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


## True Division

Let $\alpha, \beta \in \mathbb{Z}[i]$. If $\beta \mid \alpha$ then $\alpha / \beta \in \mathbb{Z}[i]$, otherwise $\alpha / \beta \in \mathbb{Q}[i]$


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


## Gaussian Primes

See [this link for a definition](https://en.wikipedia.org/wiki/Gaussian_integer#Gaussian_primes) of a Gaussian prime, and see [this link for the algorithm](https://mathworld.wolfram.com/GaussianPrime.html) used here to determine whether a Gaussian integer is prime or not.


```python
gints = [alpha, beta, gamma, Zi(2, 0), Zi(3, 0), Zi(5, 0), Zi(7, 0), Zi(0, 2), Zi(0, 3)]

for gi in gints:
    print(f"Is {gi} a Gaussian prime? {Zi.is_gaussian_prime(gi)}")
```

    Is (4+5j) a Gaussian prime? True
    Is (1-2j) a Gaussian prime? True
    Is (3-3j) a Gaussian prime? False
    Is 2 a Gaussian prime? False
    Is 3 a Gaussian prime? True
    Is 5 a Gaussian prime? False
    Is 7 a Gaussian prime? True
    Is 2j a Gaussian prime? False
    Is 3j a Gaussian prime? True

