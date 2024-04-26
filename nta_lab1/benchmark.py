import argparse
import secrets
import threading
import time

import matplotlib.pyplot as plt
from matplotlib.pyplot import rcParams

from .solovay_strassen import solovay_strassen


def benchmark(args):
    x_1 = []
    x_2 = []
    y_1 = []
    y_2 = []
    not_factorized = []

    threading.excepthook = lambda args: None

    for i in range(1, 64):
        for n in range(10):
            # r = int.from_bytes(random.randbytes(i))
            while (r := secrets.randbits(i)) == 0:
                pass

            print(r)

            s = time.perf_counter_ns()
            # for squares
            try:
                d = solovay_strassen(r, k=40)
            except (ZeroDivisionError, ValueError):
                continue
            s = time.perf_counter_ns() - s

            if d is not None:
                # d = d[0]
                pass
            else:
                not_factorized.append(n)
                continue

            if d:
                x_1.append(r.bit_length())
                y_1.append(s)
            else:
                x_2.append(r.bit_length())
                y_2.append(s)

    subplots = plt.subplots()
    fig: plt.Figure = subplots[0]
    fig.add_gridspec(1, 3)
    ax: plt.Axes = subplots[1]
    ax.grid(which='both', axis='y', linewidth=0.1)
    ax.set_title('Триваліcть тесту Соловея-Штрассена, 40 раундів')
    ax.set_xlabel('Бітова довжина')
    ax.set_ylabel('Час, мкс')
    ax.scatter(x_1, list(map(lambda y: y / 1000, y_1)), label='Просте', s=(rcParams['lines.markersize'] ** 2) // 10)
    ax.scatter(
        x_2, list(map(lambda y: y / 1000, y_2)), label='Складене', c=(1, 0, 0), s=(rcParams['lines.markersize'] ** 2) // 10
        )
    ax.set(xlim=(1, 64))
    ax.minorticks_on()
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels)
    plt.show()
    # plt.savefig('../report/img/bm_benchmark')


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()

    args = argparser.parse_args()
    benchmark(args)
