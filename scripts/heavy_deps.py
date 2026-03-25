# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "boto3",
#     "celery",
#     "fastapi",
#     "httpx[http2]",
#     "numpy",
#     "opentelemetry-sdk",
#     "opentelemetry-exporter-otlp",
#     "pandas",
#     "polars",
#     "psutil",
#     "pydantic",
#     "pymongo",
#     "pytest",
#     "redis",
#     "rich",
#     "scipy",
#     "sqlalchemy",
#     "typer",
#     "uvicorn",
# ]
# ///

import importlib
import sys
import time

from rich.console import Console
from rich.table import Table

console = Console()
console.print("[bold]Dependency Load Test[/bold]")
console.print(f"Python {sys.version}\n")

PACKAGES = [
    ("boto3", "boto3"),
    ("celery", "celery"),
    ("fastapi", "fastapi"),
    ("httpx", "httpx"),
    ("numpy", "numpy"),
    ("opentelemetry-sdk", "opentelemetry.sdk.trace"),
    ("pandas", "pandas"),
    ("polars", "polars"),
    ("psutil", "psutil"),
    ("pydantic", "pydantic"),
    ("pymongo", "pymongo"),
    ("pytest", "pytest"),
    ("redis", "redis"),
    ("rich", "rich"),
    ("scipy", "scipy"),
    ("sqlalchemy", "sqlalchemy"),
    ("typer", "typer"),
    ("uvicorn", "uvicorn"),
]

results = Table("Package", "Version", "Import time (s)", "Status")

total_start = time.perf_counter()

for pkg_name, module_name in PACKAGES:
    start = time.perf_counter()
    try:
        mod = importlib.import_module(module_name)
        elapsed = time.perf_counter() - start
        version = getattr(mod, "__version__", "?")
        results.add_row(pkg_name, str(version), f"{elapsed:.3f}", "[green]OK[/green]")
    except Exception as e:
        elapsed = time.perf_counter() - start
        results.add_row(pkg_name, "-", f"{elapsed:.3f}", f"[red]FAIL: {e}[/red]")

total_elapsed = time.perf_counter() - total_start

console.print(results)
console.print(
    f"\nImported [bold]{len(PACKAGES)}[/bold] packages in [bold]{total_elapsed:.2f}s[/bold]"
)
