"""
Declare Request Example Data
여러 방법이 존재한다.
"""

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()


################################################################
# pydantic의 Config와 schema_exrea를 활용하는 방법, pydentic은 다양한 스키마 커스터마이징도 지원한다.
# https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization
################################################################

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

    class Config:
        schema_extra = {
            "example": {
                "name": "Foo",
                "description": "A very nice Item",
                "price": 35.4,
                "tax": 3.2,
            }
        }


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item):
    results = {"item_id": item_id, "item": item}
    return results


################################
# 필드 내 추가 인자를 활용하는 방법 (example, examples 인자가 존재함)
"""
이 객체들에는 다 두 example, examples 인자가 있음
Path()
Query()
Header()
Cookie()
Body()
Form()
File()
"""
################################

class Item2(BaseModel):
    name: str = Field(example="Foo")
    description: str | None = Field(default=None, example="A very nice Item")
    price: float = Field(example=35.4)
    tax: float | None = Field(default=None, example=3.2)


@app.put("/items2/{item_id}")
async def update_item(item_id: int, item: Item2):
    results = {"item_id": item_id, "item": item}
    return results

###########
# Body()를 활용한 examples 인자 활용 예
###########

class Item3(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


@app.put("/items3/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Item3 = Body(
        examples={
            "normal": {
                "summary": "A normal example",
                "description": "A **normal** item works correctly.",
                "value": {
                    "name": "Foo",
                    "description": "A very nice Item",
                    "price": 35.4,
                    "tax": 3.2,
                },
            },
            "converted": {
                "summary": "An example with converted data",
                "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                "value": {
                    "name": "Bar",
                    "price": "35.4",
                },
            },
            "invalid": {
                "summary": "Invalid data is rejected with an error",
                "value": {
                    "name": "Baz",
                    "price": "thirty five point four",
                },
            },
        },
    ),
):
    results = {"item_id": item_id, "item": item}
    return results