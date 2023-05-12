import pydantic # 데이터 타입을 다루는 파이썬 모듈
from bson import ObjectId # 몽고db의 ObjectID를 다루기 위한 모듈
from fastapi import FastAPI
import pymongo
from bson.json_util import dumps, loads

app = FastAPI()

client = pymongo.MongoClient("mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority")
post = client['core_data']['post']

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

@app.get('/api/posts')
async def read_posts():
    cursor = post.find()
    data = loads(dumps(cursor))

    return data

@app.post('/api/post')
async def create_post():
    post.insert_one({'title': '현호', 'content': '밥'})

    return "create success"
