import sqlite3
import os

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

def dbExists():
    """
    function that checks to see if the television.db file exists in the current working directory
    :return:
    """
    path=os.getcwd()
    if "games.db" in os.listdir():
        return True
    return False

def dbClose(conn):
    try:
        conn.commit()
        conn.close()
    except Exception as e:
        print(e)

cursor.execute (''' CREATE TABLE IF NOT EXISTS games (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                genre TEXT NOT NULL,
                release_date DATE,
                platform TEXT,
                description TEXT
                )''')

cursor.execute(''' CREATE TABLE IF NOT EXISTS users (
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               username TEXT NOT NULL UNIQUE,
               salt TEXT NOT NULL,
               hashed_password TEXT NOT NULL
               )''')

cursor.execute ('''CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    game_id INTEGER NOT NULL,
    review TEXT,
    rating INTEGER CHECK(rating BETWEEN 1 AND 5),
    FOREIGN KEY(user_id) REFERENCES users(id),
    FOREIGN KEY(game_id) REFERENCES games(id)
)
''')

conn.commit()
conn.close()