import time


class TimeStats:
    __slots__ = ("checkpoints",)

    def __init__(self):
        self.checkpoints = []
        self.checkpoints.append(time.perf_counter_ns())

    def checkpoint(self):
        self.checkpoints.append(time.perf_counter_ns())
        return " - Last operation took " + str(self.checkpoints[-1] - self.checkpoints[-2]) + " ns"

    def stop(self):
        self.checkpoints.append(time.perf_counter_ns())
        return f"Total runtime: {self.checkpoints[-1] - self.checkpoints[0]} ns"
