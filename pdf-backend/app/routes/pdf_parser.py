from fastapi import APIRouter, UploadFile, File
from app.services.parser import extract_entities

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    print(content)
    entities = extract_entities(content)
    return {"entities": entities}
