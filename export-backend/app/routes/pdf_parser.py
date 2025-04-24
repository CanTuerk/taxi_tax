import io
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from app.services.parser import extract_entities
from app.services.csv_parser import process_bolt_data
import pandas as pd

router = APIRouter()


@router.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    content = await file.read()
    print(content)
    entities = extract_entities(content)
    return {"entities": entities}


@router.post("/upload/bolt")
async def upload_csv(file: UploadFile = File(...)):
    print(file)
    if file.content_type != "text/csv":
        return JSONResponse(
            content={"error": "Please upload a CSV file."}, status_code=400
        )

    content = await file.read()
    try:
        df = pd.read_csv(io.StringIO(content.decode("utf-8")))
        processed_df = process_bolt_data(df)
        print(processed_df)
        # Just an example: return first 5 rows as JSON
        return processed_df.head().to_dict(orient="records")
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
