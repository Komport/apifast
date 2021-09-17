from fastapi import FastAPI 
from typing import  Optional
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def index():
    return {"data":{"name":"Yusif"}}

@app.get('/blogs/{id}')
def get_blog(id: int,limit):
    return {"data":{"_id":id,"limit":limit}}

@app.get('/blogs/comments/{id}')
def get_comments(id: int = 10, limit: Optional[str]=None):
    return {"data":{"_id":id,"limit":limit}}


class Blog(BaseModel):
    title: str
    blog_content: str
    blog_author: str


@app.post('/newblog')
def new_blog(blog: Blog):
    return blog