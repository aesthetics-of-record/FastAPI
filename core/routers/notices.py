import pymongo
import certifi
from bson.json_util import dumps, loads
import pydantic
from bson import ObjectId
from pydantic import BaseModel
from fastapi import APIRouter

################################################################
pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']
notice = db['notice']
################################################################

router = APIRouter(
	tags=["notices"]
)

@router.get("/api/notices", description="공지사항 전체 가져오기")
async def read_all_notice():
	cursor = notice.find()
	data = loads(dumps(cursor))

	return data

class Notice(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	classification: int

@router.post("/api/notice", description="공지사항 추가하기")
async def create_notice(notice_data: Notice):
	notice_dict = notice_data.dict()

	notice.insert_one({"title": notice_dict["title"], "content": notice_dict["content"], "author": notice_dict["author"],
					 "user_id": notice_dict["user_id"],
					 "classification": notice_dict["classification"]})
	return "post success"

@router.delete("/api/notice/{objid}", description="공지사항 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_club(objid: str):
	notice.delete_one({"_id": ObjectId(objid)})
	return "delete success"