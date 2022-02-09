
import threading
import imp_functions
import psycopg2
import urllib.parse
import os
result = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))

conn = psycopg2.connect(
    host=result.hostname,
    database=result.path[1:],
    user=result.username,
    password=result.password
)
cursor = conn.cursor()


def db_insertion(tracks, typee):
    unique = imp_functions.random_string(5)
    cursor.execute(
        "INSERT INTO songs_name (folder,songs,web_type) VALUES (%s,%s,%s)", (unique, tracks, typee))
    conn.commit()
    cursor.execute(
        "SELECT id FROM songs_name WHERE folder = %s", (unique,))
    id = cursor.fetchone()[0]
    threading.Thread(target=imp_functions.create_directory,
                     args=([id])).start()
    threading.Thread(target=imp_functions.deleting,
                     args=([id-1])).start()
    return id, typee


def tracks_from_db(id):
    print(id)
    cursor.execute(
        "SELECT songs,web_type FROM songs_name WHERE id = %s", (id,))
    x = cursor.fetchone()
    if x[1] == 'youtube':
        return x[0][1:-1].split(',')
    return x[0][1:-1].split(',')


def song_name_retrevial(id, song_no):
    cursor.execute(
        "SELECT songs,web_type FROM songs_name WHERE id = %s", (id,))
    x = cursor.fetchone()
    if x[1] == 'youtube':
        return x[0][1:-1].split(',')[song_no-2]
    return x[0][1:-1].split(',')[song_no-2]
