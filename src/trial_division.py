import time

import numpy as np
from math import log2

import numpy.dtypes

from primes import primes

trial_divisors = primes[:15]

_ris = [1]


def get_fb_representation(b, n, factor_base):
    k = factor_base.shape[0]
    pows = np.zeros(k, dtype=np.int64)
    i = 0
    if factor_base[i] == -1:
        if (t := -b % n) != 0 and t < b:
            pows[i] = 1

        i += 1

    while i < k:
        e = factor_base[i]
        while b % e == 0:
            pows[i] += 1
            b //= e
        i += 1


    if b != 1:
        return None

    return pows


def canonical_by_trial(n, divisors):
    c = np.zeros(len(divisors), dtype=np.int64)
    for i, divisor in enumerate(divisors):
        while n % divisor == 0:
            c[i] += 1
            n //= divisor

    if n != 1:
        return None

    else:
        return c


# extra slow ~ 200 times slower than simply dividing
def trial_division_pascal(n: int, divisors=trial_divisors) -> int | None:
    global _ris
    # We use B = 2
    t = int(log2(n)) + 1

    # Використовується для наступних викликів
    for i in range(len(_ris), t):
        _ris.append(_ris[-1] << 1)

    # Цифри n у двійковій системі
    def ais():
        d = 0
        while d < n.bit_length():
            yield (n & (1 << d)) >> d
            d += 1

    for divisor in divisors:
        s = 0
        for ai, ri in zip(ais(), _ris):
            s += ai * ri
        if s % divisor == 0:
            return divisor

    return None


if __name__ == "__main__":
    print(trial_division_pascal(int(input("N:")), trial_divisors))
