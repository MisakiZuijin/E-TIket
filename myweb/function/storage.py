import json, os

def baca_data(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def simpan_data(file_name, data):
    with open(file_name, "w") as f:
        json.dump(data, f, indent=4)