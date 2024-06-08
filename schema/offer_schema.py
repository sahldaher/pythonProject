def offer_serilazer(offer) -> dict:
    if offer is None:
        return None
    return {"id": str(offer["_id"]),
        'owner_id': offer['owner_id'],
        'title': offer['title'],
        'description': offer['description'],
        'address': offer['address'],
        'location': offer['location'],
        'capacity': offer['capacity'],
        'price_by_day': offer['price_by_day'],  # float = Field(gt=0, description="the price must be greater than zero")
        'images': offer['images'],
        'note': offer['note'],
        'craeted_at': offer['craeted_at'],

        'type': offer['type'],
            'owner_info': '',
            'revwies': '',
            'rating': ''

            }


def list_offers_serilazaer(offers) -> list:
    if offers is None:
        return None
    return [offer_serilazer(offer) for offer in offers]