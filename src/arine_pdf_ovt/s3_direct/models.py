from typing import Annotated

from pydantic import BaseModel, Field


class S3DirectRequest(BaseModel):
    bucket: Annotated[str, Field(description="The S3 bucket name.")]
    key: Annotated[str, Field(description="The S3 object key.")]


class S3DirectResponse(BaseModel):
    message: Annotated[str, Field(description="A message indicating the result of the operation.")]
