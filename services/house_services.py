from schema.house import list_house_sreilazer
from config.databse import collection_house


async def get_all_house():
    house = await list_house_sreilazer(collection_house.aggregate([{"$sort": {"craeted_at": -1}}]))
    return house