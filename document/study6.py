"""
Cookie Parameters
"""

from fastapi import Cookie, FastAPI

app = FastAPI()

# Cookie 에 직접 ads_id와 값을 넣어주고, 보내면 여기서 쿠키값을 받을 수 있다.
@app.get("/items/")
async def read_items(ads_id: str | None = Cookie(default=None)):
    return {"ads_id": ads_id}