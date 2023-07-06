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
from . import models, schemas
from .database import engine, get_db

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


# Get all posts
@app.get("/posts", response_model= List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    return posts

# @app.post("/createposts")
# #Allows me to define a var called payload. The body parameter takes the body text of the HTTP message and convert it as a dict.
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"posts": f"title: {payload['title']} | content: {payload['content']}"}

# @app.post("/posts")
# def create_posts(posts: Post):
#     print(posts)
#     #dict is a func that converts the pydantic model into a dictionary
#     print(posts.dict())
#     return {"data" : posts}

# Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    # # We use %s because it helps us avoid SQL injection
    # cursor.execute('''INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *''',
    #                (post.title, post.content, post.published))
    # # fetchone is used when we know there is only one post that is there and the db does not need to keep searching to find more
    # new_post = cursor.fetchone()
    # conn.commit()

    # Does the same thing as content = post.content, title = post.title
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    #retrieves the new post created and returns it back
    db.refresh(new_post)
    return new_post


# Get an individual post
@app.get("/posts/{id}", response_model= schemas.Post)
# FastAPi allows us to validate if the id entered is integer or not using ': int'
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    return post


# deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):

    # cursor.execute(
    #     """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post = db.query(models.Post).filter(models.Post.id == id)

    # Use to catch errors if no value is returned from find_index_post
    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id: {id} does not exist')
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


# updating a post
@app.put("/posts/{id}", response_model= schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
