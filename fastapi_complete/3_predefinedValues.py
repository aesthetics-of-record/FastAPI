from enum import Enum
from fastapi import FastAPI

app = FastAPI()


class BlogType(str, Enum):
    short = 'short'
    story = 'story'
    howto = 'howto'


@app.get('/blog/type/{type}')
def get_blog_type(type: BlogType):
    return {"message": f"Blog type {type}"}
