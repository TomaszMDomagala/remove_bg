from fastapi import FastAPI, Request
from fastapi import File, UploadFile
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import uvicorn
from image_processing import remove_bg

root = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def main():
    return {"response": "Jello World"}

@app.get("/download/{item_id}")
async def download_file(item_id: str):
    file_name = f'converted/{item_id}.png'
    return FileResponse(file_name)

@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        contents = file.file.read()
        with open(f'uploaded/{file.filename}', 'wb') as f:
            f.write(contents)
        remove_bg(file.filename)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/items", response_class=HTMLResponse)
async def read_item(request: Request):
    list_files = [file.split('.')[0] for file in os.listdir('converted')]
    return templates.TemplateResponse("upload.html", {"request": request, "files": list_files})


if __name__ == '__main__':
    print("Server running...")
    uvicorn.run(app, host='127.0.0.1', port=8005)
