#!/usr/bin/env python
"""Small Script to automate the Deployment.

I've spend a good amount of time trying to get serverless configured the way I
want but never quite god it exactly as I wanted.

"""
import glob
import hashlib
import io
import os
import shutil
import subprocess
import typing

import boto3


if typing.TYPE_CHECKING:
    from mypy_boto3_lambda.type_defs import LayerVersionsListItemTypeDef, PublishLayerVersionResponseTypeDef


LAMBDA_CLIENT = boto3.client("lambda")
S3_CLIENT = boto3.client("s3")
LAMBDA_FUNCTION_UPDATED_WAITER = LAMBDA_CLIENT.get_waiter("function_updated")


# SETTINGS
DEPLOY_BUCKET = os.getenv("DEPLOY_BUCKET") or "lorrgs-code"

DEPLOY_DIR = "./.deploy"


PREFIX = os.getenv("DEPLOY_PREFIX") or ""


################################################################################
# Utils
#


def calc_checksum(path) -> str:
    """Calc an MD5 Checksum for a given path."""
    hash = hashlib.md5()

    for filepath in glob.glob(path, recursive=True):
        with open(filepath, "rb") as f:
            hash.update(f.read())

    return hash.hexdigest()


def zip_folder(src: str, tar: str) -> str:
    """Zip the content from `src` to `tar`."""
    zip_file = shutil.make_archive("tmp_zip", "zip", base_dir=src)
    return shutil.move(zip_file, tar)  # type: ignore


def checksum_compare(name: str, files: str, s3bucket=DEPLOY_BUCKET) -> bool:
    """Compare the Checksum of `files` with an prev. version stored on S3.

    Returns True if they are the same.
    """
    # fetch old checksum
    try:
        old_obj = S3_CLIENT.get_object(Bucket=s3bucket, Key=f"{name}.md5")
    except S3_CLIENT.exceptions.NoSuchKey:
        old_sha = ""
    else:
        body = old_obj.get("Body")
        old_sha = body.read().decode("utf-8") if body else ""

    # calc new checksum
    new_sha = calc_checksum(files)

    # cache latest
    if old_sha != new_sha:
        print(name, "has changed", old_sha, ">", new_sha)
        S3_CLIENT.put_object(Bucket=s3bucket, Key=f"{name}.md5", Body=io.BytesIO(new_sha.encode("utf-8")))
    else:
        print(name, "did not change. :)")

    return old_sha == new_sha


################################################################################


class LambdaLayer:
    def __init__(self, name: str, src_dir: str = "") -> None:
        self.name = name
        self.src_dir = src_dir or self.name

        self.latest_version: typing.Union[
            "LayerVersionsListItemTypeDef", "PublishLayerVersionResponseTypeDef", None
        ] = None

    @property
    def full_name(self) -> str:
        return f"{PREFIX}{self.name}"

    def get_versions(self, max=50) -> list["LayerVersionsListItemTypeDef"]:
        """List all versions for a given Lambda."""
        response = LAMBDA_CLIENT.list_layer_versions(LayerName=self.full_name, MaxItems=max)
        return response.get("LayerVersions") or []

    def get_latest_version_arn(self) -> str:
        if not self.latest_version:
            versions = self.get_versions(max=1)
            if not versions:
                raise ValueError(f"Layer: {self.full_name} has no versions.")
            self.latest_version = versions[0]
        return self.latest_version.get("LayerVersionArn") or ""

    def delete_layer_versions(self) -> None:
        """Deplete all version for a given Lambda."""
        for layer_version in self.get_versions():
            version = layer_version.get("Version")
            if version:
                LAMBDA_CLIENT.delete_layer_version(LayerName=self.full_name, VersionNumber=version)
                print(f"deleting {self.full_name}.{version}")

    def deploy_version(self, path: str) -> "PublishLayerVersionResponseTypeDef":
        zip_file = shutil.make_archive(base_name=path, format="zip", root_dir=path)
        S3_CLIENT.upload_file(zip_file, DEPLOY_BUCKET, f"{self.full_name}.zip")
        self.latest_version = LAMBDA_CLIENT.publish_layer_version(
            LayerName=self.full_name,
            Content={
                "S3Bucket": DEPLOY_BUCKET,
                "S3Key": f"{self.full_name}.zip",
            },
        )
        return self.latest_version

    def deploy(self) -> None:
        """Deploy a Lambda Layer."""
        if checksum_compare(name=self.full_name, files=f"{self.src_dir}/**/*.py"):
            return None

        path = f"{DEPLOY_DIR}/{self.full_name}"
        shutil.copytree(self.src_dir, f"{path}/python/{self.src_dir}")
        self.delete_layer_versions()
        self.deploy_version(path)


