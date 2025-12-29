import sqlite3 as sq
from utils.user_service import is_log_in

def init(con,  pre_films, statuses, pre_genres, rating_v, pre_user):
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
        description TEXT NOT NULL, 
        owner_id INTEGER NOT NULL)
        ''')
    
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                login TEXT NOT NULL,
                password  TEXT NOT NULL,
                is_active INTEGER NOT NULL DEFAULT 0,
                avatar BLOB) ''')
    
    con.commit()
    # Проверяем, есть ли уже данные в таблицах
    cur.execute('SELECT COUNT(*) FROM status')
    if cur.fetchone()[0] == 0:
        for status in statuses:
            cur.execute('INSERT INTO status (name) VALUES(?)', status)
        con.commit()

    cur.execute('SELECT COUNT(*) FROM rating')
    if cur.fetchone()[0] == 0:
        for rating in rating_v:
            cur.execute('INSERT INTO rating (value) VALUES(?)', rating)
        con.commit()

    cur.execute('SELECT COUNT(*) FROM genre')
    if cur.fetchone()[0] == 0:
        for genre in pre_genres:
            cur.execute('INSERT INTO genre (name) VALUES(?)', genre)
        con.commit()

    cur.execute('SELECT COUNT(*) FROM filmlist')
    if cur.fetchone()[0] == 0:
        for film in pre_films:
            cur.execute('''INSERT INTO filmlist (name, genre, status, rating, description, owner_id) 
                VALUES(?, ?, ?, ?, ?, ?)''', film)
        con.commit()

    cur.execute('SELECT COUNT(*) FROM users ')
    if cur.fetchone()[0] == 0:
        for user in pre_user:
            cur.execute('''INSERT INTO users (login,password, is_active, avatar) 
                VALUES(?, ?, ?, ?)''', user)
        con.commit()
    cur.close()
    print("Database initialized successfully!")

def get_active_user(con):
    con.row_factory = sq.Row
    cur = con.cursor()

    cur.execute(''' 
        SELECT * FROM users WHERE users.is_active = 1
        ''')
    results = cur.fetchall()

    return results

def get_films_dict(req_res, genre = None):
    
    films = []
    for row in req_res:
        
        film_dict = {
            'name': row['name'],
            'genre': row['genre_name'],  
            'status': row['status_name'], 
            'rating': row['rating'],
            'description': row['description'], 
            'film_id': row['film_id'],
            'active': False,  
        }
        if genre == None: films.append(film_dict)
        else: 
            if genre in film_dict['genre']: films.append(film_dict)  
    return films


@is_log_in
def get_film_by_name(film_name, con, current_user = None):
    
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute(f'''
        SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
        JOIN genre ON filmlist.genre  = genre.genre_id
        JOIN status ON filmlist.status = status.status_id
        WHERE filmlist.name LIKE ? AND filmlist.owner_id = ?
        ''', (film_name, current_user))
    results = cur.fetchall()
    return results

@is_log_in
def get_all_films(con, current_user = None):
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute('''
        SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
        JOIN genre ON filmlist.genre  = genre.genre_id
        JOIN status ON filmlist.status = status.status_id
        WHERE  filmlist.owner_id = ?
        ORDER BY rating DESC''', (current_user,))
    results = cur.fetchall()
    return results
@is_log_in
def delete_film(con, film_id, current_user = None):
    cur = con.cursor()
    cur.execute('''DELETE FROM filmlist where film_id = ? AND filmlist.owner_id = ?''', (film_id,current_user))
    con.commit()

