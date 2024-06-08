from config.databse import collection_Car
from schema.car_schema import list_cars_serilazaer

from schema.offer_schema import list_offers_serilazaer




async def get_all_cars():
    cars= list_cars_serilazaer(collection_Car.aggregate([{"$sort":{"craeted_at":-1}}]))
    return cars