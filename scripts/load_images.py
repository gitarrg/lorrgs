#!/usr/bin/env -S PYTHONPATH=. uv run --env-file=.env
"""Uploads spell icons and spec images to our S3 bucket.

Spell icons are fetched from wowhead. Spec images are read from `lorrgs_assets/images/specs/`.
Only images missing in the bucket are uploaded.

PYTHONPATH=. uv run scripts/load_images.py

"""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import importlib
import io
import os
import pathlib

# IMPORT THIRD PARTY LIBRARIES
import boto3
import requests
from PIL import Image

# IMPORT LOCAL LIBRARIES
from lorgs import game_version
from lorgs.models.raid_boss import RaidBoss
from lorgs.models.raid_zone import RaidZone
from lorgs.models.wow_potion import WowPotion
from lorgs.models.wow_spell import WowSpell
from lorgs.models.wow_trinket import WowTrinket


# S3_CLIENT = boto3.client("s3")
S3 = boto3.resource("s3")


BUCKET_NAME = os.getenv("BUCKET_NAME", "assets2.lorrgs.io")
BUCKET = S3.Bucket(BUCKET_NAME)


FOLDER = "images/spells/"
SPECS_FOLDER = "images/specs/"
LOCAL_SPECS_FOLDER = pathlib.Path(__file__).parent.parent / "lorrgs_assets" / "images" / "specs"


def get_images(folder: str) -> list[str]:
    """Retrieve a list of images from the S3 bucket.

    Args:
        folder (str): The folder path in the S3 bucket.

    Returns:
        list[str]: List of image filenames.

    """
    images = [obj.key for obj in BUCKET.objects.filter(Prefix=folder)]
    images = [img for img in images if not img.endswith(".webp")]
    images = [img[len(folder) :] for img in images]
    return images


def convert_to_webp(data: bytes) -> bytes:
    image = Image.open(io.BytesIO(data))
    buffer = io.BytesIO()
    image.save(buffer, format="webp")
    return buffer.getvalue()


def upload_image(data: bytes, folder: str, filename: str) -> None:
    """Upload a jpeg to S3, plus a webp version of it.

    Args:
        data (bytes): The jpeg image data.
        folder (str): The folder path in the S3 bucket.
        filename (str): The jpeg filename.

    """
    # upload jpeg to S3
    BUCKET.put_object(
        Body=data,
        Key=f"{folder}{filename}",
        ContentType="image/jpeg",
        CacheControl="public, max-age=31536000, immutable",
    )

    # convert jpeg to webp
    webp_data = convert_to_webp(data)

    webp_path = pathlib.Path(folder) / filename
    webp_path = webp_path.with_suffix(".webp")

    # upload webp to S3
    BUCKET.put_object(
        Body=webp_data,
        Key=webp_path.as_posix(),
        ContentType="image/webp",
        CacheControl="public, max-age=31536000, immutable",
    )


def upload(filename: str) -> None:
    """Download a spell icon from wowhead and upload it to S3.

    Args:
        filename (str): The filename of the image to upload.

    """
    # Download the file from the HTTP URL
    url = f"https://wow.zamimg.com/images/wow/icons/large/{filename}"
    response = requests.get(url)
    if not response:
        response.raise_for_status()

    upload_image(response.content, FOLDER, filename)


def upload_spec_images() -> None:
    """Upload the local spec images missing in the S3 bucket."""
    existing = set(get_images(SPECS_FOLDER))

    for path in sorted(LOCAL_SPECS_FOLDER.glob("*.jpg")):
        if path.name in existing:
            continue

        print(f"uploading: {path.name}")
        upload_image(path.read_bytes(), SPECS_FOLDER, path.name)


################################################################################


# Register the game data of every Game Version (not just the active one).
# Icons live in one shared folder, so we want the icons of all of them.
for _game_version in game_version.GAME_VERSIONS.values():
    importlib.import_module(_game_version.data_package)

# Get existing images in the S3 bucket
images = get_images(FOLDER)

# list of all the "types" of Spells
# TODO: find a way to create this dynamically?
spell_types: set[type[WowSpell | RaidBoss | RaidZone]] = {
    WowSpell,
    WowTrinket,
    WowPotion,
    # not actual "Spell" subclasses... but lets go with this for now
    RaidBoss,
    RaidZone,
}


# Retrieve all spells
spells: list[WowSpell | RaidBoss | RaidZone] = []
for spell_type in spell_types:
    spells += spell_type.list()


for spell in spells:
    icon = spell.icon

    if not icon:
        print(f"spell: {spell} has no icon.")
        continue

    # check if already uploaded
    if icon in images:
        continue

    print(f"uploading: {icon} for {spell.name}")
    upload(icon)


# Upload the Spec images
upload_spec_images()
