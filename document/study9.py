"""
응답 상태 코드
"""

"""
응답 모델과 같은 방법으로, 
어떤 경로 작동이든 status_code 매개변수를 사용하여 응답에 대한 HTTP 상태 코드를 선언할 수 있습니다.
"""

from fastapi import FastAPI, status

app = FastAPI()


@app.post("/items/", status_code=201)
async def create_item(name: str):
    return {"name": name}

@app.post("/items2/", status_code=status.HTTP_201_CREATED)
async def create_item(name: str):
    return {"name": name}