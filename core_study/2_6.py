from fastapi import FastAPI, Path, Query, Body
from typing import Union, Annotated
from pydantic import BaseModel, Field, HttpUrl

app = FastAPI()

"""
Hello World! (기본 get 요청)
"""
@app.get("/")
def index():
	return { "message": "Hello World!"}


"""
Path Parameter
"""
@app.get("/api/path/{id}")
async def path(id: int):
	return { "message": f"아이디는 {id}"}

"""
Query Parameter + Type (Optional, Union 이 있는데, Union만 써도 다 된다.)
"""
@app.get("/api/query")
def query_and_type(q: int | None = None):
	return { "message": f"query 는 {q}"}

"""
Multiple Parameter, Numerric/Sting Validation
"""
# 참고로 Path 파라미터는 default값이 없습니다.
# default값 None, '...'
@app.get("/api/multiple/{id}")
def numeric(id: Annotated[Union[int, float], Path(ge=1, le=10)], q: str = Query(default=..., min_length=3, max_length=10)):
	return { "message": f"아이디 : {id} / 쿼리는 {q}"}


"""
Request Body ( Fields, Nested Models(Special types ) )
"""
# Nested Model 있다는 것 만 알아두세요. 외우려고 하지마세요.
class Image(BaseModel):
	url: HttpUrl # 이런형식의 특별한 타입모델도 있습니다.
	name: str

# Field 는 fastapi(Query, Path, Body)에서가 아니라 pydantic 에서 import 해야한다.
class Club(BaseModel):
	name: str
	description: str | None = Field(default=None, description="동아리 설명", regex="[a-zA-Z0-9]+@[a-zA-Z0-9]+")
	number_of_persons: int = Field(ge=1, le=100, description="동아리 회원 수")
	images: list[Image] | None = None


# get 요청은 body를 가질 수 없으니 주의
@app.post("/api/body")
def body(club: Annotated[Club, Body(example={
  "name": "string",
  "description": "safas12@dasf",
  "number_of_persons": 100,
  "images": [
    {
      "url": "http://127.0.0.1:8000/docs#/default/body_api_body_post",
      "name": "string"
    }
  ]
},
)
]
		 ):
	return club


