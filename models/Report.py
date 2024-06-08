import datetime

from pydantic import BaseModel

class Reports(BaseModel):
    onwer_id: ObjectId# user that report
    reported: ObjectId # user or house or any thing other

    reported_type:str   #user or house or any thing other
    report_description: str
    created_st:datetime.datetime
    is_active:bool
