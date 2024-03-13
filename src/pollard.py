from math import gcd
from typing import *
from collections.abc import Callable


def classic(j):
    yield from range(0, j)


def floyd(j):
    if j % 2 == 0:
        yield j // 2


def h(j):
    yield 2 ** (j.bit_length() - 1) - 1


def pollard_factorization(
        n: int,
        f: Callable[[int], int],
        x0: int,
        method: Callable[[int], Generator[int, None, None]],
) -> int | None:
    x = [x0]

    # 4stats:
    gcds = 0
    elements = 0

    for j in range(1, n + 1):
        # we won't have more than n different elements anyway
        x.append(f(x[-1]) % n)
        elements += 1

        for k in method(j):
            d = gcd(x[j] - x[k], n)
            gcds += 1

            # collision?
            if d == n:
                return None

            elif d > 1:
                return d

    # we must've checked all pairs possible with the chosen method
    return None


def pollard_floyd(n):
    x = y = 2
    while True:
        x = (pow(x, 2, n) + 1)
        y = pow(pow(y, 2, n) + 1, 2, n) + 1
        if (x - y) % n == 0:
            return None
        if (d := gcd(x - y, n)) != 1:
            return d
