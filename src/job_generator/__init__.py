from pathlib import Path
from typing import Optional

import cdk8s_plus_33 as k_plus
from cdk8s import App, Chart, Duration, YamlOutputType
from constructs import Construct
from rich import print


class JobSpec(Chart):
    def __init__(
        self,
        scope: Construct,
        id: str,
        script: str,
        env: Optional[dict[str, str]] = None,
    ):
        super().__init__(scope, id)

        config_map = k_plus.ConfigMap(
            self,
            id,
            data={"script.py": script},
        )

        script_volume = k_plus.Volume.from_config_map(
            self, "script-volume", config_map=config_map
        )

        cache_volume = k_plus.Volume.from_empty_dir(self, "root-volume", name="root")

        job = k_plus.Job(
            self,
            "job",
            ttl_after_finished=Duration.seconds(10),
        )

        container = job.add_container(
            image="ghcr.io/astral-sh/uv:alpine",
            command=["uv", "run", "/script/script.py"],
            security_context=k_plus.ContainerSecurityContextProps(
                ensure_non_root=False
            ),
            volume_mounts=[
                k_plus.VolumeMount(volume=script_volume, path="/script"),
                k_plus.VolumeMount(volume=cache_volume, path="/root"),
            ],
        )

        for name, value in (env or {}).items():
            container.env.add_variable(name, k_plus.EnvValue.from_value(value))


def __del_dir(path: Path):
    for p in path.iterdir():
        if p.is_dir():
            __del_dir(p)
            p.rmdir()
        else:
            p.unlink()


def generate_manifests(scripts_path: Path):
    app = App(yaml_output_type=YamlOutputType.FILE_PER_RESOURCE)

    for script_path in scripts_path.glob("*.py"):
        JobSpec(
            app,
            f"{script_path.stem.replace('_', '-')}",
            script=script_path.read_text(),
        )

    output_dir = Path(Path.cwd(), app.outdir).resolve()
    __del_dir(output_dir)

    app.synth()
    print(f"Resources synthed to {output_dir}")
