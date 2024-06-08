from models.Profile import Profile
from services.Account_services import Get_user_by_id,check_of_id,check_user_found
from config.databse import collection_house,collection_offer,collection_Car,collection_profile,collection_reviwes,collection_books
from schema.reviwe_shema import list_reviwe_serilazer

from schema.house import list_house_sreilazer
from schema.car_schema import list_cars_serilazaer
from schema.offer_schema import list_offers_serilazaer


#

# from services.profile import get_user_offers

async def profile_serilazer(profile) ->dict:
    if profile is None:
        return None
    user =await  Get_user_by_id(profile["user_id"])
    offers = await get_user_offers(user["id"])
    reviwes = await get_revwies(user["id"])

    return {"id": str(profile["_id"]),
                "username":user["username"],
                "phone_number":user["phone_number"],
                "user_id":profile["user_id"],
  "address":profile['address'],
  "first_name": profile['first_name'],
  "last_name": profile['last_name'],
  "vertification": profile['vertification'],
  "description": profile['description'],
  "favotites": profile['favotites'],
  "image": profile['image'],
            "offers":offers,
            "revwies":reviwes,


}

async def list_profile_serlazir(prolfiles) -> list:
    return [  await profile_serilazer(profile) for profile in prolfiles]


async def get_user_offers(id:str):
    await check_of_id(id)


    profile = collection_profile.find_one({'user_id':id})
    await check_user_found(profile, "profile.")
    houses = await list_house_sreilazer(collection_house.find({'owner_id':id}))
    car =  list_cars_serilazaer(collection_Car.find({'owner_id':id }))
    offers =  list_offers_serilazaer(collection_offer.find({'owner_id':id }))
    # print(houses,car,offers)
    houses.extend(car)
    houses.extend(offers)

    return houses


async def get_revwies(id:str):
    await check_of_id(id)

    profile = collection_profile.find_one({'user_id': id})
    await check_user_found(profile, "profile.")

    reviwes = await list_reviwe_serilazer(collection_reviwes.find({'offer_id':str(profile['_id'])}))


    return reviwes
