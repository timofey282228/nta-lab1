from .miller_rabin import *
from .pollard import pollard_floyd
from .trial_division import *
from .bm import brillhart_morrison


def canonical_add(canonical: dict[int, int], p: int):
    if canonical.get(p) is not None:
        canonical[p] += 1
    else:
        canonical[p] = 1


def canonical(n, k=7, attempts=5, m=10):
    prime_test = miller_rabin_test

    current_n = n
    canonical: dict[int, int] = {}  # primes to corresponing powers in the canonical representation
    is_prime = False

    if prime_test(n, k=m):
        is_prime = True

    while not is_prime and (d := trial_division_pascal(n)) is not None:
        canonical_add(canonical, d)
        n //= d
        is_prime = prime_test(n, k=m)

    pollard = pollard_floyd

    # Only find one divisor
    if not is_prime and (d := pollard(n)) is not None:
        canonical_add(canonical, d)
        n //= d
        is_prime = prime_test(n, k=m)

    while not is_prime and (dd := brillhart_morrison(n, k=k, attempts=attempts)) is not None:
        canonical_add(canonical, dd[0])
        n = int(n) // dd[0]
        is_prime = prime_test(n, k=m)

    if is_prime:
        if n != 1:
            canonical_add(canonical, n)
        return canonical
    else:
        return None
