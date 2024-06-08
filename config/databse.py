from pymongo import MongoClient
client = MongoClient(
    f"mongodb://localhost:27017/Rentify_db")
try:
    db = client["Rentify_db"]
except Exception as e:
    print(e)

collection_name = db["testco"]
collection_user = db["users"]
collection_profile = db["profile"]
collection_house = db["houses"]
collection_Car = db["cars"]
collection_offer = db["offer"]
collection_reviwes = db["reviwes"]
collection_books = db["Booking"]