@is_log_in
def get_film_with_filters(con , film_status = "", film_rating = "", film_genre = "", current_user = None):
    film_genre = film_genre.strip().lower() if film_genre!="" else ""
    con.row_factory = sq.Row 
    cur = con.cursor()

    base_req = ''' SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
        JOIN genre ON filmlist.genre  = genre.genre_id
        JOIN status ON filmlist.status = status.status_id
        '''
    
    if(film_rating != '' and film_status != "Все"):
        base_req += '''WHERE status.name = ? AND rating = ? AND filmlist.owner_id = ?'''
        cur.execute(base_req, ( film_status,film_rating, current_user))
    elif (film_rating != '' and film_status == "Все"):
        base_req += '''WHERE rating = ? AND filmlist.owner_id = ?'''
        cur.execute(base_req, (film_rating, current_user))
    elif(film_rating == '' and film_status == "Все"):
        base_req += ''' AND filmlist.owner_id = ? ORDER BY rating DESC'''
        cur.execute(base_req, (current_user,))
    elif film_rating == '' and film_status != "Все":
        base_req += '''WHERE status.name = ? AND filmlist.owner_id = ? ORDER BY rating DESC'''
        cur.execute(base_req, (film_status,current_user))
    results = cur.fetchall()
    return results

def add_genre(con, genre_name):
    cur = con.cursor()
    cur.execute('''INSERT INTO genre(name) VALUES (?)''', (genre_name,))
    genre_id = cur.lastrowid
    con.commit()
    return genre_id

def already_in_db(con,   film_name, film_genre, film_status, film_rating):
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

    return 1 if results else 0

def get_genre_id(con, genre_name):
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute('''SELECT * from genre where LOWER(name) = LOWER(?)''', (genre_name,))
    results = cur.fetchall()
    films = []
    for row in results:
        film_dict = {
        'name': row['name'],
        'genre_id': row['genre_id']
        }
        films.append(film_dict)
    if not films: genre_id = add_genre(con, genre_name)
    else: genre_id = films[0]['genre_id']

    return genre_id

def get_status_id (con, status_name):
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute('''SELECT * from status where LOWER(name) = LOWER(?)''', (status_name,))
    results = cur.fetchall()
    films = []
    for row in results:
        film_dict = {
        'name': row['name'],
        'status_id': row['status_id']
        }
        films.append(film_dict)
                
    if films: status_id = films[0]['status_id']
    else: status_id = -1

    return status_id

@is_log_in
def get_film_by_id(con, film_id,  current_user = None):
    con.row_factory = sq.Row 
    cur = con.cursor()
    film_id_int = int(film_id)
    cur.execute('''
        SELECT filmlist.name, genre.name as genre_name, status.name as status_name, 
        rating, filmlist.description, filmlist.film_id 
        FROM filmlist
        JOIN genre ON filmlist.genre = genre.genre_id
        JOIN status ON filmlist.status = status.status_id
        WHERE filmlist.film_id = ? AND filmlist.owner_id = ?
    ''', (film_id_int, current_user))
    result = cur.fetchall()
    return result\

@is_log_in
def add_film_to_bd(con, film_name, film_genre, film_status, film_rating, film_discription = "", current_user = None):
    cur = con.cursor()

    if film_name == "" or film_name == " ": return 3
    if(already_in_db(con,   film_name, film_genre, film_status, film_rating) == 1): return 0
    if film_genre == "" or film_genre == " ": return 4

    genre_id = get_genre_id(con, film_genre)
    status_id = get_status_id(con, film_status)
    if status_id == -1: return 2

    rating_id = film_rating
    if film_rating == "": rating_id = "0"

    cur.execute('''INSERT INTO filmlist(name, genre, status, rating, description, owner_id) VALUES (?, ?, ?, ?, ?, ?)''', 
                            (film_name, genre_id, status_id, rating_id, film_discription, current_user))
    con.commit()
    return 1

@is_log_in
def update_film_data(con, film_id, film_name, film_genre, film_status, film_rating, film_discription, current_user = None):
    cur = con.cursor()
    if film_name == "" or film_name == " ": return 3
    if film_genre == "" or film_genre == " ": return 4

    genre_id = get_genre_id(con, film_genre)
    status_id = get_status_id(con, film_status)
    if status_id == -1: return 2
    rating_id = film_rating
    if film_rating == "": rating_id = "0"

    cur.execute('''UPDATE filmlist 
        set genre = ?, status = ? , rating = ?,  description= ?
        WHERE film_id = ? AND filmlist.owner_id = ?''', (genre_id, status_id, rating_id, film_discription,film_id, current_user ))
    
    con.commit()
    return 1


