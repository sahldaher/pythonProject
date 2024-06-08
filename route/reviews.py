import datetime
from services.offer import check_and_prepares,uplaod_image,check_of_info
from services.reviwe_services import find_offer
from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.Reviwes import Reviwes
from models.address import Address
from config.databse import collection_reviwes,db,collection_user,collection_offer
from bson import ObjectId
from starlette import  status
from schema.reviwe_shema import reviwe_serilazer,list_reviwe_serilazer,get_name_and_image
from pydantic import Json
from auth import get_current_user


reviwe_router = APIRouter(prefix='/reviwes',tags=['reviwes'])


user_dep =Annotated[dict,Depends(get_current_user)]


@reviwe_router.get("/",status_code=status.HTTP_200_OK)
async def get_reviwes():
    reviwes = collection_reviwes.find()
    rs = await list_reviwe_serilazer(reviwes)
    return rs

@reviwe_router.get("/my",status_code=status.HTTP_200_OK)
async def get_reviwes(u:user_dep):

    reviwes = collection_reviwes.find({'onwer_id':u['id']})
    rs = await list_reviwe_serilazer(reviwes)
    return rs


@reviwe_router.get("/user/{id}", status_code=status.HTTP_200_OK)
async def get_user_reviwe(u: user_dep,id:str):
    reviwes = collection_reviwes.find({'onwer_id': id})
    rs = await list_reviwe_serilazer(reviwes)
    return rs


@reviwe_router.get("/get/{id}",status_code=status.HTTP_200_OK)
async def get_reviwes_by_id(id:str):
    reviwes = collection_reviwes.find_one({'_id':ObjectId(id)})
    #print(reviwes['onwer_id'])
    rs =   await reviwe_serilazer(reviwes)
    return rs



@reviwe_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_reviwe(u:user_dep,
    # review_on:str
    offer_id:str  = Form(),# ObjectId#house or car or elec or furniture or user
    comment:str  = Form(None),
    rate:int = Form(),
                        type:str = Form(),
   ):
    userid = u['id']
    await check_of_info(userid)
    offer = find_offer(offer_id,type)

    new_review = Reviwes(
        onwer_id = userid,
    review_on= type.lower(),
    offer_id=offer_id ,# ObjectId#house or car or elec or furniture or user
    comment = comment,
    rate = rate,
    created_at = datetime.datetime.now())

    collection_reviwes.insert_one(new_review.dict())
    return {'state':'sucessfully'}


@reviwe_router.put("/update/{id}",status_code=status.HTTP_201_CREATED)
async def update_reviwe(u:user_dep,id:str,
    # review_on:str
    offer_id:str  = Form(),# ObjectId#house or car or elec or furniture or user
    comment:str  = Form(None),
    rate:int = Form(),
    type:str = Form()

   ):
    userid = u['id']
    await check_of_info(userid)
    offer = find_offer(offer_id,type)

    reviwe = collection_reviwes.find_one({'_id':ObjectId(id)})
    if reviwe is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="thie reviwe is not found")

    new_review = Reviwes(
        onwer_id = userid,
    review_on= type.lower(),
    offer_id=offer_id ,# ObjectId#house or car or elec or furniture or user
    comment = comment,
    rate = rate,
    created_at = datetime.datetime.now())

    collection_reviwes.find_one_and_update({'_id':ObjectId(id)},{"$set":new_review.dict()})
    return {'state':'sucessfully'}


@reviwe_router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
async def delete_reviwe(u:user_dep,id:str):
    userid = u['id']
    await check_of_info(userid)
    re = collection_reviwes.find_one({'_id':ObjectId(id)})
    if re is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this review is noyt found")
    if re['onwer_id'] != userid or "admin" not in u['Roles']:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you dont have premssion")
    de_re = collection_reviwes.find_one_and_delete({'_id':ObjectId(id)})
    return {'state':'successed','reviwe':await reviwe_serilazer(de_re)}


