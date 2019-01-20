import sqlite3


conn = sqlite3.connect("anime.db")
cur = conn.cursor()

cur.execute('''
    CREATE TABLE IF NOT EXISTS Anime (title TEXT, latest_ep TEXT, latest_ep_link TEXT)
    ''')

cur.execute('''SELECT latest_ep FROM Anime WHERE title=?''', ("The Promised Neverland",))
animes = cur.fetchone()

print(animes)