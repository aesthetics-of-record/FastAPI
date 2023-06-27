from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

@app.get('/')
def index():
    return{"message": "hello world!"}

"""
Static File
"""
app.mount('/images', StaticFiles(directory='images'), name="images")
