from database import myDataBase
import json
import os
from kivy.app import App

def export(export_dir = "", file_name = "all_data"):
    file_name = "all_data" if file_name == "" else file_name
    
    db = myDataBase()
    all_data = db.get_all_films()
    
    os.makedirs(export_dir, exist_ok=True)
    file_name = file_name + ".json"
    file_path = os.path.join(export_dir, file_name)
    json_string = json.dumps(all_data,  ensure_ascii = False , indent=4)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_string)

def import_films(import_dir , file_name ):
    db = myDataBase()

    file_name = file_name + ".json"
    # os.makedirs(import_dir)
    file_path = os.path.join(import_dir, file_name)
    films_list = []
    with open(file_path, "r",  encoding="utf-8") as f:
        films_list = json.load(f)
    
    for film in films_list:
        film_name = film["name"]
        film_genre = film["genre"]
        film_status = film["status"]
        film_rating = film["rating"]
        film_description = film["description"]

        db.add_film_to_bd(film_name, film_genre, film_status, film_rating, film_description)

        app = App.get_running_app()

        app.data_updated = True