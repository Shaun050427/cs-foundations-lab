"""Timing is measured here, never invented by the web UI."""
import argparse
import json
import platform
import random
import statistics
import sys
import time
from algorithms import insertion_sort, merge_sort


def run(size=1000, repeats=7, seed=42):
    if not 1 <= size <= 10000 or not 3 <= repeats <= 50:
        raise ValueError('size must be 1..10000; repeats must be 3..50')
    rng = random.Random(seed)
    workload = [rng.randrange(-size, size) for _ in range(size)]
    expected = sorted(workload)
    funcs = {'python_insertion': insertion_sort, 'python_merge': merge_sort, 'python_builtin': sorted}
    samples = {key: [] for key in funcs}
    # Warm up and verify each implementation before timing.
    for fn in funcs.values():
        assert fn(workload) == expected
    for repetition in range(repeats):
        # Rotate order; don't always favor the implementation run first/last.
        names = list(funcs)
        names = names[repetition % 3:] + names[:repetition % 3]
        for name in names:
            begin = time.perf_counter_ns()
            output = funcs[name](workload)
            elapsed = time.perf_counter_ns() - begin
            assert output == expected
            samples[name].append(elapsed / 1e6)
    return {'environment': {'python': sys.version, 'platform': platform.platform()},
            'config': {'size': size, 'repeats': repeats, 'seed': seed, 'distribution': 'uniform integers with duplicates'},
            'results': {name: {'raw_ms': values, 'median_ms': statistics.median(values),
                               'min_ms': min(values), 'max_ms': max(values)} for name, values in samples.items()},
            'boundary': 'Different implementation layers: built-in sorting is implemented in C; this is not an isolated algorithm comparison. Data generation and correctness checks are outside timing; list allocation inside functions is included.'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--size', type=int, default=1000)
    parser.add_argument('--repeats', type=int, default=7)
    parser.add_argument('--seed', type=int, default=42)
    args = parser.parse_args()
    print(json.dumps(run(args.size, args.repeats, args.seed), indent=2))
