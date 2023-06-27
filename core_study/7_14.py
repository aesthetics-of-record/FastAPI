from fastapi import FastAPI, Cookie, status, Header
from enum import Enum
from typing import Annotated, Union
from fastapi.responses import Response, HTMLResponse

app = FastAPI()

"""
Enum
"""
class Club(Enum):
	중앙동아리 = "중앙동아리"
	직무동아리 = "직무동아리"

@app.get("/api/enum")
def get_enum(club: Club):
	return club


"""
Cookie
"""
# Cookie 에 직접 ads_id와 값을 넣어주고, 보내면 여기서 쿠키값을 받을 수 있다.
@app.get("/api/cookie")
def cookie(cookie_id: Annotated[Union[str, None], Cookie()] = None):
    return {"cookie_id": cookie_id}


"""
Response Cookie ( Response - 직접 응답 객체를 조정가능함. 즉 response 를 커스터마이징 가능 ) ( 이런식으로 response 를 추가 가능 )
"""
@app.get("/api/response/cookie")
def response(response: Response):
	response.set_cookie(key="cookie_id", value="hello~ test cookie")
	return {"massage": "get cookie"}

"""
Header
"""
@app.get("/header")
async def get_header(user_agent: str | None = Header(default=None),
                     host: Annotated[str | None, Header()] = None,
                     accept_encoding = Header(default=None)
                     ):
    return {"User-Agent": user_agent, "Host": host, "Accept-Encoding": accept_encoding }

"""
Response Header
"""
@app.get("/headers-and-object/")
def get_headers(response: Response):
    response.headers["X-Cat-Dog"] = "alone in the world"
    # 이런식으로 헤더에 추가 정보를 딸려 보낼 수 있다.
    return {"message": "헤더 추가/변경"}

"""
Status Code (status_code 파라미터 부터 시작 => response를 통한 status_code 조정까지 )
"""
@app.get('/post/{id}', status_code=status.HTTP_200_OK)
def get_posts(id: int, response: Response):
    if id > 5:
        response.status_code = status.HTTP_404_NOT_FOUND
        return {'error': f'Post {id} not found'}
    else:
        response.status_code = status.HTTP_200_OK
        return {'message': f'Post with id {id}'}



"""
Custom Response (헤더, 쿠키, 응답타입(기본JSON, xml, html, files 등) 표준응답이 아닌 것을 추가할 수 있다.) 
"""
products = ['시계', '책', '치킨']

@app.get('/all')
def get_all_products():
	# return products
	data = ", ".join(products)
	return Response(content=data, media_type="text/plain")

@app.get('/html/{id}')
def get_html_id(id: int):
    out = f"""
    <head>
      <style>
      .box {{
        width: 500px;
        height: 30px;
        border: 2px inset green;
        background-color: lightblue;
        text-align: center;
      }}
      </style>
    </head>
    <div class="box">{id}</div>
    """
    return Response(content=out, media_type="text/html") # 이런식으로 media_type를 바꿔줘도 되고, HTMLResponse를 활용해도 된다.
