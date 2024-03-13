import numpy as np
from itertools import chain


def fastgauss_elimination_solve(a):
    """
    :param a: An NxM array of vectors (will be taken modulo 2)
    :return: a binary vector of length M of solutions
    """
    a = np.mod(a, 2)
    n, m = a.shape
    marked_rows = set()
    for j in range(m):
        i = None

        # linear search for 1 in column j
        for k in range(n):
            if a[k, j] != 0:
                i = k
                break

        if i is not None:
            marked_rows.add(i)
            for k in chain(range(j), range(j + 1, m)):
                if a[i, k] == 1:
                    a[:, k] = (a[:, j] + a[:, k]) % 2

    for i in range(n):
        if i not in marked_rows and any(a[i]):
            # solution vector
            x = np.zeros(n, dtype=np.bool_)
            x[i] = 1

            # current undetermined vector
            v = a[i]
            for l in chain(range(i), range(i + 1, n)):
                if (a[l] & v).any():
                    x[l] = 1
                    # update current undetermined vector
                    v = (v + a[l]) % 2

                # if we have solved the system - move on to the next undetermined vector
                if not any(v):
                    yield x
                    break
