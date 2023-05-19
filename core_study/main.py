import pydantic
from fastapi import FastAPI
from pymongo import MongoClient
from bson.json_util import dumps, loads
from bson import ObjectId

# 몽고디비 설정
client = MongoClient("mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority")
club = client['core_data']['notice']

# 몽고db에서쓰는 objectId 타입을 파이썬에서 못 읽어서, string(문자)로 바꿔주는 기능
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

app = FastAPI()

@app.get("/")
async def home():
    return "hello"

@app.get("/api/post")
async def read_post():
    cursor = club.find()
    data = loads(dumps(cursor))

    return data

# Path 파라미터 ( 경로 매개변수로 받아오기 )
@app.get("/api/post/{title}")
async def read_one_post(title: str):
    cursor = club.find({"title":title})
    data = loads(dumps(cursor))

    return data

class Post(pydantic.BaseModel):
    title: str
    content: str
    count: int

@app.post("/api/post")
async def create_post(post: Post):
    post_dict = post.dict()
    club.insert_one({"title": post_dict["title"], "content": post_dict["content"], "count": post_dict["count"]})

@app.delete("/api/post/{objid}")
async def delete_post(objid: str):
    club.delete_one({'_id': ObjectId(objid)})
    return "delete success"

