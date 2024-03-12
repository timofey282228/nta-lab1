import numpy as np

from itertools import chain
from miller_rabin import miller_rabin_test
from trial_division import trial_division_pascal
from pollard import pollard_factorization, floyd
from bm import brillhart_morrison


def canonical_add(canonical: dict[int, int], p: int):
    if canonical.get(p) is not None:
        canonical[p] += 1
    else:
        canonical[p] = 1


def do_factorize(n):
    print(f"Factorizing n = {n}")
    n_bak = n
    canonical: dict[int, int] = {}  # primes to corresponing powers in the canonnical representation
    is_prime = False

    if miller_rabin_test(n):
        print("Was prime")
        is_prime = True
        canonical[n] = 1

    while (d := trial_division_pascal(n)) is not None and not is_prime:
        print(f"Found {d} by trial division")
        canonical_add(canonical, d)
        n //= d
        is_prime = miller_rabin_test(n)
        if is_prime:
            print(f"{n} is prime")

    while (
            (
                    d := pollard_factorization(
                        n, lambda x: x ** 2 + 1, 1, floyd
                    )
            ) is not None and not is_prime
    ):
        print(f"Found {d} by pollard method")
        canonical_add(canonical, d)
        n //= d
        is_prime = miller_rabin_test(n)
        if is_prime:
            print(f"{n} is prime")

    while (
            (
                    d := brillhart_morrison(
                        n
                    )
            ) is not None and not is_prime
    ):
        print(f"Found {d} by brillhart-morrisoon method")
        canonical_add(canonical, d)
        n //= d
        is_prime = miller_rabin_test(n)
        if is_prime:
            print(f"{n} is prime")

    canonical_add(canonical, n)

    if n != 1 and not is_prime:
        print("Could not fully factorize")
    else:
        print(f"Canonical representation of {n}: {canonical}")

    # TODO remove sanity check
    ren = 1
    for prime, power in canonical.items():
        ren = ren * pow(prime, power)

    assert ren == n_bak


if __name__ == "__main__":
    byvar = [
        901667173167834173,
        323324583518541583,
        2500744714570633849,
        691534156424661573,
        1184056490329830239,
        1449863225586482579,
        778320232076288167,
        1515475730401555091,
        341012868237902669,
        7442109405582674149,
    ]

    alltasks = [
        3009182572376191,
        1021514194991569,
        4000852962116741,
        15196946347083,
        499664789704823,
        269322119833303,
        679321846483919,
        96267366284849,
        61333127792637,
        2485021628404193,
    ]
    for n in chain(byvar, alltasks):
        do_factorize(n)
