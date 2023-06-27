from fastapi import FastAPI, File, UploadFile
import shutil
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# @app.post('/file')
# def get_file(file: bytes = File(...)):
#   content = file.decode('utf-8')
#   lines = content.split('\n')
#   return {'lines': lines}


@app.post('/uploadfile')
def get_uploadfile(upload_file: UploadFile = File(...)):
  path = f"files/{upload_file.filename}"
  with open(path, 'w+b') as buffer:
    shutil.copyfileobj(upload_file.file, buffer)

  return {
    'filename': path,
    'type': upload_file.content_type
  }

@app.get('/download/{name}', response_class=FileResponse)
def get_file(name: str):
  path = f'files/{name}'
  return path


"""
Static File
"""
# @app.mount('/files', StaticFiles('/files'), name="files")
