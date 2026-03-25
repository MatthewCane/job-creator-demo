from pathlib import Path

from src.job_generator import generate_manifests


def main():
    script_path = Path(__file__).parent / "scripts"
    generate_manifests(script_path)


if __name__ == "__main__":
    main()
