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

	post.insert_one({"title": post_dict["title"], "content": post_dict["content"], "author": post_dict["author"],
					 "id": post_dict["id"], "image_url": post_dict["image_url"]})
	return "success"


@app.delete("/api/post/{objid}", description="글 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_post(objid: str):
	post.delete_one({"_id": ObjectId(objid)})
	return "success"
