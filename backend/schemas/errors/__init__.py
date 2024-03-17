"""typing for APIError"""
from pydantic import BaseModel, Field


class APIError(BaseModel):
    """type for APIError"""
    code: int = Field(...)
    message: str = Field(...)
    request: object
    details: object


class InvalidParametersError(APIError):
    """type for InvalidParametersError"""
    code: int = 400
    message: str = "Invalid parameters provided"


class NotFoundError(APIError):
    """type for NotFoundError"""
    code: int = 404
    message: str = "Specified resource(s) was not found"


class InvalidCreationError(APIError):
    """type for InvalidCreationError"""
    code: int = 422
    message: str = "Unable to create resource"


class InternalCreationError(APIError):
    """type for InternalCreationError"""
    code: int = 500
    message: str = "Internal server error"
