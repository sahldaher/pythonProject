from schema.offer_schema import list_offers_serilazaer
from config.databse import collection_offer


async def get_all_offers():
    offers = list_offers_serilazaer(collection_offer.aggregate([{"$sort": {"craeted_at": -1}}]))
    return offers