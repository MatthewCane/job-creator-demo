# job-creator-demo

A code generation tool that produces Kubernetes `Job` manifests from plain Python scripts.

Drop a [PEP 723](https://peps.python.org/pep-0723/) Python script (with an inline `# /// script` dependency block) into `scripts/`, run the synthesiser, and get a ready-to-apply Kubernetes YAML manifest in `dist/`.

Each generated manifest contains:
- A **ConfigMap** holding the script source code
- A **`batch/v1` Job** that mounts the ConfigMap and runs the script via `ghcr.io/astral-sh/uv:alpine`, which handles dependency resolution at runtime.

## Prerequisites

- Python 3.13
- [`uv`](https://github.com/astral-sh/uv)
- [`just`](https://github.com/casey/just) (optional)
- A Kubernetes cluster accessible via `kubectl`

## Usage

**Install dependencies:**
```bash
uv sync
```

**Synthesise manifests** (reads `scripts/`, writes to `dist/`):
```bash
just synth
# or: uv run main.py
```

**Deploy to Kubernetes:**
```bash
just deploy
# or: kubectl apply -f dist/ --namespace test-ns
```

## Adding your own scripts

Add any PEP 723-compatible Python script to `scripts/` and re-run `just synth`. No changes to `main.py` required.

```python
# /// script
# requires-python = ">=3.12"
# dependencies = ["requests", "rich"]
# ///

import requests
# ...
```
