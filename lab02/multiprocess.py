

import os
import random
import time
import math
from multiprocessing import Pool, cpu_count

# ---------- Sekwencyjny merge sort (bez wbudowanego sortowania) ----------
def _merge(left, right):
    i = j = 0
    out = []
    len_l, len_r = len(left), len(right)
    while i < len_l and j < len_r:
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    if i < len_l:
        out.extend(left[i:])
    if j < len_r:
        out.extend(right[j:])
    return out

def merge_sort_seq(arr):
    n = len(arr)
    if n <= 1:
        return arr[:]
    mid = n // 2
    left = merge_sort_seq(arr[:mid])
    right = merge_sort_seq(arr[mid:])
    return _merge(left, right)

# ---------- Narzędzia do dzielenia i scalania ----------
def _chunkify(data, k):

    n = len(data)
    if k <= 0:
        k = 1
    size = math.ceil(n / k)
    return [data[i:i+size] for i in range(0, n, size)]

def _pairwise_merge(runs):

    while len(runs) > 1:
        merged = []
        it = iter(runs)
        for a in it:
            try:
                b = next(it)
            except StopIteration:
                merged.append(a)
                break
            merged.append(_merge(a, b))
        runs = merged
    return runs[0] if runs else []

# ---------- Równoległe sortowanie ----------
def parallel_merge_sort(data, processes=None):

    if processes is None:
        processes = cpu_count()

    if len(data) == 0:
        return []

    chunks = _chunkify(data, processes)
    with Pool(processes=processes) as pool:
        sorted_chunks = pool.map(merge_sort_seq, chunks)

    return _pairwise_merge(sorted_chunks)

# ---------- Demo / Pomiar ----------
if __name__ == "__main__":
    try:
        N = int(input("Podaj N (liczba elementów do posortowania): ").strip())
    except ValueError:
        N = 200_000
        print("Niepoprawne N — przyjęto N =", N)

    try:
        P = input(f"Podaj liczbę procesów [Enter = auto ({cpu_count()})]: ").strip()
        processes = int(P) if P else None
    except ValueError:
        processes = None

    random.seed(42)
    data = [random.randint(-1_000_000, 1_000_000) for _ in range(N)]

    # Równoległe sortowanie
    t0 = time.perf_counter()
    sorted_parallel = parallel_merge_sort(data, processes=processes)
    t1 = time.perf_counter()

    # Sekwencyjna weryfikacja (naszym merge sortem, nie built-in)
    t2 = time.perf_counter()
    sorted_seq = merge_sort_seq(data)
    t3 = time.perf_counter()

    ok = (sorted_parallel == sorted_seq)

    print("\n=== Podsumowanie ===")
    print(f"Liczba elementów: {N}")
    print(f"Procesów        : {processes if processes else cpu_count()} (auto)")
    print(f"Czas równoległy : {t1 - t0:.3f} s")
    print(f"Czas sekwencyjny: {t3 - t2:.3f} s")
    print(f"Zgodność wyników: {'TAK' if ok else 'NIE'}")

