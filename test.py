import certifi
import pydantic
from bson import ObjectId
from bson.json_util import dumps, loads

from fastapi import FastAPI
import pymongo

app = FastAPI()

# mongodb 보안에러 해결을 위한 패키지
ca = certifi.where()

client = pymongo.MongoClient(
	"mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority", tlsCAFile=ca)

pydantic.json.ENCODERS_BY_TYPE[ObjectId] = str

post = client['core_data']['post']

@app.get('/')
def get_data():
    data = post.find()
    data = loads(dumps(data))
    print(data)

    return data

