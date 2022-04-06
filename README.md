# Benchmark Timer

Use the `BenchmarkTimer` class to measure the time it takes to execute some piece of code. \
This gives more flexibility than the built-in timeit function, and runs in the same scope as the rest of your code.


```python
from benchmark_timer import BenchmarkTimer
import time

with BenchmarkTimer(name="MyTimedCode", print_iters=True) as tm:
    for timing_iteration in tm.iterations(n=5):
        with timing_iteration:
            time.sleep(.1)

print("\nList of timings: ", list(tm.timings.values()))
```

Output:
```text
Benchmarking MyTimedCode...
[MyTimedCode] iter=0 took 0.099844s
[MyTimedCode] iter=1 took 0.100076s
[MyTimedCode] iter=2 took 0.100837s
[MyTimedCode] iter=3 took 0.100112s
[MyTimedCode] iter=4 took 0.100256s
MyTimedCode benchmark: n_iters=5 avg=0.100225s std=0.000333s min=0.099844s max=0.100837s

List of timings:  [0.0998444, 0.1000763, 0.10083749999999997, 0.10011230000000004, 0.10025640000000002]
```
