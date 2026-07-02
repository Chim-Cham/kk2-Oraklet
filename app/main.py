from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from .data import upload_file, get_dataframe, get_filename, data_stats, data_stats_text
from .config import settings
from app.chain.pipeline import chain
from .schemas import QuestionRequest, QuestionResponse, DatasetQuestion

app = FastAPI()

@app.post("/data/upload")
async def upload_Data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    
    upload_file(
        file.filename,
        await file.read()
    )

    return {
        "filename": get_filename()
    }


@app.get("/data/stats")
async def get_Stats():
    return {
        "dataset": get_filename(),
        "stats": data_stats()
    }


@app.get("/health")
async def health_Check():
    return {"status": "Running"}


@app.get("/URL_info")
async def get_URL():
    return {
        settings.url,
        settings.api_key
    }
    

@app.post("/ai/ask")
async def ask_AI(question: QuestionRequest):
    data = DatasetQuestion(
        df=get_dataframe(),
        question=question.question
    )

    return chain.invoke(data)
    