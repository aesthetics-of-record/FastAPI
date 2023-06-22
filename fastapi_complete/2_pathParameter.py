from fastapi import FastAPI

app = FastAPI()

# 순서가 가장 중요하다. 만약 <이 함수를 밑에 쓴다면>,
# /blog/all 을 들어가도, /blog/{id}가 먼저 실행되기에 오류가 난다.
# 그래서 이 함수는 위에 써주거나 해야한다.
@app.get('/blog/all')
def get_all_blogs():
	return {"message": "All blogs provided"}


@app.get('/blog/{id}')
def get_blog(id: int):
	return {"message": f"Blog with id {id}"}



