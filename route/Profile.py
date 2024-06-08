from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.Profile import Profile,favorite
from models.address import Address
from config.databse import collection_profile,db,collection_user
from bson import ObjectId
from starlette import  status
from schema.profile_schema import profile_serilazer,list_profile_serlazir
from pydantic import Json
from auth import get_current_user
import secrets
from services.profile import Get_all,Get_profile_by_id,Get_current_profile,Update_profile,delete_profile
from services.booking_services import get_user_booking
from services.reviwe_services import get_rating



Profile_router = APIRouter(prefix='/users/Profile',tags=['Profile'])


user_dep =Annotated[dict,Depends(get_current_user)]


@Profile_router.get("/",status_code=status.HTTP_200_OK)
async def get_all_profile():
    prolfiles = await Get_all()
    return prolfiles
@Profile_router.get("get/{id}")
async  def get_profile_by_id(id:str):

    profile = await Get_profile_by_id(id)
    booking = await get_user_booking(profile["user_id"])
    rating = await get_rating(id)
    profile['booking'] = booking
    profile['rating'] = rating


    return  profile



@Profile_router.get("/current")
async  def get_current_profile(u:user_dep):
    current_profile = await Get_current_profile(u['id'])
    bookin= await get_user_booking(u["id"])
    rating = await get_rating(u["id"])
    current_profile['booking'] = bookin
    current_profile['rating'] = rating


    return    current_profile
#
# @Profile_router.post("/create",status_code=status.HTTP_201_CREATED)
# async def create_profile(u:user_dep,
#   first_name: str = Form(None),
#   last_name: str = Form(None) ,
#   city: str = Form(None) ,
# state: str = Form(None),
#   street: str = Form(None) ,
#
#   description:str=Form(None),
#                          image: UploadFile = File(None)):
#     userid = u['id']
#     if len(userid) < 24 or 24< len(userid):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid ID")
#
#     user = collection_user.find_one({'_id':ObjectId(userid)})
#     if user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user is not found")
#     profile_exist = collection_profile.find({'user_id':ObjectId(userid)})
#     if profile_exist is not None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="  you have profile can not to create new profile ")
#     address = Address(  city = city,
#     state = state,
#     street = street)
#
#     image_name = check_and_prepare(userid,image)
#     print(f"\n\nimage name = {image_name}\n\n")
#
#
#     new_profile = Profile( user_id = userid,
#
#         first_name = first_name,
#         last_name = last_name,
#                            address = address,
#         vertification = False,
#         description = description,
#         favotites =  [],
#         image  = image_name# str = "http://127.0.0.1:8000/static/Profile/person.jpg"
#     )
#     await uplaod_image(image_name,image)
#     profile = collection_profile.insert_one(new_profile.dict())
#     return {'state':'successfully'}
#

@Profile_router.put("/update",status_code=status.HTTP_201_CREATED)
async def update_profile(u:user_dep,
  first_name: str = Form(None),
  last_name: str = Form(None) ,
  city: str = Form(None) ,
state: str = Form(None),
  street: str = Form(None) ,

  description:str=Form(None),
                         image: UploadFile = File(None)):
    # userid = u['id']
    # if len(userid) < 24 or 24< len(userid):
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invalid ID")
    #
    # user = collection_user.find_one({'_id':ObjectId(userid)})
    # if user is None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user is not found")
    # profile_exist = collection_profile.find_one({'user_id':userid})
    # if profile_exist is  None:
    #     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="  you donot have profile ,\n craete profile then update profile ")


    address = Address(  city = city,
    state = state,
    street = street)
    # if image is not None:
    #    image_name = check_and_prepare("Profile",image)
    # else:
    #     image_name = None
    # print(f"\n\nimage name = {image_name}\n\n")
   # user_info = {'id': u['id'], 'fname': first_name, 'lname': last_name, 'address': address, 'desc': description})
    profile =await Update_profile(u['id'],{'first_name':first_name,'last_name':last_name,'address':dict(address),'description':description},image)
    # new_profile = Profile( user_id = userid,
    #
    #     first_name = first_name,
    #     last_name = last_name,
    #                        address = address,
    #     vertification = False,
    #     description = description,
    #     favotites =  [],
    #     image  = image_name# str = "http://127.0.0.1:8000/static/Profile/person.jpg"
    # )
    # if image is not None:
    #
    #  await uplaod_image(image_name,image)
    #profile = collection_profile.find_one_and_update({'user_id': userid},{'$set':new_profile.dict()})
    return profile



@Profile_router.delete('/delete',status_code=status.HTTP_200_OK)
async  def delete_profile(u:user_dep):
    profile_exist  =await  delete_profile(u['id'])

    return {'stata': 'sucessfully deleted','prolfile':profile_exist}


#
#
# def check_and_prepare(title:str,file:UploadFile = File()):
#     filepath = f"/static/{title}/"
#     file_name = file.filename
#     extension = file_name.split(".")[1]
#     if extension not in ["png","jpg",]:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")
#     image_name =secrets.token_hex(10) +'.'+extension
#     generated_name = filepath+image_name
#     return generated_name
#
#
# async def uplaod_image(img_name:str,file:UploadFile = File()):
#     file_content = await file.read()
#     with open(f".{img_name}","wb")as  file:
#         file.write(file_content)
#
#
#     # img = Image.open(generated_name)
#     # img = img.resize((200,200))
#     # img.save(generated_name)
#     file.close()
#
#     return {'state':'succesd'}
