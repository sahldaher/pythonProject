def car_serilazer(car) -> dict:
    if car is None:
        return None
    return {"id": str(car["_id"]),
        'owner_id': car['owner_id'],
        'title': car['title'],
        'description': car['description'],
        'address': car['address'],
        'location': car['location'],
        'capacity': car['capacity'],
        'price_by_day': car['price_by_day'],  # float = Field(gt=0, description="the price must be greater than zero")
        'images': car['images'],
        'note': car['note'],
        'craeted_at': car['craeted_at'],

        'seates': car['seates'],
        'engine': car['engine'],
        'Fuletype': car['Fuletype'],
            'Type':'car',
            'owner_info':'',
            'revwies' :'',
            'rating':''

    }


def list_cars_serilazaer(cars) -> list:
    if cars is None:
        return None
    return [car_serilazer(car) for car in cars]