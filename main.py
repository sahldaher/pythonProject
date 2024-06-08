from fastapi import FastAPI,HTTPException,Depends,Query,Form,File,UploadFile
from pymongo import MongoClient
from route.route import route
from auth import router
from auth import get_current_user
from starlette import  status
from typing import Annotated , Union
from pydantic import BaseModel
import secrets
from fastapi.staticfiles import StaticFiles
from PIL import Image
from models.user import User
from  route.Accounts import user_router
from  route.Profile import Profile_router
from route.house import House_router
from route.Cars import Car_router
from route.offer import offer_router
from route.reviews import reviwe_router
from route.Booking import book_router
from services.Homepage import top ,get_cars,get_houses,get_offer




app = FastAPI()
app.include_router(route)
app.include_router(router)
app.include_router(user_router)
app.include_router(Profile_router)
app.include_router(House_router)
app.include_router(Car_router)
app.include_router(offer_router)
app.include_router(reviwe_router)
app.include_router(book_router)




app.mount("/static",StaticFiles(directory="static"),name="static")





#
# client = MongoClient(
#     f"mongodb://localhost:27017/Rentify_db")
# try:
#     db = client["Rentify_db"]
# except Exception as e:
#     print(e)
user_dep =Annotated[dict,Depends(get_current_user)]

@app.get("/test/booking")
async def testbook():
    book = await top()
    cars = await get_cars()
    houses = await get_houses()
    offers = await get_offer()
    return offers


@app.get("/",status_code=status.HTTP_200_OK)
def user(user:user_dep):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='authntication falied')
    return {'user':user}

class test(BaseModel):
    name:str
    age:str
    file:UploadFile = File()
@app.post("/p/")
async def image(t:test  =Depends(),file:UploadFile = File()):
    return {"name":t.name,"img":file.filename}



@app.post("/upload")
async def create_upload(user:user_dep,file:UploadFile =File(...),):
    filepath = "static/images/"
    file_name = file.filename
    extension = file_name.split(".")[1]
    if extension not in ["png","jpg",]:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")
    token_name = secrets.token_hex(10)+'.'+extension
    generated_name = filepath+token_name
    file_content = await file.read()
    with open(generated_name,"wb")as  file:
        file.write(file_content)


    # img = Image.open(generated_name)
    # img = img.resize((200,200))
    # img.save(generated_name)
    file.close()

    return {'state':filepath}



