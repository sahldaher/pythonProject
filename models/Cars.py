from pydantic import BaseModel
from .post import Post
from bson import ObjectId

class Car(Post):

    seates:int| None = None
    Fuletype:str| None = None
    engine:str | None = None