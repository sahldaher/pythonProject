from fastapi import APIRouter,HTTPException
from models.user import User ,User_updat
from config.databse import collection_user,db
from schema.shemas import list_serial
from bson import ObjectId
from starlette import  status
from schema.user_schema import user_serliazer,user_list_serliazer
from services.Account_services import Get_users,Get_user_by_id,Get_user_by_email,Update_user



user_router = APIRouter(prefix='/users',tags=['users'])
@user_router.get("/",status_code=200)
async def get_users():
    users = await Get_users()

    return users

@user_router.get("/user/{id}",status_code=status.HTTP_200_OK)
async def get_user_by_id(id:str):
    user = await Get_user_by_id(id)
    return user



@user_router.get("/user/email/{email}",status_code=status.HTTP_200_OK)
async def get_user_by_email(email:str):
    user = await Get_user_by_email(email)
    return user
@user_router.get("/blcked/",status_code=200)
async def get_blocked_users():
    users = user_list_serliazer(list(collection_user.find({"is_active":False})))



    return users



@user_router.put("user/update/{id}",status_code=status.HTTP_201_CREATED)
async  def update_user(id:str,user_update:User_updat):

    user = await Update_user(id,user_update)# user_serliazer(collection_user.find_one_and_update({"_id":ObjectId(id)},{"$set":user_update.dict()}))

    return {"statues":"sucessfully",'msg': " update user is uccessfully","userinfo ": user}


@user_router.put("user/block/{id}",status_code=status.HTTP_201_CREATED)
async  def block_user(id:str):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="Invaild id")
    user = user_serliazer(collection_user.find_one_and_update({"_id":ObjectId(id)},{"$set":{'is_active':False}}))
    if user is None:
        raise     HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user is not found")
    return {"statues":"sucessfully",'msg': " Block user is uccessfully",'info':user}




@user_router.delete("user/deleted/{id}",status_code=status.HTTP_201_CREATED)
async  def delete_user(id:str,user_update:User_updat):
    if len(id) < 24 or 24 < len(id):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invaild id")

    user = user_serliazer(collection_user.find_one_and_delete({"_id":ObjectId(id)}))
    if user is None:
        raise     HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user is not found")
    return {"statues":"sucessfully",'msg': " remove  user is uccessfully",'info':user}






