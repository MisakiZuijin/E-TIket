from function.storage import baca_data, simpan_data

FILE_USER = "data_users.json"

def register(username, password, role="user"):
    data = baca_data(FILE_USER)
    if any(u["username"] == username for u in data):
        return "Username sudah digunakan!"
    new_id = len(data) + 1
    data.append({"id": new_id, "username": username, "password": password, "role": role})
    simpan_data(FILE_USER, data)
    return "success"

def login(username, password):
    data = baca_data(FILE_USER)
    for user in data:
        if user["username"] == username and user["password"] == password:
            return user
    return None