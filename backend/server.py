from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import dbInit
import uvicorn
import hashlib
import os

app = FastAPI()

# This middleware is required in order to accept requests from other domains such as a React app
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def dbConnect():
    return sqlite3.connect('games.db')
@app.get("/") 
def getRoot():
    return {"message": "Welcome to the game search API"}

@app.get("/games")
def getGames():
    conn = dbConnect()
    cursor = conn.cursor()
    try: 
        cursor.execute("SELECT * FROM GAMES")
        rows = cursor.fetchall()
        conn.close()
        return [{
            "id": row[0],
            "name": row[1],
            "genre": row[2],
            "release_date": row[3],
            "platform": row[4],
            "description": row[5],
        }
        for row in rows]
    except Exception as e:
        conn.close()
        raise HTTPException(status_code = 500, detail = str(e))
    
@app.post("/register")
async def register(request:Request):
    conn = dbConnect()
    cursor = conn.cursor()
    data = await request.json()
    username = data.get(username)
    password = data.get(password)
    try: 
        salt = generate_salt()
        hashed_password = encrypt(password, salt)
        cursor.execute( "INSERT INTO AccountsDB(username, hashed_password, salt) VALUES ('"+username+"', '"+hashed_password+"', '"+salt+"');")
        conn.close()

    except Exception as e:
        conn.close()
        raise HTTPException(status_code = 500, detail = str(e))

def generate_salt():
    return os.urandom(16).hex()

def encrypt(password, salt):
    salted_password = password + salt
    hash_object = hashlib.sha256()
    hash_object.update(salted_password.encode())

    return hash_object.hexdigest()


    
if __name__ == "__main__":
    conn = dbConnect()  # Make sure to create a connection before using it
    if dbInit.dbExists(): 
        uvicorn.run("server:app", host="localhost", port=8000)
        dbInit.dbClose(conn)
    else:
        print("Run accountsinit and dbinit first.")
