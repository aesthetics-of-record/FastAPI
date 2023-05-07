"""
Body - Fields
"""

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()

# 이렇게 필드를 통해 객체 속성 하나하나에도 추가 validation을 넣을 수 있다.
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="The description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The price must be greater than zero")
    tax: float | None = None


@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item = Body(embed=True)):
    results = {"item_id": item_id, "item": item}
    return results