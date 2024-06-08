import datetime
from services.offer import check_and_prepares,uplaod_image,check_of_info
from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.offer import Offer
from models.address import Address
from config.databse import collection_offer,db,collection_user
from bson import ObjectId
from starlette import  status
from schema.offer_schema import offer_serilazer,list_offers_serilazaer
from pydantic import Json
from auth import get_current_user
from services.reviwe_services import get_offer_reviwes
from services.profile import Get_current_profile
from services.reviwe_services import get_rating


offer_router = APIRouter(prefix='/offers',tags=['offers'])


user_dep =Annotated[dict,Depends(get_current_user)]


@offer_router.get("/",status_code=status.HTTP_200_OK)
async  def get_offer():
    offers = collection_offer.find()
    if offers is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this offers is not found")
    return list_offers_serilazaer(offers)


@offer_router.get("/useroffers")
async def get_currentuser_offer(u:user_dep):
    offers = collection_offer.find({'owner_id':u['id']})
    if offers is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user do not havr avy offers")

    return list_offers_serilazaer(offers)

@offer_router.get("/{id}")
async  def get_offer_by_id(id:str):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    offer = collection_offer.find_one({'_id':ObjectId(id)})
    if offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this offer is not found")
    offer =   offer_serilazer(offer)
    owner = await Get_current_profile(offer['owner_id'])
    #
    # # owner_id   = house['owner_id']  # print(house['owner_id'])
    # #  owner_info = collection_profile.find_one({'user_id':house['owner_id']})
    offer['owner_info'] = {"username": f"{owner['first_name']} {owner['last_name']}",
                           "description": owner['description'], "image": owner['image'], "address": owner['address']}

    offer['revwies'] = await get_offer_reviwes(id)
    offer['rating'] = await get_rating(id)

    return offer


@offer_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_offer( u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
    type:str = Form(),

                        image:list[UploadFile] = File()

):
    userid = u['id']
    await check_of_info(userid)
    address = Address(city=city,
                      state=state,
                      street=street)
    images_name = check_and_prepares("offer",image)
    print(f"\n\nimage name = {images_name}\n\n")

    new_offer = Offer(owner_id=userid,

                        title = title,
                        description = description,
                        address =address,
                        location = location,
                        capacity =capacity,
                        price_by_day = price_by_day,#float = Field(gt=0, description="the price must be greater than zero")
                        images = images_name,
                        note = note,
                        craeted_at = datetime.datetime.now(),

                         type=type,


                          )
    await uplaod_image(images_name, image)
    offer = collection_offer.insert_one(new_offer.dict())
    return {'state': 'successfully'}


@offer_router.put("/update/{id}",status_code=status.HTTP_201_CREATED)
async def update_offer( id:str,u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
    type:str = Form(None),
                        image:list[UploadFile] = File()

):
    userid = u['id']
    await check_of_info(userid)
    exists_offer = collection_offer.find_one({'_id': ObjectId(id)})
    if exists_offer is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found offer")
    if str(exists_offer['owner_id']) != userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you do not have auyhurize ro update this offer")
    address = Address(city=city,
                      state=state,
                      street=street)
    if image is not None:
        offerimg = exists_offer['images']
        if len(image) > len(offerimg):
            new_images = check_and_prepares("offer", image[len(offerimg):])
            offerimg.extend(new_images)

    print(f"\n\nimage name = {offerimg}\n\n")

    new_offer = Offer(owner_id=userid,

                        title = title,
                        description = description,
                        address =address,
                        location = location,
                        capacity =capacity,
                        price_by_day = price_by_day,#float = Field(gt=0, description="the price must be greater than zero")
                        images = offerimg,
                        note = note,
                        craeted_at = datetime.datetime.now(),

                        type = type,

                          )
    await uplaod_image(offerimg[len(offerimg)-len(image):], image)
    offer = collection_offer.find_one_and_update({'_id':ObjectId(id)},{'$set':new_offer.dict()})
    return {'state': 'successfully'}




@offer_router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
async def delete_offer(u:user_dep,id:str):
    offer_deleted = collection_offer.find_one_and_delete({'_id':ObjectId(id)})
    if offer_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this offer not defind")
    return {'status':'sucessfully'}


