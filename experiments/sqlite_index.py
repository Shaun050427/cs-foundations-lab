"""Synthetic data, independent correctness checks and query plan inspection."""
import json
import random
import sqlite3
import statistics
import time


def run(n=50000, repeats=7):
    rng = random.Random(42)
    rows = [(i, rng.randrange(1000), rng.randrange(1, 10000)) for i in range(n)]
    expected = sum(row[2] for row in rows if row[1] == 42)
    connection = sqlite3.connect(':memory:')
    connection.execute('CREATE TABLE events (id INTEGER, bucket INTEGER, amount INTEGER)')
    connection.executemany('INSERT INTO events VALUES (?, ?, ?)', rows)
    connection.commit()
    query = 'SELECT SUM(amount) FROM events WHERE bucket = ?'
    output = {'sqlite_version': sqlite3.sqlite_version, 'size': n, 'seed': 42, 'results': {}}
    for use_index in (False, True):
        if use_index:
            connection.execute('CREATE INDEX bucket_idx ON events(bucket)')
        plan = list(connection.execute('EXPLAIN QUERY PLAN ' + query, (42,)))
        assert connection.execute(query, (42,)).fetchone()[0] == expected
        samples = []
        for _ in range(repeats):
            begin = time.perf_counter_ns()
            answer = connection.execute(query, (42,)).fetchone()[0]
            samples.append((time.perf_counter_ns() - begin) / 1e6)
            assert answer == expected
        output['results']['indexed' if use_index else 'scan'] = {'plan': plan, 'raw_ms': samples, 'median_ms': statistics.median(samples)}
    connection.close()
    output['boundary'] = 'In-memory synthetic SQLite database, selective bucket query, warm cache; excludes index construction and write maintenance. Does not measure disk I/O or guarantee index benefit on other queries.'
    return output


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
