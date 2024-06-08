from config.databse import collection_profile,collection_user
from bson import ObjectId
from services.reviwe_services import find_offer

async def book_serilazer(book) -> dict:
    if book is None:
        return None
    user_info =     await get_name_and_image(book['user_id'])
    name =user_info['username']
    img = user_info['image']
    offer = await find_offer(book['offer_id'],book['book_on'])


    return  { "id": str(book["_id"]),'user_id': book['user_id'],
    # review_on:str
    'offer_id':book['offer_id'], # ObjectId#house or car or elec or furniture or user
    'type':book['book_on'],
    'start_date':book['start_date'],
    'end_date':book['end_date'],
    'total_price':book['total_price'],
    'confirm_book':book['confirm_book'],
             'is_active': book['is_active'],
             'bill_img': book['bill_img'],
             'bill_num': book['bill_num'],
    'created_at':book['craeted_at'],
             'username':name,
             'image':img,
              'offer':offer

    }

async def list_book_serilazer(books) ->list:
    if books is None:
        return None
    return [await book_serilazer(r) for r in books]




async def get_name_and_image(id:str) :
    username =   collection_user.find_one({'_id':ObjectId(id)},{'username':1})

    img =   collection_profile.find_one({'user_id':str(username['_id'])},{'image':1})
    return{'username':username['username'],'image':img['image']}


