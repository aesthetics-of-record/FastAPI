from fastapi import FastAPI
from pymongo import MongoClient
from pymongo.cursor import CursorType
from sse_starlette import EventSourceResponse

app = FastAPI()
client = MongoClient("mongodb+srv://apple825:aa04190825@cluster0.amq3ff3.mongodb.net/?retryWrites=true&w=majority")
db = client["test"]
collection = db["collection"]

@app.get("/stream")
async def stream():
    pipeline = [{"$match": {"operationType": "insert"}}]
    change_stream = collection.watch()

    # async def event_generator():
    #     async for change in change_stream:
    #         yield change

    async def event_generator():
        return change_stream

    for change in change_stream:
        print(change)

    return 1