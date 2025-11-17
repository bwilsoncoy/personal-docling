from fastapi import FastAPI, UploadFile, File
from docling.document_converter import DocumentConverter
import tempfile
from pathlib import Path
import os

app = FastAPI(title="Docling Service")
converter = DocumentConverter()

@app.post("/parse")
async def parse_document(file: UploadFile = File(...)):
    input_bytes = await file.read()
    suffix = Path(file.filename).suffix or ""

    fd, tmp_path = tempfile.mkstemp(suffix=suffix)
    os.close(fd)

    try:
        with open(tmp_path, "wb") as f:
            f.write(input_bytes)

        result = converter.convert(tmp_path)
        doc = result.document
        return {
            "filename": file.filename,
            "markdown": doc.export_to_markdown(),
        }
    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)