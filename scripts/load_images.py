#!/usr/bin/env -S PYTHONPATH=. uv run --env-file=.env
"""Uploads spell icons, talent icons and spec images to our S3 bucket.

Spell and talent icons are fetched from wowhead. Spec images are read from `lorrgs_assets/images/specs/`.
Only images missing in the bucket are uploaded.

PYTHONPATH=. uv run scripts/load_images.py

"""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import io
import os
import pathlib
import typing

# IMPORT THIRD PARTY LIBRARIES
import boto3
import requests
from PIL import Image

# IMPORT LOCAL LIBRARIES
from lorgs import utils
from lorgs.data import GAME_VERSIONS, talent_trees


if typing.TYPE_CHECKING:
    from lorgs.models.raid_boss import RaidBoss
    from lorgs.models.raid_zone import RaidZone
    from lorgs.models.wow_spell import WowSpell


# S3_CLIENT = boto3.client("s3")
S3 = boto3.resource("s3")


BUCKET_NAME = os.getenv("BUCKET_NAME", "assets2.lorrgs.io")
BUCKET = S3.Bucket(BUCKET_NAME)


FOLDER = "images/spells/"
SPECS_FOLDER = "images/specs/"
LOCAL_SPECS_FOLDER = pathlib.Path(__file__).parent.parent / "lorrgs_assets" / "images" / "specs"


EXTRA_ICONS = [
    "ability_marksmanship.jpg",  # used for "Talents"
]


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
    response = requests.get(url, timeout=30)
    if not response:
        response.raise_for_status()

    upload_image(response.content, FOLDER, filename)


def get_talent_icons() -> set[str]:
    """Icons of every talent (see `scripts/generate_talent_trees.py`)."""
    return {
        entry["icon"]
        for tree in talent_trees.load_spec_trees().values()
        for node in tree["nodes"]
        for entry in node["entries"]
        if entry["icon"]
    }


def upload_spec_images() -> None:
    """Upload the local spec images missing in the S3 bucket."""
    existing = set(get_images(SPECS_FOLDER))

    for path in sorted(LOCAL_SPECS_FOLDER.glob("*.jpg")):
        if path.name in existing:
            continue

        print(f"uploading: {path.name}")
        upload_image(path.read_bytes(), SPECS_FOLDER, path.name)


################################################################################


# Get existing images in the S3 bucket
images = get_images(FOLDER)

# Icons live in one shared folder, so we want the icons of every Game Version.
spells: list[WowSpell | RaidBoss | RaidZone] = []
for _game_version in GAME_VERSIONS.values():
    game_data = _game_version.data
    spells += game_data.spells
    spells += game_data.trinkets
    # not actual "Spell" subclasses... but lets go with this for now
    spells += game_data.bosses
    spells += game_data.zones
spells = utils.uniqify(spells)


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
    images.append(icon)


# Talent icons share the folder with the spell icons
for icon in sorted(get_talent_icons()):
    if icon in images:
        continue

    print(f"uploading: {icon} for Talents")
    upload(icon)
    images.append(icon)

for extra_icon in EXTRA_ICONS:
    print(f"uploading: {extra_icon} for Talents")
    upload(extra_icon)


# Upload the Spec images
upload_spec_images()
