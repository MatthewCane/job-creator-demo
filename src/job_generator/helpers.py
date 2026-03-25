from pathlib import Path


def del_dir(path: Path):
    for p in path.iterdir():
        if p.is_dir():
            del_dir(p)
            p.rmdir()
        else:
            p.unlink()
