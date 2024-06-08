import datetime
from services.offer import check_and_prepares,uplaod_image,check_of_info
from fastapi import APIRouter,HTTPException,Depends,Form, UploadFile,File
from typing import Annotated
from models.Cars import Car
from models.address import Address
from config.databse import collection_Car,db,collection_user
from bson import ObjectId
from starlette import  status
from schema.car_schema import car_serilazer,list_cars_serilazaer
from pydantic import Json
from auth import get_current_user
from services.profile import Get_current_profile
from services.reviwe_services import get_offer_reviwes
from services.profile import Get_current_profile
from services.reviwe_services import get_rating

Car_router = APIRouter(prefix='/cars',tags=['cars'])


user_dep =Annotated[dict,Depends(get_current_user)]


@Car_router.get("/",status_code=status.HTTP_200_OK)
async  def get_car():
    cars = collection_Car.find()
    if cars is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this cars is not found")
    return list_cars_serilazaer(cars)


@Car_router.get("/usercars")
async def get_currentuser_car(u:user_dep):
    cars = collection_Car.find({'owner_id':u['id']})
    if cars is None:
              raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user do not havr avy cars")

    return list_cars_serilazaer(cars)

@Car_router.get("/{id}")
async  def get_car_by_id(id:str):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    car = collection_Car.find_one({'_id':ObjectId(id)})
    if car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this car is not found")

    car = car_serilazer(car)

    owner = await Get_current_profile(car['owner_id'])

    # owner_id   = house['owner_id']  # print(house['owner_id'])
    #  owner_info = collection_profile.find_one({'user_id':house['owner_id']})
    car['owner_info'] = {"username": f"{owner['first_name']} {owner['last_name']}",
                           "description": owner['description'], "image": owner['image'], "address": owner['address']}

    car['revwies'] = await get_offer_reviwes(id)
    car['rating'] = await get_rating(id)
    return car


@Car_router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_car( u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
    seates:int = Form(None),
                        engine: str = Form(None),
                        Fuletype: str = Form(None),
                        image:list[UploadFile] = File()

):
    userid = u['id']
    await check_of_info(userid)
    address = Address(city=city,
                      state=state,
                      street=street)
    images_name = check_and_prepares("cars",image)
    print(f"\n\nimage name = {images_name}\n\n")

    new_car = Car(owner_id=userid,

                        title = title,
                        description = description,
                        address =address,
                        location = location,
                        capacity =capacity,
                        price_by_day = price_by_day,#float = Field(gt=0, description="the price must be greater than zero")
                        images = images_name,
                        note = note,
                        craeted_at = datetime.datetime.now(),

                         seates =seates,
                    engine = engine,
                    Fuletype = Fuletype

                          )
    await uplaod_image(images_name, image)
    car = collection_Car.insert_one(new_car.dict())
    return {'state': 'successfully'}


@Car_router.put("/update/{id}",status_code=status.HTTP_201_CREATED)
async def update_car( id:str,u:user_dep,title:str  = Form(),
    description: str = Form(None),


    city: str = Form(None),
    state: str = Form(None),
    street: str = Form(None),
    location:str  = Form(None),
    capacity:int  = Form(None),
    price_by_day:float  = Form(),

    note:str  = Form(None),
    seates:int = Form(None),
                        engine: str = Form(None),
                        Fuletype: str = Form(None),
                        image:list[UploadFile] = File()

):
    userid = u['id']
    await check_of_info(userid)
    exists_car = collection_Car.find_one({'_id': ObjectId(id)})
    if exists_car is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found car")
    if str(exists_car['owner_id']) != userid:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="you do not have auyhurize ro update this car")
    address = Address(city=city,
                      state=state,
                      street=street)
    if image is not None:
        carimg = exists_car['images']
        if len(image) > len(carimg):
            new_images = check_and_prepares("cars", image[len(carimg):])
            carimg.extend(new_images)

    print(f"\n\nimage name = {carimg}\n\n")

    new_car = Car(owner_id=userid,

                        title = title,
                        description = description,
                        address =address,
                        location = location,
                        capacity =capacity,
                        price_by_day = price_by_day,#float = Field(gt=0, description="the price must be greater than zero")
                        images = carimg,
                        note = note,
                        craeted_at = datetime.datetime.now(),

                         seates =seates,
                    engine = engine,
                    Fuletype = Fuletype

                          )
    await uplaod_image(carimg[len(carimg)-len(image):], image)
    car = collection_Car.find_one_and_update({'_id':ObjectId(id)},{'$set':new_car.dict()})
    return {'state': 'successfully'}




@Car_router.delete("/delete/{id}",status_code=status.HTTP_200_OK)
async def delete_car(u:user_dep,id:str):
    car_deleted = collection_Car.find_one_and_delete({'_id':ObjectId(id)})
    if car_deleted is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this car not defind")
    return {'status':'sucessfully'}


