"""Client to store Objects in DynamoDB."""

from __future__ import annotations

# IMPORT STANDARD LIBRARIES
import decimal
import json
import typing

# IMPORT THIRD PARTY LIBRARIES
import boto3
from boto3.dynamodb.conditions import Attr

# IMPORT LOCAL LIBRARIES
from lorgs.logger import Timer
from lorgs.models.base import base


if typing.TYPE_CHECKING:
    from mypy_boto3_dynamodb.service_resource import Table


dynamodb = boto3.resource("dynamodb")


TBaseModel = typing.TypeVar("TBaseModel", bound="DynamoDBModel")


class DynamoDBModel(base.BaseModel):
    pkey_name: typing.ClassVar[str] = "pk"
    skey_name: typing.ClassVar[str] = "sk"
    pkey: typing.ClassVar[str] = "{id}"
    skey: typing.ClassVar[str] = ""

    @classmethod
    def get_table(cls) -> "Table":
        return dynamodb.Table(cls.get_table_name())

    @classmethod
    def get_keys(cls, **kwargs) -> dict[str, str]:
        keys = {cls.pkey_name: cls.pkey.format(**kwargs)}
        if cls.skey_name and cls.skey:
            keys[cls.skey_name] = cls.skey.format(**kwargs)
        return keys

    ############################################################################
    # Get from DB
    #

    @classmethod
    def get(cls: typing.Type[TBaseModel], **kwargs: typing.Any) -> TBaseModel | None:
        table = cls.get_table()
        keys = cls.get_keys(**kwargs)

        with Timer(f"GET: {kwargs}"):
            response = table.get_item(Key=keys)
        try:
            item = response["Item"]
        except KeyError:
            return None

        with Timer(f"PARSE: {kwargs}"):
            return cls(**item)

    @classmethod
    def first(cls: typing.Type[TBaseModel], **kwargs: typing.Any) -> TBaseModel | None:
        """Returns the first Item matching the given keywords."""

        table = cls.get_table()

        if not kwargs:
            raise ValueError("Need to provide some search arguments.")

        expr = None
        for name, value in kwargs.items():
            attr = Attr(name).eq(value)
            if not expr:
                expr = attr
            else:
                expr = expr & attr

        response = table.scan(FilterExpression=expr)  # type: ignore
        items = response["Items"]
        if not items:
            return None

        item = items[0]
        return cls(**item)

    ############################################################################
    # Save to DB
    #

    def json_dict(self, exclude_unset: bool = True) -> dict[str, typing.Any]:
        # convert into json compatible dict
        # this back and fort serialization makes sure all complex objects
        # are converted into json compatible formats.
        # There is some work done to simplify this: https://github.com/pydantic/pydantic/discussions/4456
        return json.loads(  # type: ignore
            self.model_dump_json(exclude_unset=exclude_unset, by_alias=True),
            parse_float=decimal.Decimal,  # dynamodb wants floats as decimals
        )

    def save(self, exclude_unset: bool = True) -> None:
        data = self.json_dict(exclude_unset=exclude_unset)

        # insert the keys
        keys = self.get_keys(**data)
        data.update(keys)

        # save
        table = self.get_table()
        table.put_item(Item=data)
