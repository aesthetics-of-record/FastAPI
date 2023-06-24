################################################################
# Part 6: Path Parameters and Numeric Validation
################################################################
from fastapi import FastAPI, Query, Path
from typing import Optional

app = FastAPI()


@app.get("/items_validation/{item_id}")
async def read_items_validation(
		*,
		item_id: int = Path(..., title="The ID of the item to get", ge=10, le=100),  # 이상이하
		q: Optional[str] = Query(None, alias="item-query"),  # 옵셔널을 써도, ... 하면 required가 된다.
		size: float = Query(..., alias="item-size", gt=0, lt=7.75)  # 초과미만
):
	results = {"item_id": item_id, "size": size}
	if q:
		results.update({"q": q})
	return results

