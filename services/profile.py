from config.databse import collection_profile,collection_house,collection_offer,collection_Car
from fastapi import HTTPException,File,UploadFile
from starlette import status
from schema.profile_schema import profile_serilazer,list_profile_serlazir
from .Account_services import check_of_id,check_user_found
from bson import ObjectId
import secrets
from schema.house import list_house_sreilazer
from schema.car_schema import list_cars_serilazaer
from schema.offer_schema import list_offers_serilazaer
#
#
# def tt(n:int):
#     if n>10:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="bad request")

async def Get_all():
    # try:
        profiles =collection_profile.find()
        return await list_profile_serlazir(profiles)
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=f"{e}....")


async def Get_profile_by_id(id:str):
    await check_of_id(id)
    profile =  collection_profile.find_one({'_id': ObjectId(id)})
    await check_user_found(profile,"profile")
    return await profile_serilazer(profile)


async def Get_current_profile(id:str):
    await check_of_id(id)
    current_profile = collection_profile.find_one({'user_id': id})
    await check_user_found(current_profile,"Profile")
    pro = await profile_serilazer(current_profile)
    return  pro



async def Update_profile(u_id,pro_info,image):
    await check_of_id(u_id)
    current_profile = collection_profile.find_one({'user_id': u_id})
    #await check_user_found(current_profile, "Profile")
    await check_user_found(current_profile,"Profile")
    # image_name = "0000"
    if image is not None:
        image_name =  await  check_and_prepare("Profile", image)
        pro_info['image'] =  image_name
        new_profile= collection_profile.find_one_and_update({'_id': current_profile['_id']}, {'$set': pro_info})
        await uplaod_image(image_name, image)

    else:
        new_profile=collection_profile.find_one_and_update({'_id': current_profile['_id']}, {'$set': pro_info})





    return {'state': 'successfully','info':await profile_serilazer(new_profile)}


async def delete_profile(id:str):
    await check_of_id(id)
    profile= collection_profile.find_one_and_delete({'_id':ObjectId(id)})
    await check_user_found(profile,"profile")
    return  profile_serilazer(profile)

async def check_and_prepare(title:str,file:UploadFile = File()):

    filepath = f"/static/{title}/"
    file_name = file.filename
    extension = file_name.split(".")[1]
    if extension not in ["png","jpg",]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")
    image_name =secrets.token_hex(10) +'.'+extension
    generated_name = filepath+image_name
    return generated_name


async def uplaod_image(img_name:str,file:UploadFile = File()):
    file_content = await file.read()
    with open(f".{img_name}","wb")as  file:
        file.write(file_content)


    # img = Image.open(generated_name)
    # img = img.resize((200,200))
    # img.save(generated_name)
    file.close()

    return {'state':'succesd'}
#
# async def get_user_offers(id:str):
#     await check_of_id(id)
#
#
#     profile = collection_profile.find_one({'user_id':id})
#     await check_user_found(profile, "profile.")
#     houses = list_house_sreilazer(collection_house.find({'owner_id':id}))
#     car = list_cars_serilazaer(collection_Car.find({'owner_id':id }))
#     offers = list_cars_serilazaer(collection_offer.find({'owner_id':id }))
#     # print(houses,car,offers)
#     houses.extend(car)
#     houses.extend(offers)
#
#     return houses


