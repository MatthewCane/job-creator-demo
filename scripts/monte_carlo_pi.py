# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "rich",
# ]
# ///

import random
import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn

SAMPLES = 10_000_000

console = Console()

console.print(f"[bold]Monte Carlo Pi Estimation[/bold] — {SAMPLES:,} samples")

inside = 0
start = time.perf_counter()

with Progress(
    SpinnerColumn(),
    "[progress.description]{task.description}",
    TimeElapsedColumn(),
    console=console,
) as progress:
    task = progress.add_task("Sampling...", total=None)
    for _ in range(SAMPLES):
        x = random.random()
        y = random.random()
        if x * x + y * y <= 1.0:
            inside += 1
    progress.update(task, description="Done")

elapsed = time.perf_counter() - start
pi_estimate = 4 * inside / SAMPLES

console.print(f"Estimated pi : [green]{pi_estimate:.6f}[/green]")
console.print(f"Actual pi    : [blue]3.141593[/blue]")
console.print(f"Error        : {abs(pi_estimate - 3.141592653589793):.6f}")
console.print(f"Time         : {elapsed:.2f}s")
