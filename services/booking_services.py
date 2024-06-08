from config.databse import collection_books
import datetime
from fastapi import HTTPException
from starlette import  status
from bson import ObjectId
from .Account_services import check_of_id
from schema.booking_schema import book_serilazer,list_book_serilazer
async def find_book_by_id(id:str):
    if len(id)<24 or len(id)>24:
        raise  HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid Book id")
    book =   collection_books.find_one({'_id':ObjectId(id)})
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this booking is not found")
    return  book
def sting_to_date(date:str):

        if "/" in date:

            return datetime.datetime.strptime(date, "%Y/%m/%d")
        elif "-" in date:

            return datetime.datetime.strptime(date, "%Y-%m-%d")
def total_price(strat:str,end:str,price:float):

    start_date = sting_to_date(strat)
    end_date = sting_to_date(end)

    total_price = (end_date - start_date).days * price

    return total_price


def allow_to_update(user_id:str,book_user_id:str):
    if user_id == book_user_id:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you dont have authorize to update the book")




async def check_conflict(offer_id,new_booking):

    eixts_book = await get_offer_booking(offer_id)

    for book in eixts_book:
        if (new_booking['start_date']<= book['end_date'] and new_booking['end_date'] >= book['start_date'] )or (new_booking['start_date']>= book['start_date'] and new_booking['end_date']<= book['end_date'] ) :
            print(f"({(new_booking['start_date']<= book['end_date'] and new_booking['end_date'] >= book['start_date'] )}  {new_booking['start_date']>= book['end_date']}")
            print(f"({new_booking['start_date']}<= {book['end_date']}  {new_booking['end_date']}>= {book['start_date']}")
            return True
    return False



async def get_offer_booking(offer_id:str):
    if await check_of_id(offer_id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    offer_booking=  collection_books.find({'offer_id':offer_id,"is_active":True})
    return  offer_booking


async def get_user_booking(id:str):
    booking = collection_books.find({"user_id":id})
    return await list_book_serilazer(booking)


async def booking_dates(id:str):
    booking = await list_book_serilazer(collection_books.find({"offer_id":id}))
    dates = []
    print(len(booking))
    if len(booking) == 0:

        return dates

    for book in booking:

        dates.extend(await booking_days(book))
   # print("done done \n dine")
    return dates


async def booking_days(book):

    start = book['start_date']
    end = book['end_date']
    day = end - start
    # print(f"days = {day}")
    days  = [ ]
    for i in range(day.days + 1):
        current = start + datetime.timedelta(days=i)
        #print(current)
        days.append(current)

    return days


