from pydantic import BaseModel
class Address(BaseModel):

    city:str | None = None

    state:str |None = None
    street:str | None = None