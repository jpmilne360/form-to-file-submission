import os
from datetime import datetime
from project import app


def food() -> dict:
    return {
    "Food":
        [
            {"ID":"1", "name":"Turkey Roast Dinner"},
            {"ID":"2", "name":"Lasagne with Salad"},
            {"ID":"3", "name":"Fish and Chips"},
            {"ID":"4", "name":"Cheeseburger and Fries"},
            {"ID":"5", "name":"Vegetarian Quiche"},
        ]
    }

def convert_iso_datetime(date_time: str) -> str:
    return datetime.fromisoformat(date_time).strftime("%d/%m/%Y %H:%M")


def terms_conditions() -> str:
    filepath = os.path.join(app.root_path, "static", "files", "terms-conditions.txt")
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def process_file(file):
    f_content = file.read()
    f_decoded = f_content.decode('utf-8')
    file_content = f_decoded.split() # becomes a list, removing all whitespace, newlines, tabs
    file_content = ' '.join(file_content) # list join, space seperator
    return file_content