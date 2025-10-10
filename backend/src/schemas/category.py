from pydantic import BaseModel, ConfigDict, Field
from datetime import date, datetime
from typing import Optional


class AddCategory(BaseModel):
    category_name: str
    icon: str | None


class UpdateCategory(BaseModel):
    category_name: str | None
    icon: str | None


class ResponseCategory(BaseModel):
    id: int
    category_name: str
    icon: str
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class ResponseUserCategory(BaseModel):
    message: str
    user_category: ResponseCategory

    model_config = ConfigDict(from_attributes=True)
