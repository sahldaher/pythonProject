from pydantic import BaseModel
from .post import Post
from bson import ObjectId

class House(Post):

    bedrooms:int | None = None

    bathroms:int | None = None



