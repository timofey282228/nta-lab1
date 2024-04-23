import argparse
import time

from miller_rabin import miller_rabin_test
from trial_division import trial_division_pascal
from solovay_strassen import solovay_strassen
from pollard import pollard_factorization, pollard_floyd, floyd, classic, h
from bm import brillhart_morrison
from functools import partial
from timestats import TimeStats


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


def get_primetest(s):
    match s:
        case "miller-rabin":
            return miller_rabin_test
        case "solovay-strassen":
            return solovay_strassen


def canonical_add(canonical: dict[int, int], p: int):
    if canonical.get(p) is not None:
        canonical[p] += 1
    else:
        canonical[p] = 1


def canonical_to_str(canonical, latex=False):
    return (("$" if latex else "") +
            " {} ".format("\\cdot" if latex else "*").join(
                (str(pr) + "^" + ("{" if latex else "") + str(po) + ("}" if latex else "") for pr, po in canonical.items())
            ) +
            ("$" if latex else ""))


def select_pollard(args):
    # choosing Polard's rho method modification
    if args.pollard_mod == "floyd_cycle":
        return pollard_floyd
    else:
        return partial(pollard_factorization, f=lambda x: x ** 2 + 1, x0=1, method=get_pollard_algo(args.pollard_mod))


def main(args):
    if args.algospeed:
        algospeed(args)
    else:
        factorize(args)


def factorize(args):
    prime_test = get_primetest(args.prime_test)

    for n in args.n:
        if n < 0:
            print(f"Please provide n > 0 (n = {n} < 0)")
            continue

        stats = TimeStats()
        current_n = n
        print(f"Factorizing n = {n}")
        canonical: dict[int, int] = {}  # primes to corresponing powers in the canonical representation
        is_prime = False

        if prime_test(n, k=args.m):
            print("Was prime")
            print(stats.checkpoint())
            is_prime = True

        while not is_prime and (d := trial_division_pascal(n)) is not None:
            print(f"Found {d} by trial division")
            print(stats.checkpoint())
            canonical_add(canonical, d)
            n //= d
            is_prime = prime_test(n)
            if is_prime:
                print(f"{n} is prime")
                print(stats.checkpoint())

        pollard = select_pollard(args)

        # Only find one divisor
        if not is_prime and (d := pollard(n)) is not None:
            print(f"Found {d} by Pollard's rho method ({args.pollard_mod})")
            print(stats.checkpoint())
            canonical_add(canonical, d)
            n //= d
            is_prime = prime_test(n, k=args.m)
            if is_prime:
                print(f"{n} is prime")
                print(stats.checkpoint())

        while not is_prime and (dd := brillhart_morrison(n, k=args.k, attempts=args.attempts)) is not None:
            print(f"Found {dd[0]} by Brillhart-Morrison's method")
            print(stats.checkpoint())
            canonical_add(canonical, dd[0])
            n = int(n) // dd[0]
            is_prime = prime_test(n, k=args.m)
            if is_prime:
                print(f"{n} is prime")
                print(stats.checkpoint())

        if is_prime:
            if n != 1:
                canonical_add(canonical, n)
            print(f"Canonical representation of {current_n}: {canonical_to_str(canonical, latex=args.latex)}")
        else:
            print("Could not fully factorize")

        print(stats.stop())
        print()


def algospeed(args):
    algos = {
        # "Pascal trial division": trial_division_pascal,
        "Pollard's rho method with Floyd's cycle finding": pollard_floyd,
        "Pollard's rho method (classic)": partial(pollard_factorization, f=lambda x: x ** 2 + 1, x0=1, method=classic),
        "Pollard's rho method (floyd)": partial(pollard_factorization, f=lambda x: x ** 2 + 1, x0=1, method=floyd),
        "Pollard's rho method (h)": partial(pollard_factorization, f=lambda x: x ** 2 + 1, x0=1, method=h),
        "Brillhart-Morrison's method": None
    }

    def bm(n):
        d = brillhart_morrison(n, k=args.k, attempts=args.attempts)
        if d is not None:
            return d[0]
        else:
            return None

    algos["Brillhart-Morrison's method"] = bm

    for n in args.n:
        if n < 0:
            print(f"Please provide n > 0 (n = {n} < 0)")
            continue

        if args.latex:
            print(r"\begin{{table}}[h]\caption{{{}}}\begin{{tabular}}{{l|cr}}".format(n))
        else:
            print(f"Benchmarking on {n}")

        header = ("Algorithm name", "Found divisor", "Execution time (µs)")
        if args.latex:
            print(
                " & ".join(header) + " \\\\"
            )
        else:
            print(
                "\t".join(header)
            )

        for algo_name, algo_func in algos.items():
            t = time.perf_counter_ns()
            d = algo_func(n)
            t = (time.perf_counter_ns() - t) / 1000
            row = (algo_name, str(d) if d is not None else "-", "{t:.1f}".format(t=t))
            if args.latex:
                print(
                    " & ".join(row) + " \\\\"
                )
            else:
                print(
                    "\t".join(row)
                )
        if args.latex:
            print(r"\end{tabular}\end{table}")
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
    bm_options.add_argument("-k", default=7, type=int, help="number of consecutive primes in factorization base")
    bm_options.add_argument(
        "--attempts", default=5, type=int,
        help="maximum attempts with different sets of B-smooth numbers for chosen factorization base"
    )

    primetest_option = argparser.add_argument_group(title="Primality test", description="Primality tests options")
    primetest_option.add_argument(
        "--prime_test", choices=['miller-rabin', 'solovay-strassen'], help="test algorithm", default="miller-rabin"
    )
    primetest_option.add_argument("-m", help="test rounds", default=10, type=int)

    display_options = argparser.add_argument_group(title="Display", description="Display options")
    display_options.add_argument("--latex", action='store_true', help="Output will be printed in latex where appropriate")

    algospeed_options = argparser.add_argument_group(title="Algorithm speed comparison")
    algospeed_options.add_argument(
        "--algospeed",
        action="store_true",
        help="Run each available factorization algorithm once for each n, find one divisor and print stats"
    )

    args = argparser.parse_args()
    main(args)
