"""
헤더 매개변수
"""

# 헤더 매개변수를 Query, Path 그리고 Cookie 매개변수들과 같은 방식으로 정의할 수 있습니다.

from fastapi import FastAPI, Header

app = FastAPI()

# 헤더명 적을 때 첫글자 대문자로 안 적고, 소문자로 적어도된다.
# 그리고 하이픈 '-' 를 표현하고 싶으면, 대신 _언더스코어를 통해 표현하면 된다.
# convert_underscores의 기본값은 True로 안 적어줘도 된다.
# 정 하이픈을 써서 표현하고싶으면, alias 인자를 이용하자.
@app.get("/items/")
async def read_items(user_agent: str | None = Header(default=None), host: str | None = Header(default=None),
					 accept_language : str | None = Header(default=None, convert_underscores=True)):
    return {"User-Agent": user_agent, "host": host, "accept_language": accept_language}