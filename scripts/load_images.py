#!/usr/bin/env python
"""Fetches spell icons from wowhead and uploads them to our S3 bucket.

PYTHONPATH=. uv run scripts/load_images.py 

"""
from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import io
import os

# IMPORT THIRD PARTY LIBRARIES
import boto3
import requests
from PIL import Image

# IMPORT LOCAL LIBRARIES
from lorgs import data
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


def get_images(folder: str) -> list[str]:
    """Retrieve a list of images from the S3 bucket

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


def upload(filname: str) -> None:
    """Download an image from wowhead and upload it to S3.

    Args:
        filename (str): The filename of the image to upload.
    """
    # Download the file from the HTTP URL
    url = f"https://wow.zamimg.com/images/wow/icons/large/{filname}"
    response = requests.get(url)
    if not response:
        response.raise_for_status()

    path = f"{FOLDER}{filname}"

    # upload jpeg to S3
    BUCKET.put_object(
        Body=response.content,
        Key=path,
        ContentType="image/jpeg",
        CacheControl="public, max-age=31536000, immutable",
    )

    # convert jpeg to webp
    webp_data = convert_to_webp(response.content)

    basename, _ = os.path.splitext(filname)
    webp_path = f"{FOLDER}{basename}.webp"

    # upload webp to S3
    BUCKET.put_object(
        Body=webp_data,
        Key=webp_path,
        ContentType="image/webp",
        CacheControl="public, max-age=31536000, immutable",
    )


################################################################################


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
spells: list[WowSpell] = []
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
