from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional, List
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .database import engine, get_db, SessionLocal, Base
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .routers import post,user, auth

models.Base.metadata.create_all(bind=engine) # to create all the models. This is what creates the table

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True

while True:    
    try:
        conn = psycopg2.connect(host = 'localhost', database = 'fastapi', user = 'postgres', password = '050567', cursor_factory = RealDictCursor)
        cursor = conn.cursor()
        print('Successfully connected to Database')
        break
    except Exception as error:
        print('Connection failed')
        print("error: ", error)
        time.sleep(2)





my_posts = [{"title":"post 1", "content": "content 1", "id": 1},{"title":"post 2","content": "content 2", "id" : 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p
        
def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

 
@app.get("/")
def root():
    return {"message": "welcome to my api"}







    






