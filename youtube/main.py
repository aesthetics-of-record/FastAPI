from typing import Optional

from fastapi import FastAPI, Query
from enum import Enum

from pydantic import BaseModel

app = FastAPI()


@app.get("/", description="This is our firlst route")
async def base_get_route():
    return {"message": "hello world"}


@app.post("/")
async def post():
    return {"message": "hello from the post route"}


@app.put("/")
async def put():
    return {"message": "hello from the put route"}


@app.get("/users")
async def list_users():
    return {"message": "list users route"}


# path paramater


@app.get("/users/{user_id}")
async def get_user(user_id: str):
    return {"user_id": user_id}


@app.get("/users/me")
async def get_current_user():
    return {"message": "this is current user"}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food_name": food_name, "message": "you are healthy"}

    if food_name.value == 'fruits':
        return {"food_name": food_name, "message": "you are still healthy, but like sweet things"}

    return {"food_name": food_name, "message": "i like chocolate milk"}


fake_items_db = [{"item_name": "Foo"}, {
    "item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items")
# async def list_items(skip: int = 0, limit: int = 10):
#     return fake_items_db[skip: skip + limit]

# path paramater / query paramater
# Optional 을 3.10 버전 이후부터는 사용할 필요가 없다.
# @app.get("/items/{item_id}")
# async def get_item(item_id: str, q: Optional[str] = None):
# 	if q:
# 		return {"item_id": item_id, "q": q}
# 	return {"item_id": item_id}


# type conversion
# 1, yes, on ,true -> True
# 필수 파라미터를 지정하려면, path파라미터로 하는 게 일반적이나,
# 필수 파라미터로 필수 쿼리파라미터를 줄 수 있다.
@app.get("/items/{item_id}")
async def get_item(item_id: str, sample_query_param: str, q: Optional[str] = None, short: bool = False):
    item = {"item_id": item_id, "sample_query_param": sample_query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "Lorem ipsum dolor sit meat hello"})
    return item


@app.get("/users/{user_id}/items/{item_id}")
async def get_user_item(user_id: int, item_id: str, q: str = None, short: bool = False):
    item = {"user_id": user_id, "item_id": item_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "Lorem ipsum dolor sit meat hello"
            }
        )
    return item


################################################################
# Part 4. Request Body
################################################################

# pydantic - BaseModel
class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: int
    tax: Optional[float] = None


@app.post("/items")
async def create_item(item: Item):
    item_dict = item.dict()  # 받은 데이터를 dict로 변환
    if item.tax:
        price_with_tax = item.price + item.tax  # int + float = float변환
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict


# BaseModel + path
@app.put("/items/{item_id}")
async def create_item_with_put(item_id: int, item: Item, q: Optional[str] = None):
    result = {"item_id": item_id, **item.dict()}  # 스프레드 오퍼레이터 **
    if q:
        result.update({"q": q})
    return result


################################################################
# Part 5. Query Parameters and String Validation
################################################################

# query parameters
@app.get("/items")
async def read_items(q: Optional[str] = Query(None, min_length=3, max_length=10)):
    results = {"itmes": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# items/{item_id} 와 겹치지 않게 이름을 다르게 써 줬다.
# multiple values
@app.get("/multiitems")
async def read_items(q: list[str] = Query(["foo", "bar"])):
    results = {"itmes": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


@app.get("/items2")
async def read_items2(q: Optional[str] = Query(
        None,
        min_length=3,
        max_length=10,
        title="Sample query string",
        description="This is a sample query string",
        alias="item-query"  # 이렇게 쓰면 q대신 여기 문자로 쿼리네임이 바뀐다.
)):
    results = {"itmes": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results


# + 공식문서를 보니, regex 로 정규표현식을 쓸 수도 있다.

# 혹시나 def함수명과 파라미터 이름이 똑같지 않게 조심하자. 오류가 날 수도 있다.
# include_in_schema=False 이거를 써주면 docs 스케마가 안 나타난다.
async def hidden_query_route(hidden_query: Optional[str] = Query(None, include_in_schema=False)):
    if hidden_query:
        return {"hidden_query": hidden_query}
    return {"hidden_query": "Not found"}
