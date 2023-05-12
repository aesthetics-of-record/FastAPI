# 패키지
# fastapi - 서버
# pymongo - 몽고디비
# uvicorn - 서버 실행기
import certifi # 인증서
import pydantic
from bson import ObjectId # 몽고디에서만 있는 이진 데이터 타입
from fastapi import FastAPI
import pymongo
from bson.json_util import dumps, loads
from fastapi.encoders import jsonable_encoder

app = FastAPI()


pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

db = client['core_data']
post = db['post']


@app.get("/")
async def read_post():
    data = post.find()
    data = loads(dumps(data))
    # print(type(data))

    return data


# 몽고디비 로그인 하면 클라우드 공간을 줍니다.
#