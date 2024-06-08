from datetime import timedelta,datetime
from typing import Annotated
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel,Field,EmailStr
from starlette import  status
from models.user import User,User_request
from  models.Profile import Profile

from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm,OAuth2PasswordBearer
from jose import jwt,JWTError
from config.databse import collection_name,collection_user,collection_profile

router = APIRouter(prefix='/auth',tags=['auth'])

SECRET_KEY = '2000/5/11/madrid14@modric#(kroos)vini8098$88&8'
ALGORITHM = 'HS256'

bcrypt_context=CryptContext(schemes=['bcrypt'],deprecated='auto')
Oauth2_bearar = OAuth2PasswordBearer(tokenUrl='auth/token')
#
# class create_user_request(BaseModel):
#     username: str
#     password: str
#     # def __init__(self,name:str,password:str):
    #     self.username = name,
    #     self.password = password





class Token(BaseModel):
    access_token: str
    token_type: str






@router.post("/create",status_code=status.HTTP_201_CREATED)
async def create_user(user_request:User_request):
    user_exist = collection_user.find_one({'email':user_request.email})
    username = collection_user.find_one({'username':user_request.username})
    if user_exist is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="this email is exist")
    if username is not None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="this username is exist")

    new_user = User(username=user_request.username,Normlazied_username=user_request.username.upper(),email = user_request.email,password=bcrypt_context.hash(user_request.password),phone_number=user_request.phone_number,Roles = [])#create_user_request(username=user_request.username,password=   bcrypt_context.hash(user_request.password),)

    new_user.Roles.append("user")
    collection_user.insert_one(new_user.dict())
    user = auth_user(new_user.username, password=user_request.password)
  #  print(f"user is : {user}")
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Colud not validate user.')
    p = collection_user.find_one({'username':user_request.username})
    if p is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="username is not found can n ot to create profile")
    print(f"user id id = {p['_id']}")
    new_profile = Profile(user_id = str(p['_id']),favotites = [],image='/static/Profile/person.jpg',description = None,address = None,first_name = None,last_name = None,vertification = False,)
    collection_profile.insert_one(new_profile.dict())
    token = create_access_token(user['username'], str(user['_id']),user['Roles'], timedelta(minutes=20))
    return Token(access_token=token, token_type='bearer')  # {"name":user["username"],"id":str(user['_id'])}


@router.post("/token",response_model=Token)
async def login(form_data:Annotated[OAuth2PasswordRequestForm,Depends()]) -> dict:
    user = auth_user(form_data.username,password=form_data.password)
    if not user:
      raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Colud not validate user.')
    print(user['Roles'])
    token = create_access_token(user['username'],str(user['_id']),user['Roles'],timedelta(minutes=20))
    return Token(access_token = token,token_type='bearer')#{"name":user["username"],"id":str(user['_id'])}


def auth_user(username:str,password:str):
    user = collection_user.find_one({"username":username})

    if not user:
        print("false usernot found")

        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="the user not found")
    #print(f"password error\n password enter:{password}, \t userpassword : {user['password']}")
    try:
        if not bcrypt_context.verify(password,user["password"]):
            print(f"password error\n password enter:{password}, \t userpassword : {user['password']}")
            return False
    except :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="this user is not found ")

    return user

def create_access_token(username:str,user_id:str,role:[],expires_delta:timedelta):
    encode ={'sub':username,'id':user_id,'Roles':role}
    expirs = datetime.utcnow() + expires_delta
    encode.update({'exp':expirs})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)

async def get_current_user(token:Annotated[str,Depends(Oauth2_bearar)]):
    try:
        playload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        username:str = playload.get('sub')
        user_id:int = playload.get('id')
        user_role:[] = playload.get('Roles')
        if username is None or user_id is None:
            raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Colud not validate user.')
        return {'username':username,'id':user_id,'Roles':user_role}
    except JWTError:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail='Colud not validate user.')