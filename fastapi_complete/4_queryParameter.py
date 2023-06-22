from fastapi import FastAPI
from typing import Optional

app = FastAPI()


@app.get('/blog/all')
def get_all_blogs(page=1, page_size: Optional[int] = None):
    return {'message': f'All {page_size} blogs on page {page}'}


# query and path
@app.get('/blog/{id}/comments/{comment_id}')
def get_comment(id: int, comment_id: int, valid: bool = True, username: Optional[str] = None):
    return {'message': f'blog_id {id}, comment_id {comment_id}, valid {valid}, username {username}'}
