from typing import Annotated

from pydantic import BaseModel, Field


class OptimizeDirectRequest(BaseModel):
    bucket: Annotated[str, Field(description="The S3 bucket name.")]
    key: Annotated[str, Field(description="The S3 object key.")]
    dpi: Annotated[int, Field(default=600, description="The DPI for image downsampling. Default is 600.")]


class OptimizeDirectResponse(BaseModel):
    message: Annotated[str, Field(description="A message indicating the result of the operation.")]
