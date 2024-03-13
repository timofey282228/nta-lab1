from math import exp, log, sqrt


def L(n):
    return exp(sqrt(log(n) * log(log(n))))


def legendre(a, p):
    return pow(a, (p - 1) // 2, p) % 5


import time


def measure_performance(func, n, *args, **kwargs):
    s = time.perf_counter_ns()
    for i in range(n):
        func(*args, **kwargs)
    ss = time.perf_counter_ns()

    return ss - s
