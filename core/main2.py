from enum import Enum

from fastapi import FastAPI
import pymongo
import certifi
from bson.json_util import dumps, loads
import pydantic
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
##########################################################
# origins에는 protocal, domain, port만 등록한다.
origins = [
	# "http://192.168.0.13:3000", # url을 등록해도 되고
	"*"  # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,  # cookie 포함 여부를 설정한다. 기본은 False
	allow_methods=["*"],  # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
	allow_headers=["*"],
	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)
##########################################################

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']
post = db['post']


@app.get("/")
async def home():
	return {"message": "hello world !"}


@app.get("/api/posts", description="글 전체 가져오기")
async def read_all_post():
	cursor = post.find()
	data = loads(dumps(cursor))

	return data

@app.get("/api/post/{objid}", description="오브젝트아이디에 맞는 글 1개만 가져오기")
async def read_one_post(objid: str):
	cursor = post.find({"_id": ObjectId(objid)})
	data = loads(dumps(cursor))

	return data

@app.get("/api/posts/", description="글 skip, limit를 통한 글 일부 가져오기\nex) 3번째글부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_post(skip: int, limit: int):
	cursor = post.find()
	document = cursor.skip(skip).limit(limit)
	data = loads(dumps(document))

	return data

# 검색 기능
@app.get("/api/posts/search/", description="검색어 쿼리로 넘기기")
async def search_post(query: str):
	condition = [
  {
    '$search': {
      'index': "postSearch",
      'text': {
        'query': query,
        'path': ['title', 'content', 'tag1', 'tag2', 'tag3']
      }
    }
  },
		{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	cursor = post.aggregate(condition)
	data = loads(dumps(cursor))

	return data

class Post(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	image_url: str
	tag1: str
	tag2: str
	tag3: str
	classification: int


@app.post("/api/post", description="글 쓰기 / classification = 0 -> 중앙동아리, 1 -> 직무동아리")
async def create_post(post_data: Post):
	post_dict = post_data.dict()  # 받은 데이터를 dict로 변환

	post.insert_one({"title": post_dict["title"], "content": post_dict["content"], "author": post_dict["author"],
					 "user_id": post_dict["user_id"], "image_url": post_dict["image_url"],
					 "tag1": post_dict["tag1"], "tag2": post_dict["tag2"], "tag3": post_dict["tag3"], "classification": post_dict["classification"]})
	return "post success"


@app.delete("/api/post/{objid}", description="글 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_post(objid: str):
	post.delete_one({"_id": ObjectId(objid)})
	return "delete success"
