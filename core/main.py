from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# 라우터
from routers import clubs, notices, promotions

app = FastAPI()

##########################################################
# origins에는 protocal, domain, port만 등록한다.
origins = [
	# "http://192.168.0.13:3000", # url을 등록해도 되고
	"*",  # private 영역에서 사용한다면 *로 모든 접근을 허용할 수 있다.
]

app.add_middleware(
	CORSMiddleware,
	allow_origins=origins,
	allow_credentials=True,  # cookie 포함 여부를 설정한다. 기본은 False
	allow_methods=["*"],  # 허용할 method를 설정할 수 있으며, 기본값은 'GET'이다.
	allow_headers=["*"],
	# 허용할 http header 목록을 설정할 수 있으며 Content-Type, Accept, Accept-Language, Content-Language은 항상 허용된다.
)
##########################################################



@app.get("/")
async def home():
	return {"message": "hello world !"}


# 라우터 사용
app.include_router(clubs.router)
app.include_router(notices.router)
app.include_router(promotions.router)


