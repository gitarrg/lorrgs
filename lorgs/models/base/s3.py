"""Store Objects in S3."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import json
import os
from typing import Any, ClassVar, Self, TypeVar

# IMPORT THIRD PARTY LIBRARIES
import boto3
from botocore.exceptions import ClientError

# IMPORT LOCAL LIBRARIES
from lorgs.logger import Timer
from lorgs.models.base import base


T = TypeVar("T", bound="S3Model")


s3client = boto3.client("s3")


class S3Model(base.BaseModel):
    bucket: ClassVar[str] = os.getenv("DATA_BUCKET") or "lorrgs"

    @classmethod
    def get_key(cls, **kwargs) -> str:
        """S3 key, namespaced by the `game_version` (name) of the item."""
        key = super().get_key(**kwargs)
        table_name = cls.get_table_name()
        return f"{kwargs['game_version']}/{table_name}/{key}"

    ############################################################################
    # S3: in/out
    #

    @classmethod
    def get_json(cls, **kwargs: Any) -> Any:
        key = cls.get_key(**kwargs)
        try:
            with Timer(f"s3.get_raw: {key}"):
                data = s3client.get_object(Bucket=cls.bucket, Key=key)
        except ClientError:
            raise KeyError("Invalid Key: %s", key)

        body = data["Body"]
        return json.loads(body.read())

    @classmethod
    def get(cls, **kwargs: Any) -> Self | None:
        """Get an Item from the Store."""
        try:
            content = cls.get_json(**kwargs)
        except KeyError:
            return None

        # TODO: arrg, 04.01.2023
        # We'd pref to use `model_construct` here as its a lot faster than `__init__`
        # Unfortunetly however we need to recurisvely construct child models,
        # which is not supported with `model_construct` as of right now.
        # We could solve this by implementing our own: `model_construct` that
        # somehow handles the creation of child models.
        return cls(**content)

    def save(self, exclude_unset=True, **kwargs: Any) -> None:
        key = self.get_key(**dict(self))
        data = self.model_dump_json(
            exclude_unset=exclude_unset,
            by_alias=True,
            **kwargs,
        )
        s3client.put_object(
            Bucket=self.bucket,
            Key=key,
            Body=data,
            ContentType="application/json",
        )
