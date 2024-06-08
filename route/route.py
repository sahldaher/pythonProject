from fastapi import APIRouter
from models.todo import todo
from config.databse import collection_name
from schema.shemas import list_serial
from bson import ObjectId
from services.reviwe_services import get_rating
from services.booking_services import booking_dates

route = APIRouter()

@route.get("/todo")
async def get_todo():
    todos = list_serial(collection_name.find())
    return todos

@route.post("/todo/create")

async def craete_todo(todo:todo|None):
    collection_name.insert_one(dict(todo))
    return True

@route.put("/todo/update/{id}")
async def update_todo(id:str,todo:todo):
    collection_name.find_one_and_update({"_id":ObjectId(id)},{"$set":dict(todo)})



@route.delete("/todo/delete/{id}")
async def delete_todo(id:str):
    collection_name.find_one_and_delete({"_id":ObjectId(id)})



#
# @route.get("/testrt")
# async def test_rating(id:str):
#     rating = await get_rating(id)
#     return rating
#
#
#
# @route.get("/booktest/")
# async def test_book(offer_id:str):
#
#     bookng = await booking_dates(offer_id)
#     return bookng