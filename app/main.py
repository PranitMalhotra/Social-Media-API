from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routers import user, post, auth, vote
from .config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
app.include_router(vote.router)