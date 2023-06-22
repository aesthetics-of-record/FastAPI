from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get('/blog/all',
         tags=['blog'])
def get_all_blogs():
    return {"message": "All blogs provided"}


@app.get('/blog/{id}/comments/{comment_id}',
         tags=['blog', 'comment'])
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}
