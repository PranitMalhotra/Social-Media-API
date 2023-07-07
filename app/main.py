from typing_extensions import deprecated
from multiprocessing import synchronize
from random import randrange
from re import I
from typing import Optional, List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import user, post, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# try helps to connect with the database incase the connection falls off
# cursor_factory is used to get the name od the colms bcuz by default colm number in returned.
while True:
    try:
        conn = psycopg2.connect(host='127.0.0.1', database='social_media_api',
                                user='postgres', password='Pranit1234', cursor_factory=RealDictCursor)
        # cursor is the one that actually executes the code
        cursor = conn.cursor()
        print("Database connection was successful")
        break

    # we are storing the error in the error var
    except Exception as error:
        print("Connection to database failed")
        print("Error: ", error)
        time.sleep(2)

# # Create a array to store are posts which are in a dictionary format
# my_posts = [{"title": "title of post 1", "content": "contents of post 1", "id": 1}, {
#     "title": "favourite foods", "content": "i like pizza", "id": 2}]

# # Very basic logic to find the post that we need my searching thorugh an array. Can be improved significantly by using binary search.
# def find_post(id):
#     for p in my_posts:
#         if p["id"] == id:
#             return p

# # Create a func to find a specific post and delete it
# def find_index_post(id):
#     for i, p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# # path operation or route
# # decorator - name of our FastAPI instance.(any http method)(path of the url)
# @app.get("/")
# def root():
#     return {"message": "Hello World"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
