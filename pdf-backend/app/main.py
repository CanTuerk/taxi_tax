from fastapi import FastAPI
from app.routes import pdf_parser

app = FastAPI()

app.include_router(pdf_parser.router)