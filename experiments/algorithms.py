"""Small reference implementations; Python 3.10+, standard library only."""
from collections import deque


def insertion_sort(values):
    a = list(values)
    for i in range(1, len(a)):
        key, j = a[i], i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a


def merge_sort(values):
    a = list(values)
    width = 1
    while width < len(a):
        for lo in range(0, len(a), 2 * width):
            mid, hi = min(lo + width, len(a)), min(lo + 2 * width, len(a))
            left, right = a[lo:mid], a[mid:hi]
            i = j = 0
            for k in range(lo, hi):
                if j == len(right) or (i < len(left) and left[i] <= right[j]):
                    a[k] = left[i]
                    i += 1
                else:
                    a[k] = right[j]
                    j += 1
        width *= 2
    return a


def lower_bound(a, target):
    """First index with a[index] >= target; assumes ascending input."""
    lo, hi = 0, len(a)
    while lo < hi:
        mid = lo + (hi - lo) // 2
        if a[mid] < target:
            lo = mid + 1
        else:
            hi = mid
    return lo


def bfs_distances(adj, start):
    distances = {start: 0}
    queue = deque([start])
    while queue:
        node = queue.popleft()
        for neighbor in adj[node]:
            if neighbor not in distances:
                distances[neighbor] = distances[node] + 1
                queue.append(neighbor)
    return distances
