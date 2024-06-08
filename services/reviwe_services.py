from config.databse import collection_offer,collection_Car,collection_house,collection_profile,collection_reviwes
from bson import ObjectId
from fastapi import HTTPException,status
from schema.car_schema import car_serilazer
from schema.offer_schema import offer_serilazer
from schema.house import house_sreilazer
from schema.profile_schema import profile_serilazer
from schema.reviwe_shema import list_reviwe_serilazer


async def find_offer(id:str,type:str):
    if type.lower() =="house":
        house = collection_house.find_one({'_id':ObjectId(id)})
        if house is not None:
            print("find house")
            return await house_sreilazer(house)

    if type.lower() == "car":

        car = collection_Car.find_one({'_id': ObjectId(id)})
        if car is not None:
            print("find car")
            return  car_serilazer(car)



    if type.lower() == "offer":
        offer = collection_offer.find_one({'_id': ObjectId(id)})
        if offer is not None:
            print("find offer")
            return offer_serilazer(offer)

    if type.lower() == "profile":
        pro = collection_profile.find_one({'_id': ObjectId(id)})
        if pro is not None:
            print("find profile")
            return  profile_serilazer(pro)

    raise  HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this offers is not found")



    print("you donut detrmine the type")



async def get_offer_reviwes(offer_id:str):

    reviwes =await list_reviwe_serilazer(collection_reviwes.find({'offer_id':offer_id}))
    return reviwes


async def get_rating(id:str):
    pipline = [{'$match':{'offer_id':id}},{'$group':{'_id':'null','total_rate':{'$sum':'$rate'},'num_of_reviwes':{'$sum':1},'avg_rate':{'$avg':'$rate'}}}]
    rating = list(collection_reviwes.aggregate(pipline))

    if len(rating) == 0:
        return { 'total_rate': 0,
  'num_of_reviwes': 0,
  'avg_rate': 0}
    return {
  'num_of_reviwes': rating[0]['num_of_reviwes'],
  'avg_rate': rating[0]['avg_rate']}
