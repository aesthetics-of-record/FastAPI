from enum import Enum
import pymongo
import certifi
from bson.json_util import dumps, loads
import pydantic
from bson import ObjectId
from typing import Optional
from pydantic import BaseModel
from fastapi import APIRouter

router = APIRouter(
	tags=["clubs"]
)

################################################################
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']
club = db['club']
################################################################


@router.get("/api/clubs", description="동아리 전체 가져오기")
async def read_all_club():
	cursor = club.find()
	data = loads(dumps(cursor))

	return data


@router.get("/api/club/{objid}", description="오브젝트아이디에 맞는 동아리 1개만 가져오기")
async def read_one_club(objid: str):
	cursor = club.find({"_id": ObjectId(objid)})
	data = loads(dumps(cursor))

	return data

@router.get("/api/clubs/", description="동아리 skip, limit를 통한 동아리 일부 가져오기\nex) 3번째부터 4개 가져오려면, -> skip=2, limit=4")
async def read_some_club(skip: int, limit: int):
	cursor = club.find()
	document = cursor.skip(skip).limit(limit)
	data = loads(dumps(document))

	return data

@router.get("/api/clubs/classification/", description="동아리 skip, limit를 통한 글 일부 가져오기\n그리고 classification을 통한 중앙 동아리 직무 동아리 구분 가능")
async def read_some_club(skip: int, limit: int, classification: int):
	cursor = club.find({"classification": classification})
	document = cursor.skip(skip).limit(limit)
	data = loads(dumps(document))

	return data


# 검색 기능
@router.get("/api/clubs/search/", description="검색어 쿼리로 넘기기")
async def search_club(query: str):
	condition = [
  {
    '$search': {
      'index': "clubSearch",
      'text': {
        'query': query,
        'path': ['title', 'content', 'tag1', 'tag2', 'tag3']
      }
    }
  },
		{ '$addFields': { 'score' : { '$meta': 'searchScore'}}}
]

	cursor = club.aggregate(condition)
	data = loads(dumps(cursor))

	return data

class Club(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	image_url: str
	tag1: str
	tag2: str
	tag3: str
	classification: int


@router.post("/api/club", description="동아리 추가하기 / classification = 0 -> 중앙동아리, 1 -> 직무동아리")
async def create_club(club_data: Club):
	club_dict = club_data.dict()  # 받은 데이터를 dict로 변환

	club.insert_one({"title": club_dict["title"], "content": club_dict["content"], "author": club_dict["author"],
					 "user_id": club_dict["user_id"], "image_url": club_dict["image_url"],
					 "tag1": club_dict["tag1"], "tag2": club_dict["tag2"], "tag3": club_dict["tag3"], "classification": club_dict["classification"]})
	return "post success"


@router.delete("/api/club/{objid}", description="동아리 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_club(objid: str):
	club.delete_one({"_id": ObjectId(objid)})
	return "delete success"