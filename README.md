# Benchmark Timer

Use the `BenchmarkTimer` class to measure the time it takes to execute some piece of code. \
This gives more flexibility than the built-in timeit function, and runs in the same scope as the rest of your code.

## Installation

```
pip install git+https://github.com/michaelitvin/benchmark-timer.git@main#egg=benchmark-timer
```

## Usage

```python
from benchmark_timer import BenchmarkTimer
import time

with BenchmarkTimer(name="MySimpleCode") as tm, tm.single_iteration():
    time.sleep(.3)
print("\n===================\n")

with BenchmarkTimer(name="MyTimedCode", print_iters=True) as tm:
    for timing_iteration in tm.iterations(n=5):
        with timing_iteration:
            time.sleep(.1)
print("\n===================\n")

print("List of timings: ", list(tm.timings.values()))
```

Output:
```text
Benchmarking MySimpleCode...
MySimpleCode benchmark: n_iters=1 avg=0.300168s std=0.000000s min=0.300168s max=0.300168s

===================

Benchmarking MyTimedCode...
[MyTimedCode] iter=0 took 0.099941s
[MyTimedCode] iter=1 took 0.100527s
[MyTimedCode] iter=2 took 0.100607s
[MyTimedCode] iter=3 took 0.100326s
[MyTimedCode] iter=4 took 0.100550s
MyTimedCode benchmark: n_iters=5 avg=0.100390s std=0.000244s min=0.099941s max=0.100607s

===================

List of timings:  [0.09994119999999995, 0.10052709999999998, 0.100607, 0.10032560000000001, 0.10055029999999998]
```
