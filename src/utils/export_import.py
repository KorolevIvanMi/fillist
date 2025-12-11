from database import myDataBase
import json
def export( filename, indent=2):
    db = myDataBase()
    all_data = db.get_all_films()

    print(all_data)

export("ss")