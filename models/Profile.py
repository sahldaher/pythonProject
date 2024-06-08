import datetime
from bson import ObjectId
from pydantic import BaseModel
from .address import Address
from models.user import User

class favorite(BaseModel):
    type:str
    offerid:str
class Profile(BaseModel):

    user_id:str
    address:Address|None = None
    first_name:str |None = None
    last_name:str|None = None
    vertification:bool = False
    description:str|None
    favotites: list[favorite] = []
    image : str = "http://127.0.0.1:8000/static/Profile/person.jpg"

