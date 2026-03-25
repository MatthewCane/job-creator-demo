# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
#     "rich",
# ]
# ///

import time
import numpy as np
from rich.console import Console
from rich.table import Table

console = Console()
console.print("[bold]NumPy Matrix Benchmark[/bold]")

results = Table("Operation", "Size", "Time (s)", "GFLOP/s")


def bench(label, size, fn):
    start = time.perf_counter()
    fn()
    elapsed = time.perf_counter() - start
    # matrix multiply: 2*N^3 flops
    gflops = (2 * size**3) / elapsed / 1e9
    results.add_row(label, f"{size}x{size}", f"{elapsed:.3f}", f"{gflops:.2f}")


N = 2048

# Matrix multiply
A = np.random.rand(N, N).astype(np.float64)
B = np.random.rand(N, N).astype(np.float64)
bench("matmul (float64)", N, lambda: np.dot(A, B))

A32 = A.astype(np.float32)
B32 = B.astype(np.float32)
bench("matmul (float32)", N, lambda: np.dot(A32, B32))

# SVD (expensive)
M = np.random.rand(1024, 1024).astype(np.float64)
start = time.perf_counter()
U, S, Vt = np.linalg.svd(M, full_matrices=False)
svd_time = time.perf_counter() - start
results.add_row("SVD", "1024x1024", f"{svd_time:.3f}", "-")

# Eigenvalues
E = np.random.rand(512, 512).astype(np.float64)
E = E + E.T  # make symmetric
start = time.perf_counter()
vals = np.linalg.eigvalsh(E)
eig_time = time.perf_counter() - start
results.add_row("eigvalsh", "512x512", f"{eig_time:.3f}", "-")

console.print(results)
console.print(f"NumPy {np.__version__} | BLAS: {np.show_config.__module__}")
