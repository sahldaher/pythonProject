import datetime
from services.offer import check_of_info
from services.reviwe_services import find_offer
from services.booking_services import sting_to_date,total_price,find_book_by_id,allow_to_update,check_conflict
from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.Booking import Booking
from models.address import Address
from config.databse import collection_books,db,collection_user,collection_offer
from bson import ObjectId
from starlette import  status
from schema.booking_schema import book_serilazer,list_book_serilazer,get_name_and_image
from pydantic import Json
from auth import get_current_user
from services.profile import uplaod_image,check_and_prepare
from services.booking_services import booking_dates


book_router = APIRouter(prefix='/books',tags=['books'])


user_dep =Annotated[dict,Depends(get_current_user)]


@book_router.get("/",status_code=status.HTTP_200_OK)
async def get_booking():
    books = collection_books.find()
    rs = await list_book_serilazer(books)
    return rs

@book_router.get("/my",status_code=status.HTTP_200_OK)
async def get_books(u:user_dep):

    books = collection_books.find({'user_id':u['id']})
    rs = await list_book_serilazer(books)
    return rs


@book_router.get("/user/{id}", status_code=status.HTTP_200_OK)
async def get_user_book(u: user_dep,id:str):
    books = collection_books.find({'user_id': id})
    rs = await list_book_serilazer(books)
    return rs


@book_router.get("/get/{id}",status_code=status.HTTP_200_OK)
async def get_books_by_id(id:str):
    books = collection_books.find_one({'_id':ObjectId(id)})
    #print(books['onwer_id'])
    rs =   await book_serilazer(books)
    return rs



@book_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_book(u:user_dep,
    # review_on:str
    offer_id:str  = Form(),# ObjectId#house or car or elec or furniture or user

    start_date = Form(),


end_date= Form(),



                        type:str = Form(),
   ):
    userid = u['id']
    await check_of_info(userid)
    offer_exist = await find_offer(offer_id,"offer")

    if await check_conflict(offer_id,{'start_date':sting_to_date(start_date),'end_date':sting_to_date(end_date)}):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="conflict_in the booking")

    totalprice = total_price(start_date,end_date,offer_exist['price_by_day'])
        #ccheck_from date function
    new_booking = Booking(
        user_id = userid,
    book_on= type.lower(),
    offer_id=offer_id ,
        craeted_at = datetime.datetime.now(),# ObjectId#house or car or elec or furniture or user
    start_date = sting_to_date(start_date),
    end_date = sting_to_date(end_date) ,
    created_at = datetime.datetime.now(),
    confirm_book = False,
        total_price = totalprice,
        is_active = True,
        bill_num = None,
        bill_img = None,

    )



    collection_books.insert_one(new_booking.dict())
    return {'state':'sucessfully'}


@book_router.put("/add_bill/{id}",status_code=status.HTTP_201_CREATED)
async def add_img_bill(u:user_dep,id:str,bill_num:str = Form(None),bill_img : UploadFile = File(None)):
    #print(f" image name = {bill_img.filename}\n bill num = {bill_num}")
    userid = u['id']
    await check_of_info(userid)
    book =  await find_book_by_id(id)
    print(dict(book))
    allow_to_update(userid,book['user_id'])

    if bill_img is  not None:
        image_name = await check_and_prepare("bill",bill_img)
    else:
        image_name = None
        print(f" image name = {image_name}\n bill num = {bill_num}")
    collection_books.find_one_and_update({'_id':ObjectId(id)},{'$set':{'bill_img':image_name,'bill_num':bill_num}})
    if bill_img is not None:
        await uplaod_image(image_name,bill_img)

    return {'state':"successfuly",'detail':' add bill to book is successful'}



@book_router.put("/update/{id}",status_code=status.HTTP_201_CREATED)
async def update_book(u:user_dep,id:str,
    # review_on:str
                        # ObjectId#house or car or elec or furniture or user

                        start_date=Form(),

                        end_date=Form(),
bill_num:str = Form(None),
                        bill_img : UploadFile = File(None)


   ):
    userid = u['id']
    await check_of_info(userid)
    book = await find_book_by_id(id)
    allow_to_update(userid, book['user_id'])
    offer = await find_offer(book['offer_id'], book['book_on'])
    # if not offer_exist:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this offer or profile is not found")

    totalprice = total_price(start_date, end_date, offer['price_by_day'])
    if bill_img is not None:
        image_name = await check_and_prepare("bill", bill_img)
    else:
        image_name = None
    _start_date = sting_to_date(start_date)
    _end_date = sting_to_date(end_date)
    s_d = datetime.datetime(_start_date.year,_start_date.month,_start_date.day)
    e_d = datetime.datetime(_end_date.year,_end_date.month,_end_date.day)
    if image_name is None and bill_num is None:
        collection_books.find_one_and_update({'_id': ObjectId(id)},
                                             {'$set': {'start_date': s_d ,'end_date': e_d,'total_price':totalprice}})
    elif image_name is not None and bill_num is None:
        collection_books.find_one_and_update({'_id': ObjectId(id)},
                                             {'$set': {'start_date':s_d, 'end_date': e_d,'bill_img':image_name,'total_price':totalprice}})
        await uplaod_image(image_name, bill_img)
    elif image_name is  None and bill_num is not None:
        collection_books.find_one_and_update({'_id': ObjectId(id)},
                                             {'$set': {'start_date': s_d, 'end_date': e_d,'bill_num':bill_num,'total_price':totalprice}})

    else:
        collection_books.find_one_and_update({'_id': ObjectId(id)},
                                             {'$set': {'start_date': s_d, 'end_date': e_d,
                                                       'bill_num': bill_num,'bill_img':image_name,'total_price':totalprice}})
        await uplaod_image(image_name, bill_img)


    return {'state':'sucessfully','detail':'update the boook is completed'}


    # if not offer_exist:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this offer or profile is not found")
    # reviwe = collection_reviwes.find_one({'_id':ObjectId(id)})
    # if reviwe is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="thie reviwe is not found")




@book_router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
async def book_reviwe(u:user_dep,id:str):
    userid = u['id']
    await check_of_info(userid)
    book = collection_books.find_one({'_id':ObjectId(id)})
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this book is noyt found")

    if book['user_id'] == userid or "admin" in u['Roles']:
      de_book = collection_books.find_one_and_delete({'_id':ObjectId(id)})
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="you dont have ahtorized")
    return {'state':'successed','bookviwe':await book_serilazer(de_book)}



@book_router.get("/book/dates")
async def get_book_date(offer_id):
    book_date = await booking_dates(offer_id)

    return book_date