# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
# ]
# ///

import time
from rich.console import Console
from rich.table import Table

console = Console()
console.print("[bold]Sieve of Eratosthenes[/bold]")

results = Table("Limit", "Primes found", "Largest prime", "Time (s)")


def sieve(limit: int) -> list[int]:
    is_prime = bytearray([1]) * (limit + 1)
    is_prime[0] = is_prime[1] = 0
    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            is_prime[i * i :: i] = bytearray(len(is_prime[i * i :: i]))
    return [i for i, v in enumerate(is_prime) if v]


for limit in [1_000_000, 5_000_000, 10_000_000, 50_000_000]:
    start = time.perf_counter()
    primes = sieve(limit)
    elapsed = time.perf_counter() - start
    results.add_row(
        f"{limit:,}",
        f"{len(primes):,}",
        f"{primes[-1]:,}",
        f"{elapsed:.3f}",
    )
    console.print(f"  Sieve up to {limit:,} done in {elapsed:.3f}s")

console.print(results)
