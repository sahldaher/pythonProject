import datetime

from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.house import House
from models.address import Address
from config.databse import collection_house,db,collection_user,collection_profile
from bson import ObjectId
from starlette import  status
from schema.house import house_sreilazer,list_house_sreilazer,house_sreilazer_post
from schema.profile_schema import profile_serilazer
from pydantic import Json
from auth import get_current_user
import secrets
from services.profile import Get_current_profile
from services.reviwe_services import get_offer_reviwes
from bson import ObjectId
from services.reviwe_services import get_rating
House_router = APIRouter(prefix='/houses',tags=['houses'])


user_dep =Annotated[dict,Depends(get_current_user)]

@House_router.get("/")
async  def get_houses():
    houses = collection_house.find()
    if houses is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this houses is not found")
    return await list_house_sreilazer(houses)


@House_router.get("/userhouses")
async def get_currentuser_house(u:user_dep):
    houses = collection_house.find({'owner_id':u['id']})
    if houses is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user do not havr avy houses")

    return await list_house_sreilazer(houses)

@House_router.get("/{id}")
async  def get_house_by_id(id:str):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    house = collection_house.find_one({'_id':ObjectId(id)})
    if house is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this house is not found")
    house =   await house_sreilazer(house)
    owner = await Get_current_profile(house['owner_id'])

   # owner_id   = house['owner_id']  # print(house['owner_id'])
   #  owner_info = collection_profile.find_one({'user_id':house['owner_id']})
    house['owner_info'] = {"username":f"{owner['first_name']} {owner['last_name']}","description":owner['description'],"image":owner['image'],"address":owner['address']}
   #
    house['revwies'] = await get_offer_reviwes(id)
    house['rating'] = await get_rating(id)



    # house['owner_info']  = owner_info['address']
    return  house



@House_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_house( u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
                        bedrooms: int = Form(None),
                        bathroms: int = Form(None),
                        image:list[UploadFile] = File()

):
    userid = u['id']
    await check_of_info(userid)
    address = Address(city=city,
                      state=state,
                      street=street)
    images_name =  check_and_prepares("Houses",image)
    print(f"\n\nimage name = {images_name}\n\n")

    new_house = House(owner_id=userid,

                        title = title,
                        description = description,
                        address =address,
                        location = location,
                        capacity =capacity,
                        price_by_day = price_by_day,#float = Field(gt=0, description="the price must be greater than zero")
                        images = images_name,
                        note = note,
                        craeted_at = datetime.datetime.now(),

                          bedrooms = bedrooms,
                          bathroms =bathroms,

                          )
    await uplaod_image(images_name, image)
    house = collection_house.insert_one(new_house.dict())
    return {'state': 'successfully'}


# @House_router.delete()

@House_router.put("/update/{id}")
async  def update_house(id:str,u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
                        bedrooms: int = Form(None),
                        bathroms: int = Form(None),
                        image:list[UploadFile] = File()
):
    userid = u['id']
    await check_of_info(userid)
    exists_house = collection_house.find_one({'_id':ObjectId(id)})
    if exists_house is None:
        raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="nou found hoouse")
    if str(exists_house['owner_id']) != userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="you do not have auyhurize ro update this house")
    address = Address(city=city,
                      state=state,
                      street=street)
    if image is not None:
        houseimg = exists_house['images']
        if len(image) > len(houseimg):
             new_images = check_and_prepares("Houses", image[len(houseimg):])
             houseimg.extend(new_images)

    print(f"\n\nimage name = {houseimg}\n\n")

    new_house = House(owner_id=userid,

                      title=title,
                      description=description,
                      address=address,
                      location=location,
                      capacity=capacity,
                      price_by_day=price_by_day,
                      # float = Field(gt=0, description="the price must be greater than zero")
                      images=houseimg,
                      note=note,
                      craeted_at=datetime.datetime.now(),

                      bedrooms=bedrooms,
                      bathroms=bathroms,

                      )
    if image is not None:
        await uplaod_image(houseimg[len(houseimg)-len(image):], image)
    house = collection_house.find_one_and_update({'_id':ObjectId(id)},{'$set':new_house.dict()})
    return {'state': 'successfully'}

async def check_of_info(userid):

    if len(userid) < 24 or 24 < len(userid):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    user = collection_user.find_one({'_id': ObjectId(userid)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user is not found")

#
# def check_and_prepare(userid:str,file:UploadFile = File()):
#     filepath = "./static/Houses/"
#     file_name = file.filename
#     extension = file_name.split(".")[1]
#     if extension not in ["png","jpg",]:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")
#     image_name =userid +'.'+extension
#     generated_name = filepath+image_name
#     return generated_name

@House_router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
async def delete_hose(u:user_dep,id:str):
    house_deleted = collection_house.find_one_and_delete({'_id':ObjectId(id)})
    if house_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this hous not defind")
    return {'status':'sucessfully'}

def check_and_prepares(title,images):
    filepath = f"/static/{title}/"
    img_names = []
    num  = 1
    for img in images:
        file_name = img.filename
        extension = file_name.split(".")[1]
        if extension not in ["png","jpg",]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")

        #image_name ="".join(title.split(" "))+f"{num}" +'.'+extension
        image_name =secrets.token_hex(10)+f"{num}" +'.'+extension
        generated_name = filepath+image_name
        img_names.append(generated_name)
        num += 1

    return img_names



async def uplaod_image(img_names,image):
    for i in range(len(img_names)):

        file_content = await image[i].read()
        with open(f".{img_names[i]}","wb")as  file:
            file.write(file_content)


        # img = Image.open(generated_name)
        # img = img.resize((200,200))
        # img.save(generated_name)
        file.close()

    return {'state':'succesd'}

#
#
# async def uplaod_image(img_name:str,file:UploadFile = File()):
#     file_content = await file.read()
#     with open(img_name,"wb")as  file:
#         file.write(file_content)
#
#
#     # img = Image.open(generated_name)
#     # img = img.resize((200,200))
#     # img.save(generated_name)
#     file.close()
#
#     return {'state':'succesd'}
