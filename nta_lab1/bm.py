from math import sqrt

import numpy as np

from .common import L, legendre
from .primes import primes
from .sle import fastgauss_elimination_solve
from .trial_division import get_fb_representation


def cfrac(n):
    m = sqrt(n)
    v = 1
    alpha = m
    a = int(alpha)
    u = a
    preprev = 0
    prev = 1
    while True:
        ret = a * prev + preprev
        preprev = prev
        prev = ret
        yield ret
        v = (n - u ** 2) // v
        alpha = (m + u) / v
        a = int(alpha)
        u = a * v - u


def brillhart_morrison(n, k=5, attempts=1):
    # Build the factor base
    factor_base = [-1]
    factor_base_size = len(factor_base)

    for prime in primes:
        if factor_base_size >= k or prime > pow(L(n), (1 / sqrt(2))):
            break
        if legendre(n, prime) == 1:
            factor_base.append(prime)
            factor_base_size += 1

    factor_base = np.array(factor_base, dtype=np.int64)
    k = factor_base_size
    cfrac_gen = cfrac(n)

    for _ in range(attempts):
        # Find k+1 b-smooth sqares
        p = 0
        a_b_smooth = np.zeros(k + 1, dtype=np.int64)
        v = np.zeros((k + 1, factor_base_size), dtype=np.int64)
        while p != k + 1:
            a = next(cfrac_gen) % n
            b = (a ** 2) % n
            if (c := get_fb_representation(b, n, factor_base)) is not None:
                v[p] = c
                a_b_smooth[p] = a
                p += 1

        solutions = fastgauss_elimination_solve(v)

        for solution in solutions:
            # sadly, no prod modulo n in numpy...
            x = 1
            for xi in np.power(a_b_smooth, solution):
                x = x * int(xi) % n
            y = 1
            for yi in np.power(factor_base, np.sum(np.multiply(solution, v.transpose()).transpose(), 0) // 2):
                y = y * int(yi) % n

            ## this will produce incorrect result for large n because of overflows
            # x = np.prod(np.power(a_b_smooth, solution)) % n
            # y = np.prod(np.power(factor_base, np.sum(np.multiply(solution, v.transpose()).transpose(),0) // 2)) % n
            # assert (pow(int(x), 2, n) - pow(int(y), 2, n)) % n == 0

            if x == y or x == (-y % n):
                continue
            return int(np.gcd(x + y, n)), int(np.gcd(x - y, n))

    return None


if __name__ == "__main__":
    n = 17873
    n = 100001119
    n = 633209
    print(brillhart_morrison(n, 15))
