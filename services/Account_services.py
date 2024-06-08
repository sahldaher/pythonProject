from config.databse import collection_user
from bson import ObjectId
from schema.user_schema import user_serliazer,user_list_serliazer
from fastapi import HTTPException
from starlette import status
async def Get_users() -> list:
    try:

        li_users =   user_list_serliazer(list(  collection_user.find({})[13:]))
        return li_users
    except   Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=f"{e}")


async def Get_user_by_id(id:str) ->dict:
    try:
        await check_of_id(id)



        user =collection_user.find_one({"_id": ObjectId(id)})
        await check_user_found(user,"user")




        return user_serliazer(user)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=f"{e}00")
#
# async def Get_user_by_id_u_e(id:str) ->dict:
#     # try:
#         await check_of_id(id)
#
#
#
#         user =list(collection_user.find_one({"_id": ObjectId(id)},{'username':1,'phone_number':1}))[13:]
#         await check_user_found(user)
#
#
#
#
#         return user_serliazer(user)
#     # except Exception as e:
#     #     raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED,detail=f"{e}")



async def Get_user_by_email(email:str):
    user = user_serliazer(collection_user.find_one({"email": email}))
    await check_user_found(user, "user")

    return user

async def Update_user(id:str,user):
    await check_of_id(id)



    user =collection_user.find_one_and_update({"_id": ObjectId(id)}, {"$set": user.dict()})
    await check_user_found(user,"user")

    return user_serliazer(user)

async def check_user_found(user,type):
    if user is None:
        raise     HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"this {type} is not found")


async def check_of_id(id:str):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild id")
