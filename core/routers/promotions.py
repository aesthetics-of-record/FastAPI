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
promotion = db['promotion']
################################################################

router = APIRouter(
	tags=["promotions"]
)

@router.get("/api/promotions", description="홍보글 전체 가져오기")
async def read_all_promotion():
	cursor = promotion.find()
	data = loads(dumps(cursor))

	return data

class Promotion(BaseModel):
	title: str
	content: str
	author: str
	user_id: str
	image_url: str
	classification: int

@router.post("/api/promotion", description="홍보글 추가하기")
async def create_notice(notice_data: Promotion):
	promotion_dict = notice_data.dict()

	promotion.insert_one({"title": promotion_dict["title"], "content": promotion_dict["content"], "author": promotion_dict["author"],
					 "user_id": promotion_dict["user_id"], "image_url": promotion_dict["image_url"],
					 "classification": promotion_dict["classification"]})
	return "post success"

@router.delete("/api/promotion/{objid}", description="홍보글 삭제하기 - ex) /api/post/123412 (삭제할 objectid) 경로로 'delete' 요청")
async def delete_club(objid: str):
	promotion.delete_one({"_id": ObjectId(objid)})
	return "delete success"