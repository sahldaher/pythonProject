#from services.profile import Get_current_profile
async def house_sreilazer(house) -> dict:
    if house is None:
        print("house is none in serialazer")
        return None

    return {"id": str(house["_id"]),
'owner_id' : house['owner_id'],
        'title': house['title'],
                        'description' : house['description'],
                        'address' : house['address'],
                        'location' : house['location'],
                        'capacity' : house['capacity'],
                        'price_by_day' : house['price_by_day'],#float = Field(gt=0, description="the price must be greater than zero")
                        'images' : house['images'],
                        'note' : house['note'],
                        'craeted_at' : house['craeted_at'],

                          'bedrooms' : house['bedrooms'],
                          'bathroms' : house['bathroms'],
            'Type':'house',
            'owner_info': '',
            'revwies': '',
            'rating': ''

            }

async def list_house_sreilazer(houses) -> list:
    if houses is None:
        return None
    return [await house_sreilazer(house) for house in houses]




async def house_sreilazer_post(house,id) -> dict:
    if house is None:
        print("house is none in serialazer")
        return None
    owner_info =  await Get_current_profile(id)

    return {"id": str(house["_id"]),
'owner_id' : house['owner_id'],
        'title': house['title'],
                        'description' : house['description'],
                        'address' : house['address'],
                        'location' : house['location'],
                        'capacity' : house['capacity'],
                        'price_by_day' : house['price_by_day'],#float = Field(gt=0, description="the price must be greater than zero")
                        'images' : house['images'],
                        'note' : house['note'],
                        'craeted_at' : house['craeted_at'],

                          'bedrooms' : house['bedrooms'],
                          'bathroms' : house['bathroms'],
            'owner_info':owner_info



    }
