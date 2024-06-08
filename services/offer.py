
from config.databse import collection_user
import secrets
from bson import ObjectId
async def check_of_info(userid):

    if len(userid) < 24 or 24 < len(userid):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid ID")

    user = collection_user.find_one({'_id': ObjectId(userid)})
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="this user is not found")

def check_and_prepares(title,images):
    filepath = f"/static/{title}/"
    img_names = []
    num  = 1
    for img in images:
        file_name = img.filename
        extension = file_name.split(".")[1]
        if extension not in ["png","jpg",]:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail=f"this type {extension} is not accepted in the system")

        #image_name ="".join(title.split(" "))+f"{num}" +'.'+extension
        image_name =secrets.token_hex(10)+f"{num}" +'.'+extension
        generated_name = filepath+image_name
        img_names.append(generated_name)
        num += 1

    return img_names



async def uplaod_image(img_names,image):
    for i in range(len(img_names)):

        file_content = await image[i].read()
        with open(f".{img_names[i]}","wb")as  file:
            file.write(file_content)


        # img = Image.open(generated_name)
        # img = img.resize((200,200))
        # img.save(generated_name)
        file.close()

    return {'state':'succesd'}
