import datetime

from pydantic import BaseModel
from bson import  ObjectId

class Booking(BaseModel):

    user_id : str
    offer_id:str
    book_on:str
    craeted_at:datetime.datetime
    start_date:datetime.datetime
    end_date:datetime.datetime
    confirm_book:bool   = False
    total_price: float
    bill_img:str | None = None
    bill_num:str | None = None
    is_active: bool = True
