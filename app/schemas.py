from pydantic import BaseModel
from datetime import datetime

# # Using Pydantic to define a schema
# # Allows us to enhance the Pydantic base model so that we can add our own paras to it
# # Allows us to validate the type of data we are getting from the client
# class Post(BaseModel):
#     title: str
#     content: str
#     # Optional field for the user to enter if we wants the post to be published or not, default is true
#     published: bool = True

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True