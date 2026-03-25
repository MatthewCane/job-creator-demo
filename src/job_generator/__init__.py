from pathlib import Path

from cdk8s import App, YamlOutputType
from rich import print

from src.job_generator.helpers import del_dir
from src.job_generator.job_spec import JobSpec


def generate_manifests(scripts_path: Path):
    app = App(yaml_output_type=YamlOutputType.FILE_PER_RESOURCE)

    for script_path in scripts_path.glob("*.py"):
        JobSpec(
            app,
            f"{script_path.stem.replace('_', '-')}",
            script=script_path.read_text(),
        )

    output_dir = Path(Path.cwd(), app.outdir).resolve()
    del_dir(output_dir)

    app.synth()
    print(f"Resources synthed to {output_dir}")
