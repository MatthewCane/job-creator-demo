# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "httpx[http2]",
#     "rich",
# ]
# ///

import asyncio
import time
import httpx
from rich.console import Console
from rich.table import Table

console = Console()
console.print("[bold]API Network Benchmark[/bold]\n")

ENDPOINTS = [
    ("GitHub API", "https://api.github.com"),
    ("httpbin delay 1s", "https://httpbin.org/delay/1"),
    ("httpbin delay 1s", "https://httpbin.org/delay/1"),
    ("httpbin delay 1s", "https://httpbin.org/delay/1"),
    ("JSONPlaceholder posts", "https://jsonplaceholder.typicode.com/posts"),
    ("JSONPlaceholder users", "https://jsonplaceholder.typicode.com/users"),
    ("JSONPlaceholder todos", "https://jsonplaceholder.typicode.com/todos"),
    ("IP info", "https://httpbin.org/ip"),
    ("User agent", "https://httpbin.org/user-agent"),
    ("Response headers", "https://httpbin.org/response-headers?X-Job=uv-demo"),
]


async def fetch(client: httpx.AsyncClient, label: str, url: str) -> dict:
    start = time.perf_counter()
    try:
        r = await client.get(url, timeout=15.0)
        elapsed = time.perf_counter() - start
        return {
            "label": label,
            "url": url,
            "status": r.status_code,
            "elapsed": elapsed,
            "bytes": len(r.content),
            "error": None,
        }
    except Exception as e:
        elapsed = time.perf_counter() - start
        return {
            "label": label,
            "url": url,
            "status": None,
            "elapsed": elapsed,
            "bytes": 0,
            "error": str(e),
        }


async def main():
    results_table = Table("Label", "Status", "Size (B)", "Time (s)")

    console.print(f"Firing [bold]{len(ENDPOINTS)}[/bold] requests concurrently...\n")
    wall_start = time.perf_counter()

    async with httpx.AsyncClient(http2=True) as client:
        results = await asyncio.gather(
            *[fetch(client, label, url) for label, url in ENDPOINTS]
        )

    wall_elapsed = time.perf_counter() - wall_start

    total_bytes = 0
    for r in results:
        if r["error"]:
            results_table.add_row(
                r["label"], "[red]ERROR[/red]", "-", f"{r['elapsed']:.2f}"
            )
            console.print(f"  [red]Error for {r['label']}:[/red] {r['error']}")
        else:
            status_str = (
                f"[green]{r['status']}[/green]"
                if r["status"] == 200
                else f"[yellow]{r['status']}[/yellow]"
            )
            results_table.add_row(
                r["label"], status_str, f"{r['bytes']:,}", f"{r['elapsed']:.2f}"
            )
            total_bytes += r["bytes"]

    console.print(results_table)
    console.print(
        f"\nTotal wall time : [bold]{wall_elapsed:.2f}s[/bold]  (sequential would be ~{sum(r['elapsed'] for r in results):.2f}s)"
    )
    console.print(f"Total data      : [bold]{total_bytes:,} bytes[/bold]")


asyncio.run(main())
