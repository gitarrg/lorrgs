"""Lambda code and layers, built locally (no Docker)."""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import hashlib
import pathlib
import shutil
import subprocess  # ruff: ignore[suspicious-subprocess-import]
import typing

# IMPORT THIRD-PARTY LIBRARIES
import aws_cdk as cdk
import jsii
from aws_cdk import aws_lambda as lambda_


REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


@jsii.implements(cdk.ILocalBundling)
class LocalBundling:
    def __init__(self, build: typing.Callable[[pathlib.Path], None]) -> None:
        self.build = build

    def try_bundle(self, output_dir: str, options: cdk.BundlingOptions) -> bool:
        self.build(pathlib.Path(output_dir))
        return True


def bundle(source: pathlib.Path, build: typing.Callable[[pathlib.Path], None], **kwargs) -> lambda_.Code:
    """An asset made by `build(output_dir)`, identified by a hash of `source`."""
    return lambda_.Code.from_asset(
        str(source),
        exclude=["__pycache__"],
        bundling=cdk.BundlingOptions(image=lambda_.Runtime.PYTHON_3_13.bundling_image, local=LocalBundling(build)),
        **kwargs,
    )


def copy_package(package: str, target: pathlib.Path) -> None:
    shutil.copytree(REPO_ROOT / package, target / package, ignore=shutil.ignore_patterns("__pycache__"))


def package_code(package: str) -> lambda_.Code:
    """Lambda code: `package` at the root of the zip."""
    return bundle(REPO_ROOT / package, lambda out: copy_package(package, out))


def package_layer(package: str) -> lambda_.Code:
    """Layer with `package` (layers import from `python/`)."""
    return bundle(REPO_ROOT / package, lambda out: copy_package(package, out / "python"))


def requirements_layer() -> lambda_.Code:
    """Layer with the dependencies from `uv.lock`, for the arm64 runtime."""

    def build(out: pathlib.Path) -> None:
        reqs = out / "requirements.txt"
        subprocess.check_call([  # ruff: ignore[start-process-with-partial-path, subprocess-without-shell-equals-true]
            "uv", "export",
            "--no-dev", "--no-emit-project",
            "--no-hashes", "-q",
            "-o", reqs,
        ],
        )
        subprocess.check_call([  # ruff: ignore[start-process-with-partial-path, subprocess-without-shell-equals-true]
            "uv", "pip", "install",
            "-q", "-r", reqs,
            "--target", out / "python",
            "--python-platform", "aarch64-manylinux2014",
            "--python-version", "3.13",
            "--only-binary", ":all:",
        ])
        reqs.unlink()

    lock_hash = hashlib.sha256((REPO_ROOT / "uv.lock").read_bytes()).hexdigest()
    return bundle(REPO_ROOT, build, asset_hash_type=cdk.AssetHashType.CUSTOM, asset_hash=lock_hash)
