from config.databse import collection_books
from services.reviwe_services import find_offer
from services.car_services import get_all_cars
from services.house_services import get_all_house
from services.offer_services import get_all_offers
async def top():
    pipline = [{"$group":{"_id":"$offer_id","type":{"$addToSet":"$book_on"},"total":{"$sum":1},},},{"$sort":{"total":-1},}]
    booking = list(collection_books.aggregate(pipline))

    top_booking = [await find_offer(b['_id'],b['type'][0]) for b in booking]
    return top_booking

async def get_cars():
     cars = await get_all_cars()
     return cars


async def get_houses():
     house = await get_all_house()
     return house


async def get_offer():
     offers = await get_all_offers()
     return offers