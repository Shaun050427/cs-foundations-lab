/* Equal work: sequential vs shuffled pointer traversal.
 * cc -O2 -std=c11 -Wall -Wextra -pedantic experiments/locality.c -o locality
 * ./locality 1048576 7
 * The model is not a literal linked-node allocator: one shuffled successor array
 * isolates access order; both loops perform n dependent successor reads per run.
 */
#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <time.h>
#include <errno.h>
#include <inttypes.h>

static uint32_t seed = 42;
static uint32_t random32(void) { seed = seed * 1664525u + 1013904223u; return seed; }
static int parse(const char *s, size_t *out) {
    char *end = NULL; errno = 0;
    unsigned long long value = strtoull(s, &end, 10);
    if (errno || !end || *end || end == s || *s == '-' || value > SIZE_MAX) return 0;
    *out = (size_t)value; return 1;
}
static double now_seconds(void) {
    struct timespec ts;
    if (timespec_get(&ts, TIME_UTC) != TIME_UTC) { fputs("clock failed\n", stderr); exit(1); }
    return (double)ts.tv_sec + (double)ts.tv_nsec / 1e9;
}
static uint64_t walk(const uint32_t *next, size_t n, uint32_t start) {
    uint64_t sum = 0; uint32_t node = start;
    for (size_t i = 0; i < n; ++i) { sum += node; node = next[node]; }
    return sum;
}
int main(int argc, char **argv) {
    size_t n = 1048576, repeats = 7;
    if (argc > 3 || (argc > 1 && !parse(argv[1], &n)) || (argc > 2 && !parse(argv[2], &repeats)) || n < 2 || n > 16777216 || repeats < 3 || repeats > 50) {
        fputs("usage: locality [n=2..16777216] [repeats=3..50]\n", stderr); return 1;
    }
    uint32_t *ordered = malloc(n * sizeof(*ordered)), *random_next = malloc(n * sizeof(*random_next)), *permutation = malloc(n * sizeof(*permutation));
    if (!ordered || !random_next || !permutation) { free(ordered); free(random_next); free(permutation); fputs("allocation failed\n", stderr); return 1; }
    for (size_t i = 0; i < n; ++i) { ordered[i] = (uint32_t)((i + 1) % n); permutation[i] = (uint32_t)i; }
    for (size_t i = n - 1; i > 0; --i) { size_t j = random32() % (i + 1); uint32_t v = permutation[i]; permutation[i] = permutation[j]; permutation[j] = v; }
    for (size_t i = 0; i < n; ++i) random_next[permutation[i]] = permutation[(i + 1) % n];
    uint64_t expected = (uint64_t)n * (n - 1) / 2;
    if (walk(ordered, n, 0) != expected || walk(random_next, n, permutation[0]) != expected) { fputs("warmup checksum failed\n", stderr); return 2; }
    printf("compiler=%s; seed=42; n=%zu; repeats=%zu; clock=TIME_UTC (wall clock)\n", __VERSION__, n, repeats);
    puts("run,pattern,seconds,checksum");
    for (size_t rep = 0; rep < repeats; ++rep) for (size_t trial = 0; trial < 2; ++trial) {
        int shuffled = (int)((trial + rep) % 2); double begin = now_seconds();
        uint64_t sum = walk(shuffled ? random_next : ordered, n, shuffled ? permutation[0] : 0);
        double elapsed = now_seconds() - begin;
        if (sum != expected || elapsed < 0) { fputs("checksum or clock validation failed\n", stderr); return 2; }
        printf("%zu,%s,%.9f,%" PRIu64 "\n", rep, shuffled ? "shuffled" : "sequential", elapsed, sum);
    }
    free(ordered); free(random_next); free(permutation); return 0;
}
