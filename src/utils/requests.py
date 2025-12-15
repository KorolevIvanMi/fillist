import sqlite3 as sq


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

def get_film_by_name(film_name, con):
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute(f'''
                            SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                            JOIN genre ON filmlist.genre  = genre.genre_id
                            JOIN status ON filmlist.status = status.status_id
                            WHERE filmlist.name LIKE ? 
                            ''', (film_name, ))
    results = cur.fetchall()
    return results

def get_all_films(con):
    con.row_factory = sq.Row 
    cur = con.cursor()
    cur.execute('''
                        SELECT filmlist.name,   genre.name as genre_name,  status.name as status_name, rating, filmlist.description, filmlist.film_id FROM filmlist
                        JOIN genre ON filmlist.genre  = genre.genre_id
                        JOIN status ON filmlist.status = status.status_id
                        ORDER BY rating DESC''')
    results = cur.fetchall()
    return results

def delete_film(con, film_id):
    cur = con.cursor()
    cur.execute('''DELETE FROM filmlist where film_id = ?''', (film_id,))


