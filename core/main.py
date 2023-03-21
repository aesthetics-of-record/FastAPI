from fastapi import FastAPI
import pymongo
import certifi
from bson.json_util import dumps, loads
import pydantic
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']
post = db['post']

app = FastAPI()

@app.get("/")
async def home():
  return { "message" : "hello world !" }

@app.get("/api/post", description="글 가져오기")
async def read_post():
	data = post.find()
	data = loads(dumps(data))

	return data


class Post(BaseModel):
	title: str
	content: str
	author: str
	id: str
	image_url: str


@app.post("/api/post", description="글 쓰기")
async def create_post(post_data: Post):
	post_dict = post_data.dict()  # 받은 데이터를 dict로 변환

	# index 계산
	data = loads(dumps(post.find()))
	count = None
	if(len(data) == 0):
		count = 1
	else:
		count = int(data[-1]["index"]) + 1

	post.insert_one({"title": post_dict["title"], "content": post_dict["content"], "author": post_dict["author"], "id": post_dict["id"], "index": count, "image_url": post_dict["image_url"]})
	return "success"

@app.delete("/api/post/{index}", description="글 삭제하기 - ex) /api/post/2 (삭제할인덱스번호) 경로로 'delete' 요청")
async def delete_post(index: int):
	post.delete_one({"index": index})
	return "success"
