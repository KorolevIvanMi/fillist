import os
import sqlite3 as sq
import sys
from utils import get_resource_path

def get_db_path():
    """Универсальный путь к базе данных для Windows и Linux"""
    if hasattr(sys, '_MEIPASS'):
        # В режиме EXE - используем папку пользователя
        user_data_dir = os.path.join(os.path.expanduser('~'), 'Fillist')
        try:
            os.makedirs(user_data_dir, exist_ok=True)
            db_path = os.path.join(user_data_dir, 'film_base.db')
            
            return db_path
        except Exception as e:
            
            return 'film_base.db'
    else:
        # В режиме разработки - используем папку dataBase в корне проекта
        script_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(script_dir)
        database_dir = os.path.join(project_root, 'dataBase')
        
        # Создаем папку dataBase если её нет
        os.makedirs(database_dir, exist_ok=True)
        
        dev_db_path = os.path.join(database_dir, 'film_base.db')
        print(f"Dev mode - DB path: {dev_db_path}")
        return dev_db_path

class myDataBase:
    def __init__(self):
        self.db_path = get_db_path()
        
        self.db_init()
        
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
            ("Зелёная миля", 1, 2, 4, "Фильм жестокий, но очень поучительный и ценный"),
            ("Я-легенда", 2, 1, 0, ""),
            ("Наруто", 3, 3, 0, "")
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
        
        try:
            with sq.connect(self.db_path) as con:
                cur = con.cursor()

                cur.execute('''
                CREATE TABLE IF NOT EXISTS status(
                status_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)
                ''')
                
                cur.execute('''
                CREATE TABLE IF NOT EXISTS rating(
                rating_id INTEGER PRIMARY KEY AUTOINCREMENT,
                value INTEGER NOT NULL)
                ''')
                
                cur.execute('''
                CREATE TABLE IF NOT EXISTS genre(
                genre_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL)
                ''')
                
                cur.execute('''
                CREATE TABLE IF NOT EXISTS filmlist(
                film_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre INTEGER NOT NULL,
                status INTEGER NOT NULL,
                rating INTEGER NOT NULL,
                description TEXT NOT NULL)
                ''')
                
                # Проверяем, есть ли уже данные в таблицах
                cur.execute('SELECT COUNT(*) FROM status')
                if cur.fetchone()[0] == 0:
                    for status in statuses:
                        cur.execute('INSERT INTO status (name) VALUES(?)', status)
                
                cur.execute('SELECT COUNT(*) FROM rating')
                if cur.fetchone()[0] == 0:
                    for rating in ratings:
                        cur.execute('INSERT INTO rating (value) VALUES(?)', rating)
                
                cur.execute('SELECT COUNT(*) FROM genre')
                if cur.fetchone()[0] == 0:
                    for genre in pre_genres:
                        cur.execute('INSERT INTO genre (name) VALUES(?)', genre)
                
                cur.execute('SELECT COUNT(*) FROM filmlist')
                if cur.fetchone()[0] == 0:
                    for film in pre_films:
                        cur.execute('''INSERT INTO filmlist (name, genre, status, rating, description) 
                                    VALUES(?, ?, ?, ?, ?)''', film)
                
                print("Database initialized successfully!")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
            print(f"DB path was: {self.db_path}")

    
    def find_film_by_name(self, film_name):
        try:
            with sq.connect(self.db_path) as con:
                con.row_factory = sq.Row 
                cur = con.cursor()
                cur.execute('''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            WHERE filmlist.name = ?
                            ''', (film_name,))
                results = cur.fetchall()
                
                films = []
                for row in results:
                    film_dict = {
                        'name': row['name'],
                        'genre': row['genre_name'],  
                        'status': row['status_name'], 
                        'rating': row['rating'],
                        'description': row['description'], 
                        'film_id': row['film_id'],
                        'active': False,  
                    }
                    films.append(film_dict)
                
                return films
        except Exception as e:
            print(f"Error in find_film_by_name: {e}")
            return []

    def get_all_films(self):
        with sq.connect(self.db_path) as con:
            con.row_factory = sq.Row 
            cur = con.cursor()
            cur.execute('''
                        SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                        JOIN genre ON filmlist.genre  = genre.genre_id
                        JOIN status ON filmlist.status = status.status_id
                        ''')
            results = cur.fetchall()
            films = []
            for row in results:
                film_dict = {
                    'name': row['name'],
                    'genre': row['genre_name'],  
                    'status': row['status_name'], 
                    'rating': row['rating'],
                    'active': False,  
                    'description': row['description'] , 
                    'film_id': row['film_id']
                }
                films.append(film_dict)
            return films
        
    def del_film(self, film_id):
        with sq.connect(self.db_path) as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM filmlist where film_id = ?''', (film_id,))
            return 0

    def find_films_with_filters(self, film_status, film_rating):
        with sq.connect(self.db_path) as con:
            con.row_factory = sq.Row 
            cur = con.cursor()
            if(film_rating != '' and film_status != "Все"):
                cur.execute('''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            WHERE status.name = ? AND rating = ?
                            ''', (film_status, film_rating))
            elif(film_rating != '' and film_status == "Все"):
                cur.execute('''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            WHERE rating = ?
                            ''', (film_rating,))    
            elif(film_rating == '' and film_status == "Все"):
                cur.execute('''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            ''')
            elif(film_rating == '' and film_status != "Все"):
                cur.execute('''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            WHERE status.name = ? 
                            ''', (film_status,))
            results = cur.fetchall()
            films = []
            for row in results:
                film_dict = {
                    'name': row['name'],
                    'genre': row['genre_name'],  
                    'status': row['status_name'], 
                    'rating': row['rating'],
                    'description': row['description'], 
                    'film_id': row['film_id'],
                    'active': False,  
                }
                films.append(film_dict)
            return films

    def add_film_to_bd(self, film_name, film_genre, film_status, film_rating, film_discription):
        film_name = film_name.strip()
        film_genre = film_genre.strip().lower()
        film_status = film_status.strip()
        film_rating = str(film_rating).strip() if film_rating else "0"
        film_discription = film_discription.strip()
        if film_name == "" or film_name == " ":
            return 0
        with sq.connect(self.db_path) as con:
            con.row_factory = sq.Row 
            cur = con.cursor()
            
            cur.execute('''
                SELECT filmlist.name, filmlist.genre as genre_id, 
                    genre.name as genre_name, status.name as status_name, 
                    rating, filmlist.description, filmlist.film_id 
                FROM filmlist
                JOIN genre ON filmlist.genre = genre.genre_id
                JOIN status ON filmlist.status = status.status_id
                WHERE LOWER(filmlist.name) = LOWER(?) 
                AND LOWER(genre.name) = LOWER(?)
                AND LOWER(status.name) = LOWER(?)
                AND rating = ?
            ''', (film_name, film_genre, film_status, film_rating))
            
            results = cur.fetchall()
            
            if not results:
                if film_genre != "":
                    genre_id = -1
                    cur.execute('''SELECT * from genre where LOWER(name) = LOWER(?)''', (film_genre,))
                    results = cur.fetchall()
                    films = []
                    for row in results:
                        film_dict = {
                            'name': row['name'],
                            'genre_id': row['genre_id']
                        }
                        films.append(film_dict)
                    
                    if not films:
                        cur.execute('''INSERT INTO genre(name) VALUES (?)''', (film_genre,))
                        genre_id = cur.lastrowid
                    else:
                        genre_id = films[0]['genre_id']
                
                status_id = -1
                cur.execute('''SELECT * from status where LOWER(name) = LOWER(?)''', (film_status,))
                results = cur.fetchall()
                films = []
                for row in results:
                    film_dict = {
                        'name': row['name'],
                        'status_id': row['status_id']
                    }
                    films.append(film_dict)
                
                if films:
                    status_id = films[0]['status_id']
                else:
                    return 0
                
                rating_id = film_rating
                if rating_id == "":
                    rating_id = "0"
                
                cur.execute('''INSERT INTO filmlist(name, genre, status, rating, description) VALUES (?, ?, ?, ?, ?)''', 
                            (film_name, genre_id, status_id, rating_id, film_discription))
                
                con.commit()
                return 1
            else:
                return 0

    def find_film_by_id(self, film_id):
        with sq.connect(self.db_path) as con:
            con.row_factory = sq.Row 
            cur = con.cursor()
            film_id_int = int(film_id)
            cur.execute('''
                        SELECT filmlist.name, genre.name as genre_name, status.name as status_name, 
                            rating, filmlist.description, filmlist.film_id 
                        FROM filmlist
                        JOIN genre ON filmlist.genre = genre.genre_id
                        JOIN status ON filmlist.status = status.status_id
                        WHERE filmlist.film_id = ?
                        ''', (film_id_int,))
            result = cur.fetchone()
            
            if result:
                film_dict = {
                    'name': result['name'],
                    'genre': result['genre_name'],  
                    'status': result['status_name'], 
                    'rating': result['rating'],
                    'description': result['description'], 
                    'film_id': result['film_id'],
                    'active': False,  
                }
                return film_dict
            return None
                
    def update_data(self,film_id, film_name, film_genre, film_status, film_rating, film_discription):
        film_name = film_name.strip()
        film_genre = film_genre.strip().lower()
        film_status = film_status.strip()
        film_rating = str(film_rating).strip() if film_rating else "0"
        film_discription = film_discription.strip()

        if film_name == "" or film_name == " ":
            return 0
        with sq.connect(self.db_path) as con:
            con.row_factory = sq.Row 
            cur = con.cursor()
            genre_id = -1
            cur.execute('''SELECT * from genre where LOWER(name) = LOWER(?)''', (film_genre,))
            results = cur.fetchall()
            films = []
            for row in results:
                film_dict = {
                    'name': row['name'],
                    'genre_id': row['genre_id']
                }
                films.append(film_dict)
                
            if not films:
                cur.execute('''INSERT INTO genre(name) VALUES (?)''', (film_genre,))
                genre_id = cur.lastrowid
            else:
                genre_id = films[0]['genre_id']
                
            status_id = -1
            cur.execute('''SELECT * from status where LOWER(name) = LOWER(?)''', (film_status,))
            results = cur.fetchall()
            films = []
            for row in results:
                film_dict = {
                    'name': row['name'],
                    'status_id': row['status_id']
                }
                films.append(film_dict)
                
            if films:
                status_id = films[0]['status_id']
            else:
                return 0
                
            rating_id = film_rating
            if rating_id == "":
                rating_id = "0"
            cur.execute('''UPDATE filmlist 
                        set genre = ?, status = ? , rating = ?,  description= ?
                        WHERE film_id = ?''', (genre_id, status_id, rating_id, film_discription,film_id))
            return 1