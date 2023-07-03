from random import randrange
from re import I
from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#Using Pydantic to define a schema

#Allows us to enhance the Pydantic base model so that we can add our own paras to it
#Allows us to validate the type of data we are getting from the client
class Post(BaseModel):
    title: str
    content: str
    #Optional field for the user to enter if we wants the post to be published or not, default is true
    published: bool = True
    #A completely optional field, if user does not enter a value default is none
    rating: Optional[int] = None

#Create a array to store are posts which are in a dictionary format
my_posts = [{"title": "title of post 1", "content": "contents of post 1", "id": 1}, {"title": "favourite foods", "content": "i like pizza", "id": 2}]

#Very basic logic to find the post that we need my searching thorugh an array. Can be improved significantly by using binary search.
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
        
# Create a func to find a specific post and delete it
def find_index_post(id):
    for i,p in enumerate(my_posts):
        if p['id'] == id:
            return i

#path operation or route
#decorator - name of our FastAPI instance.(any http method)(path of the url)
@app.get("/")
def root():
    return {"message": "Hello World"}

#Get all posts
@app.get("/posts")
def get_posts():
    return {"data": my_posts}

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

#Create a post
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(posts: Post):
    post_dict = posts.dict()
    post_dict["id"] = randrange(0, 10000000)
    my_posts.append(post_dict)
    return {"data" : post_dict}

#Get an individual post
@app.get("/posts/{id}")
#FastAPi allows us to validate if the id entered is integer or not using ': int'
def get_post(id: int, response: Response):
    post = find_post(id)
    #Solving for giving the user an error code for feedback
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id: {id} was not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message': f"post with id: {id} was not found"}
    return {"post_detail": post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index in the array that has required ID
    # my_posts.pop(index)
    index = find_index_post(id)

    # Use to catch errors if no value is returned from find_index_post
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'post with id: {id} does not exist')

    my_posts.pop(index)
    # Cannot write a norrmal return because 204 expects that we will not give any sort of return so we use Response
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    index = find_index_post(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")
    
    post_dict = post.dict()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}