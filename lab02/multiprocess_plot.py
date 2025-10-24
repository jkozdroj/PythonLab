import math, random, time, csv
from statistics import median
from multiprocessing import Pool, cpu_count
import matplotlib.pyplot as plt

def _merge(L, R):
    i=j=0; out=[]
    while i<len(L) and j<len(R):
        if L[i] <= R[j]: out.append(L[i]); i+=1
        else: out.append(R[j]); j+=1
    out.extend(L[i:]); out.extend(R[j:])
    return out

def merge_sort_seq(a):
    if len(a) <= 1: return a[:]
    m = len(a)//2
    return _merge(merge_sort_seq(a[:m]), merge_sort_seq(a[m:]))

def _chunkify(data, k):
    k = max(1, k)
    size = math.ceil(len(data)/k)
    return [data[i:i+size] for i in range(0, len(data), size)]

def _pairwise_merge(runs):
    while len(runs) > 1:
        nxt=[]
        it = iter(runs)
        for a in it:
            b = next(it, None)
            nxt.append(a if b is None else _merge(a,b))
        runs=nxt
    return runs[0] if runs else []

def parallel_merge_sort(data, processes=None):
    processes = processes or cpu_count()
    chunks = _chunkify(data, processes)
    with Pool(processes) as pool:
        parts = pool.map(merge_sort_seq, chunks)
    return _pairwise_merge(parts)

def time_once(fn, *args, **kw):
    t0=time.perf_counter(); fn(*args, **kw)
    return time.perf_counter()-t0

def benchmark(N_values, P_values, repeats=3, seed=7):
    random.seed(seed)
    base = [random.randint(-1_000_000,1_000_000) for _ in range(max(N_values))]
    rows=[]
    for N in N_values:
        data = base[:N]
        for P in P_values:
            ts=[]
            for _ in range(repeats):
                ts.append(time_once(parallel_merge_sort, list(data), P))
            rows.append({
                "N": N, "processes": P,
                "time_s_median": round(median(ts), 6),
                "time_s_min": round(min(ts), 6),
                "time_s_max": round(max(ts), 6),
                "repeats": repeats
            })
    return rows

if __name__ == "__main__":
    N_values = [8000, 16000, 32000]
    P_values = [1, 2, 4] + ([8] if cpu_count()>=8 else [])
    rows = benchmark(N_values, P_values, repeats=3)

    with open("benchmark.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader(); w.writerows(rows)

    plt.figure(figsize=(8,5))
    for N in N_values:
        xs = [r["processes"] for r in rows if r["N"]==N]
        ys = [r["time_s_median"] for r in rows if r["N"]==N]
        plt.plot(xs, ys, marker="o", label=f"N={N}")
    plt.xlabel("Liczba procesów")
    plt.ylabel("Czas [s] (mediana)")
    plt.title("Parallel merge sort — czas vs liczba procesów")
    plt.legend(); plt.grid(True); plt.tight_layout()
    plt.savefig("benchmark.png", dpi=160)
    plt.show()