class RequirementsLayer(LambdaLayer):
    GENERATED_REQUIREMENTS = f"{DEPLOY_DIR}/requirements.txt"

    def __init__(self, name: str = "requirements") -> None:
        super().__init__(name=name)

    def _export_requirements(self) -> str:
        """Generate a requirements.txt from pyproject.toml / uv.lock."""
        subprocess.check_call(
            [
                "uv",
                "export",
                "--no-annotate",
                "--no-dev",
                "--no-emit-project",
                "--no-hashes",
                "--no-header",
                "-o",
                self.GENERATED_REQUIREMENTS,
            ]
        )
        return self.GENERATED_REQUIREMENTS

    def deploy(self) -> None:
        """Deploy a Lambda layer using dependencies from pyproject.toml."""
        reqs = self._export_requirements()
        if checksum_compare(name=self.full_name, files=reqs):
            return

        path = f"{DEPLOY_DIR}/{self.full_name}"

        subprocess.call(
            [
                "uv",
                "run",
                "pip",
                "install",
                "--platform=manylinux2014_aarch64",
                "--only-binary=:all:",
                "-r", reqs,
                f"--target={path}/python",
            ]
        )
        self.delete_layer_versions()
        self.deploy_version(path)


class Lambda:
    def __init__(self, name: str) -> None:
        self.client = LAMBDA_CLIENT
        self.name = name

    @property
    def full_name(self):
        return f"{PREFIX}{self.name}"

    def deploy(self, src: str = "") -> None:
        """Update the Lambda with `name` to use the Code found in `src`."""
        src = src or self.name.replace("-", "_")
        if checksum_compare(name=self.full_name, files=f"{src}/**/*.py"):
            return

        # zip
        zip_file = zip_folder(src=src, tar=f"{DEPLOY_DIR}/{self.full_name}.zip")

        # upload and update
        S3_CLIENT.upload_file(zip_file, DEPLOY_BUCKET, f"{self.full_name}.zip")
        LAMBDA_CLIENT.update_function_code(
            FunctionName=self.full_name, S3Bucket=DEPLOY_BUCKET, S3Key=f"{self.full_name}.zip"
        )

        # Wait for the update to complete
        print("[deploy_lambda]", self.full_name, "waiting...")
        LAMBDA_FUNCTION_UPDATED_WAITER.wait(FunctionName=self.full_name, WaiterConfig={"Delay": 2})
        print("[deploy_lambda]", self.full_name, "Done!")

    def update_used_layers(self, *layers: LambdaLayer, force=False) -> None:
        """Update the given Lambdas to use the latest version of each Layer."""

        needs_update = force or any(layer.latest_version for layer in layers)
        if not needs_update:
            return

        arns = [layer.get_latest_version_arn() for layer in layers]
        print("Updating Layers for", self.name, arns)
        LAMBDA_CLIENT.update_function_configuration(FunctionName=self.full_name, Layers=arns)


################################################################################


def main() -> None:
    """Deploy everything."""
    if os.path.exists(DEPLOY_DIR):
        shutil.rmtree(DEPLOY_DIR)
    os.mkdir(DEPLOY_DIR)

    # Layers
    core_layer = LambdaLayer("lorrgs-core", src_dir="lorgs")
    core_layer.deploy()

    reqs_layer = RequirementsLayer(name="lorrgs-requirements")
    reqs_layer.deploy()

    # Lambdas
    api_lambda = Lambda(name="lorrgs-api")
    api_lambda.deploy()

    sqs_lambda = Lambda(name="lorrgs-sqs")
    sqs_lambda.deploy()

    # Update if one of them got deployed
    api_lambda.update_used_layers(reqs_layer, core_layer)
    sqs_lambda.update_used_layers(reqs_layer, core_layer)
    return


if __name__ == "__main__":
    main()
