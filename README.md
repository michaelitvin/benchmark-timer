# Benchmark Timer

Use the `BenchmarkTimer` class to measure the time it takes to execute some piece of code. \
This gives more flexibility than the built-in timeit function, and runs in the same scope as the rest of your code.

## Installation

```
pip install git+https://github.com/michaelitvin/benchmark-timer.git@main#egg=benchmark-timer
```

## Usage

### Single iteration example
```python
from benchmark_timer import BenchmarkTimer
import time

with BenchmarkTimer(name="MySimpleCode") as tm, tm.single_iteration():
    time.sleep(.3)
```

Output:
```text
Benchmarking MySimpleCode...
MySimpleCode benchmark: n_iters=1 avg=0.300881s std=0.000000s range=[0.300881s~0.300881s]
```

### Multiple iterations example
```python
from benchmark_timer import BenchmarkTimer
import time

with BenchmarkTimer(name="MyTimedCode", print_iters=True) as tm:
    for timing_iteration in tm.iterations(n=5, warmup=2):
        with timing_iteration:
            time.sleep(.1)

print("\n===================\n")
print("List of timings: ", list(tm.timings.values()))
```

Output:
```text
Benchmarking MyTimedCode...
[MyTimedCode] iter=0 took 0.099755s (warmup)
[MyTimedCode] iter=1 took 0.100476s (warmup)
[MyTimedCode] iter=2 took 0.100189s 
[MyTimedCode] iter=3 took 0.099900s 
[MyTimedCode] iter=4 took 0.100888s 
MyTimedCode benchmark: n_iters=3 avg=0.100326s std=0.000414s range=[0.099900s~0.100888s]

===================

List of timings:  [0.10018850000000001, 0.09990049999999995, 0.10088760000000008]
```
