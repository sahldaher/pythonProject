import datetime

from pydantic import BaseModel
from bson import  ObjectId
class Reviwes(BaseModel):
    onwer_id: str
    review_on:str
    offer_id:str # ObjectId#house or car or elec or furniture or user
    comment:str | None = None
    rate:int
    created_at:datetime.datetime