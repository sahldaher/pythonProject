from config.databse import collection_profile,collection_user
from bson import ObjectId

async def reviwe_serilazer(reviwe) -> dict:
    if reviwe is None:
        return None
    user_info =     await get_name_and_image(reviwe['onwer_id'])
    name =user_info['username']
    img = user_info['image']

    return  { "id": str(reviwe["_id"]),'onwer_id': reviwe['onwer_id'],
    # review_on:str
    'offer_id':reviwe['offer_id'], # ObjectId#house or car or elec or furniture or user
    'comment':reviwe['comment'],
    'rate':reviwe['rate'],
             'type': reviwe['review_on'],
    'created_at':reviwe['created_at'],
             'username':name,
             'image':img

    }

async def list_reviwe_serilazer(reviwes) ->list:
    if reviwes is None:
        return None
    return [await reviwe_serilazer(r) for r in reviwes]




async def get_name_and_image(id:str) :
    username =   collection_user.find_one({'_id':ObjectId(id)},{'username':1})

    img =   collection_profile.find_one({'user_id':str(username['_id'])},{'image':1})
    return{'username':username['username'],'image':img['image']}

