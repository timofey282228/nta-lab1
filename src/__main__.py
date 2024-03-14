import argparse

from miller_rabin import miller_rabin_test
from trial_division import trial_division_pascal
from pollard import pollard_factorization, pollard_floyd, floyd, classic, h
from bm import brillhart_morrison
from functools import partial


def get_pollard_algo(s):
    match s:
        case "classic":
            return classic
        case "floyd":
            return floyd
        case "h":
            return h
        case _:
            return None


def canonical_add(canonical: dict[int, int], p: int):
    if canonical.get(p) is not None:
        canonical[p] += 1
    else:
        canonical[p] = 1


def canonical_to_str(canonical, latex=False):
    return (("$" if latex else "") +
            " {} ".format("\\cdot" if latex else "*").join((str(pr) + "^" + str(po) for pr, po in canonical.items())) +
            ("$" if latex else ""))


def main(args):
    for n in args.n:
        current_n = n
        print(f"Factorizing n = {n}")
        canonical: dict[int, int] = {}  # primes to corresponing powers in the canonnical representation
        is_prime = False

        if miller_rabin_test(n):
            print("Was prime")
            is_prime = True

        while not is_prime and (d := trial_division_pascal(n)) is not None:
            print(f"Found {d} by trial division")
            canonical_add(canonical, d)
            n //= d
            is_prime = miller_rabin_test(n)
            if is_prime:
                print(f"{n} is prime")

        # choosing Polard's rho method modification
        if args.pollard_mod == "floyd_cycle":
            pollard = pollard_floyd
        else:
            pollard = partial(pollard_factorization, f=lambda x: x ** 2 + 1, x0=1, method=get_pollard_algo(args.pollard_mod))

        # Only find one divisor
        if not is_prime and (d := pollard(n)) is not None:
            print(f"Found {d} by Pollard's rho method ({args.pollard_mod})")
            canonical_add(canonical, d)
            n //= d
            is_prime = miller_rabin_test(n, k=args.m)
            if is_prime:
                print(f"{n} is prime")

        while not is_prime and (dd := brillhart_morrison(n, k=args.k, attempts=args.attempts)) is not None:
            print(f"Found {dd[0]} by Brillhart-Morrison's method")
            canonical_add(canonical, dd[0])
            n = int(n) // dd[0]
            is_prime = miller_rabin_test(n)
            if is_prime:
                print(f"{n} is prime")

        if is_prime:
            if n != 1:
                canonical_add(canonical, n)
            print(f"Canonical representation of {current_n}: {canonical_to_str(canonical, latex=args.latex)}")
        else:
            print("Could not fully factorize")
        print()


if __name__ == "__main__":
    argparser = argparse.ArgumentParser(
        description="This program performs factorization of integers using trial division, Pollard's rho method, and Brillhart-Morrison's method."
    )
    argparser.add_argument("n", type=int, action='extend', nargs='+', help="integers to factorize")

    pollard_options = argparser.add_argument_group(title="Pollard's rho", description="Pollard's rho method options")
    pollard_options.add_argument(
        "--pollard_mod", required=False, choices=['classic', 'floyd', 'h', "floyd_cycle"], default="floyd_cycle", action='store',
        help="method of index choosing"
    )

    bm_options = argparser.add_argument_group(title='Brillhart-Morrison', description="Brillhart-Morrison method options")
    bm_options.add_argument("--k", default=7, type=int, help="number of consecutive primes in factorization base")
    bm_options.add_argument(
        "--attempts", default=5, type=int,
        help="maximum attempts with different sets of B-smooth numbers for chosen factorization base"
    )

    primetest_option = argparser.add_argument_group(title="Primality tets", description="Primality tests options")
    primetest_option.add_argument("--m", help="test rounds", default=10, type=int)

    display_options = argparser.add_argument_group(title="Display", description="Display options")
    display_options.add_argument("--latex", action='store_true', help="Output will be printed in latex where appropriate")
    args = argparser.parse_args()
    main(args)
