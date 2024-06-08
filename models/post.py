import datetime

from pydantic import BaseModel ,Field,EmailStr
from .address import Address
from typing import List
class Post(BaseModel):
    owner_id: str
    title:str
    description:str  | None = Field(default=None,title="description of items",max_length=500)
    address: Address
    location:str | None = None
    capacity:int | None = None
    price_by_day:float = Field(gt=0,description="the price must be greater than zero")
    images:List[str]
    note:str | None = None
    craeted_at : datetime.datetime



