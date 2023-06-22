from fastapi import FastAPI

app = FastAPI()

@app.get('/hello')
def index():
	return {"message": 'Hello world!'}

@app.post('/hello')
def index2():
	return 'Hi'

