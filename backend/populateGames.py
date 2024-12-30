import sqlite3 

conn = sqlite3.connect('games.db')
cursor = conn.cursor()

games = [
    ('The Legend of Zelda: Breath of the Wild', 'Adventure', '2017-03-03', 'Nintendo Switch', 'An open-world adventure game.'),
    ('God of War', 'Action', '2018-04-20', 'PlayStation 4', 'A father-son epic journey in Norse mythology.'),
    ('Among Us', 'Party', '2018-06-15', 'PC, Mobile', 'A multiplayer social deduction game.'),
]

cursor.executemany('''
INSERT INTO games (name, genre, release_date, platform, description) 
VALUES (?, ?, ?, ?, ?)
''', games)

conn.commit()
conn.close()