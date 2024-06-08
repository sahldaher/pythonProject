from pydantic import BaseModel,Field,EmailStr
class User(BaseModel):
    username:str = Field(default=None,title="username",max_length=50)
    Normlazied_username:str |None = None
    email:EmailStr
    Normlazied_email:str|None = None # = email.upper()
    emailconfirm :bool = False
    password:str
    phone_number:str|None = None
    confirm_phoneNumber:bool = False
    Roles:list[str]




    is_active:bool = True

class User_request(BaseModel):
    username: str = Field(default=None, title="username", max_length=50)

    email: EmailStr
     # = email.upper()
    phone_number: str | None = None
    password: str


class User_updat(BaseModel):
    username: str = Field(default=None, title="username", max_length=50)


     # = email.upper()
    phone_number: str | None = None

