# Lorrgs Assets

This module holds any static Assets, (eg.: Images) used on [lorrgs.io](https://lorrgs.io).  
The files will be uploaded to S3 and cached via CloudFront.

We mostly store any assets strongly related to the `lorrgs.data` here. eg.; Spell- or Boss-Icons,
where the data does have a direct relation to the assets.

This allows adding new spells without updating the frontend repository.

## Where are all the Spell and Boss Icons?

Icons for Spells are loaded dynamically using the `scripts/load_images.py`-script at deploy time.
They will be downloaded from wowhead and uploaded to S3 where they are cached and served from.

## Conversion

There is a lambda function monitoring the S3 Bucket and automatically converting
all uploaded `.jpg`, `.jpeg` and `.png` files to `.webp`.
<insert link to lambda code>

## Notes

S3 Bucket
    name: `assets2.lorrgs.io`
    Static website hosting: enabled

Cloudflare DNS:
    `assets2` -> `lorrgs-assets.s3-website-eu-west-1.amazonaws.com`
