def individual_serial(todo) -> dict:
    if(todo is None):
        return None
    return {
        "id":str(todo["_id"]),
        "name": todo["name"],
        "description": todo["description"],
        "done": todo["done"],
    }

def list_serial(todos) -> list:
    return [individual_serial(todo) for todo in todos]