import random


def jacobi(a, n):
    assert (n > a > 0 and n % 2 == 1)
    s = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                s = -s
        a, n = n, a
        if a % 4 == 3 and n % 4 == 3:
            s = -s
        a %= n
    return s if n == 1 else 0


def solovay_strassen(n, k=10):
    if n == 2:
        return True
    if n < 2 or n % 2 == 0:
        return False
    for _ in range(k):
        a = random.randrange(2, n - 1)
        x = pow(a, (n - 1) // 2, n)
        j = (n + jacobi(a, n)) % n
        if x == 0 or x != j:
            return False
    return True
