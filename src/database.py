import os
import sqlite3 as sq
import sys
import utils.requests  as rq

def get_db_path():
    """Универсальный путь к базе данных для Windows и Linux"""
    if hasattr(sys, '_MEIPASS'):
        # В режиме EXE - используем папку пользователя
        user_data_dir = os.path.join(os.path.expanduser('~'), 'Fillist')
        try:
            os.makedirs(user_data_dir, exist_ok=True)
            new_user_dir = os.path.join(user_data_dir, 'film_base')
            os.makedirs(new_user_dir, exist_ok=True)
            db_path = os.path.join(new_user_dir, 'film_base.db')

            return db_path
        except Exception as e:
            
            return 'film_base.db'
    else:
        # В режиме разработки - используем папку dataBase в корне проекта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        database_dir = os.path.join(project_root, 'resources')
        
        # Создаем папку dataBase если её нет
        os.makedirs(database_dir, exist_ok=True)
        
        dev_db_path = os.path.join(database_dir, 'film_base.db')
        print(f"Dev mode - DB path: {dev_db_path}")
        return dev_db_path

class myDataBase:
    _instance = None
    _initialized = False


    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    

    def __init__(self):
        if not self._initialized:
            self.db_path = get_db_path()
            self.con = sq.connect(self.db_path)
            self.db_init()
            self._initialized = True
        
    def db_init(self):
        # Убедимся, что можем создать файл БД
        db_dir = os.path.dirname(self.db_path)
        
        try:
            # Создаем директорию если нужно
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir, exist_ok=True)
                print(f"Created directory: {db_dir}")
            
            # Проверяем права на запись
            if os.path.exists(self.db_path):
                if not os.access(self.db_path, os.W_OK):
                    print(f"Warning: No write permissions for {self.db_path}")
            else:
                # Проверяем права на создание файла в директории
                test_file = os.path.join(db_dir, 'test_write.tmp')
                try:
                    with open(test_file, 'w') as f:
                        f.write('test')
                    os.remove(test_file)
                except Exception as e:
                    print(f"No write permissions in {db_dir}: {e}")
        
        except Exception as e:
            print(f"Error during DB path setup: {e}")
        
        pre_films = [
            ("Зелёная миля", 1, 2, 4, "Фильм жестокий, но очень поучительный и ценный", 1),
            ("Я-легенда", 2, 1, 0, "", 1),
            ("Наруто", 3, 3, 0, "", 1)
        ]
        statuses = [
            ("В планах",),
            ("Просмотрен",),
            ("В процессе",)
        ]
        pre_genres = [
            ("тёмное фэнтези",),
            ("ужасы",),
            ("фэнтези",)
        ]
        ratings = [
            (1,),
            (2,),
            (3,),
            (4,),
            (5,)
        ]
<<<<<<< HEAD

        pre_user = [
            ("admin", 12345, 0, None)
        ]
=======
        
        pre_person = [
            ("admin", "123450", 0, None)
        ]

>>>>>>> 0d57d91 (c)
        try:
            rq.init(self.con, pre_films, statuses, pre_genres, ratings, pre_user)

        except Exception as e:
            print(f"Error initializing database: {e}")
            print(f"DB path was: {self.db_path}")

    def find_film_by_name(self, film_name):
        film_name = f"%{film_name}%"
        try:
            results = rq.get_film_by_name(film_name, self.con)
            films = rq.get_films_dict(results)
            return films

        except Exception as e:
            print(f"Error in find_film_by_name: {e}")
            return []

    def get_all_films(self):

        results = rq.get_all_films(self.con)
        films = rq.get_films_dict(results)
        return films
        
    def del_film(self, film_id):
        rq.delete_film(self.con, film_id)
        
    def find_films_with_filters(self, film_status, film_rating, film_genre):
        film_genre = film_genre.strip().lower()
        
        results = rq.get_film_with_filters(self.con, film_status, film_rating, film_genre)
        films = rq.get_films_dict(results, genre= film_genre)
        return films
    
    def add_film_to_bd(self, film_name, film_genre, film_status, film_rating, film_discription):
        film_name = film_name.strip()
        film_genre = film_genre.strip().lower()
        film_status = film_status.strip()
        film_rating = str(film_rating).strip() if film_rating else "0"
        film_discription = film_discription.strip()
        
        res = rq.add_film_to_bd(self.con,film_name, film_genre, film_status, film_rating, film_discription)
        return res

    def find_film_by_id(self, film_id):
        
        result = rq.get_film_by_id(self.con, film_id)
        films = rq.get_films_dict(result)
        return films[0] if films else None
        
    def update_data(self,film_id, film_name, film_genre, film_status, film_rating, film_discription):
        film_name = film_name.strip()
        film_genre = film_genre.strip().lower()
        film_status = film_status.strip()
        film_rating = str(film_rating).strip() if film_rating else "0"
        film_discription = film_discription.strip()
        
        res = rq.update_film_data(self.con ,film_id, film_name, film_genre, film_status, film_rating, film_discription)

        return res