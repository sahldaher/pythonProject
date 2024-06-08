from models.user import User
def user_serliazer(user) -> dict:
    if user is None:
        print(user)
        return None


    return{ "id": str(user["_id"]),
    "username": user["username"],
    "Normlazied_username": user["Normlazied_username"],
    "email": user["email"],
    "Normlazied_email":user["Normlazied_email"],
    "emailconfirm": user["emailconfirm"],
    #"password": "$2b$12$nN1k0pRVCr8SIMr6ClZr.uu.rD.HeMdG9ndCEnPVMbZXONKVSEHqe",
    "phone_number": user["phone_number"],
    "confirm_phoneNumber": user["confirm_phoneNumber"],
    "Roles":user["Roles"],
    "is_active": user["is_active"],}


def user_list_serliazer(users)-> list:
    return [user_serliazer(user) for user in users]