from database import myDataBase
import json
import os

def export(export_dir = ""):
    db = myDataBase()
    all_data = db.get_all_films()
    

    os.makedirs(export_dir, exist_ok=True)
    file_path = os.path.join(export_dir, "all_your_data.json")

    json_string = json.dumps(all_data,  ensure_ascii = False , indent=4)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(json_string)
        
