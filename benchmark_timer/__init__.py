import itertools
import time
from collections import defaultdict

import numpy as np


class BenchmarkTimer:
    """
    Use this class to measure the time it takes to execute some piece of code.
    This gives more flexibility than the built-in timeit function, and runs in the same scope as the rest of your code.
    See demo() for a usage example.
    """

    def __init__(self,
                 name: str = "Timing",
                 print_summary: bool = True,
                 print_iters: bool = False,
                 summary_fmt: str = "{name} benchmark: n_iters={n} avg={avg:.6f}s std={std:.6f}s "
                                    "range=[{p0:.6f}s~{p100:.6f}s]",
                 iters_fmt: str = "[{name}] iter={i} took {total_seconds:.6f}s {warmup_str}",
                 ):
        self.timings = defaultdict(float)
        self._summary_fmt = summary_fmt
        self._iters_fmt = iters_fmt
        self._name = name
        self._print_iters = print_iters
        self._print_summary = print_summary
        self._last_unprinted_tmi = None
        self._used = False

    class TimingIteration:
        def __init__(self, timer: "BenchmarkTimer", i: int, is_warmup: bool = False):
            self._timer = timer
            self.i = i
            self.start_time = None
            self.end_time = None
            self.is_warmup = is_warmup

        def __enter__(self):
            self.start_time = time.perf_counter()

        def __exit__(self, exc_type, exc_val, exc_tb):
            self.end_time = time.perf_counter()
            if not self.is_warmup:
                self._timer.timings[self.i] += self.total_seconds()

        def total_seconds(self):
            return self.end_time - self.start_time

    def iterations(self, n=None, warmup=0):
        assert not self._used
        self._used = True
        iter_counter = itertools.count() if n is None else range(n)
        for i in iter_counter:
            self._last_unprinted_tmi = self.TimingIteration(self, i, i < warmup)
            yield self._last_unprinted_tmi
            self._print_last_tmi_in_need_be()

    def single_iteration(self):
        assert not self._used
        self._used = True
        self._last_unprinted_tmi = self.TimingIteration(self, 0)
        return self._last_unprinted_tmi

    def _print_last_tmi_in_need_be(self):
        if self._print_iters and self._last_unprinted_tmi is not None:
            s = self._iters_fmt.format(name=self._name,
                                       i=self._last_unprinted_tmi.i,
                                       total_seconds=self._last_unprinted_tmi.total_seconds(),
                                       warmup_str='(warmup)' if self._last_unprinted_tmi.is_warmup else '')
            print(s)
            self._last_unprinted_tmi = None

    def __enter__(self):
        if self._print_summary:
            print(f"Benchmarking {self._name}...")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._print_last_tmi_in_need_be()
        if self._print_summary:
            tms = list(self.timings.values())
            s = self._summary_fmt.format(name=self._name,
                                         n=len(tms),
                                         avg=np.mean(tms),
                                         std=np.std(tms),
                                         **{f'p{i}': np.percentile(tms, i) for i in range(0, 101, 10)})
            print(s)


def demo():
    with BenchmarkTimer(name="MySimpleCode") as tm, tm.single_iteration():
        time.sleep(.3)
    print("\n===================\n")

    with BenchmarkTimer(name="MyTimedCode", print_iters=True) as tm:
        for timing_iteration in tm.iterations(n=5, warmup=2):
            with timing_iteration:
                time.sleep(.1)
    print("\n===================\n")

    print("List of timings: ", list(tm.timings.values()))


if __name__ == '__main__':
    demo()
