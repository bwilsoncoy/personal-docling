from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Header
from fastapi.responses import PlainTextResponse
from docling.document_converter import DocumentConverter
import tempfile
import shutil

API_KEY = "QZMFa8KqGQgU!!ydwkA@U3dqCMbxPJz9"

app = FastAPI(title="Docling Service")

def get_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return x_api_key

converter = DocumentConverter()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/parse", dependencies=[Depends(get_api_key)], response_class=PlainTextResponse)
async def parse(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        shutil.copyfileobj(file.file, tmp)
        tmp_path = tmp.name
    try:
        doc = converter.convert(tmp_path)
        md = doc.render_as_markdown()
        return md
    finally:
        file.file.close()