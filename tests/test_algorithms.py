import bisect
import random
import sys
import unittest
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'experiments'))
from algorithms import insertion_sort, merge_sort, lower_bound, bfs_distances

class Algorithms(unittest.TestCase):
    def test_generated_sorting_and_boundaries(self):
        rng = random.Random(42)
        arrays = [[], [1], [1, 1], [5, 4, 3], [-1, 0, -8]]
        arrays += [[rng.randrange(-20, 20) for _ in range(rng.randrange(100))] for _ in range(100)]
        for a in arrays:
            original = list(a)
            for sort in [insertion_sort, merge_sort]:
                self.assertEqual(sort(a), sorted(a))
                self.assertEqual(a, original)
    def test_lower_bound_oracle(self):
        rng = random.Random(99)
        for _ in range(100):
            a = sorted(rng.randrange(20) for _ in range(rng.randrange(50)))
            for target in range(-2, 22):
                self.assertEqual(lower_bound(a, target), bisect.bisect_left(a, target))
    def test_bfs_distance_and_disconnection(self):
        self.assertEqual(bfs_distances([[1, 2], [0, 3], [0, 3], [1, 2], []], 0), {0: 0, 1: 1, 2: 1, 3: 2})

if __name__ == '__main__':
    unittest.main()
