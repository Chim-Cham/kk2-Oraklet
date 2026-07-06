from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from .data import upload_file, get_dataframe, get_filename, data_stats
from .config import settings
from .chain.pipeline import chain
from .schemas import QuestionRequest, DatasetQuestion

app = FastAPI()

@app.post("/data/upload")
async def upload_Data(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    contents = await file.read()    
    try:
        pd.read_csv(BytesIO(contents))
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Invalid CSV file."
        )
    
    MAX_SIZE = 1024 * 1024 # 1 MB
    if len(contents) > MAX_SIZE:
        raise HTTPException(
            status_code=413,
            detail="File too large"
        )
    
    
    upload_file(
        file.filename,
        contents
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
    

@app.post("/ai/ask")
async def ask_AI(question: QuestionRequest):
    data = DatasetQuestion(
        df=get_dataframe(),
        question=question.question
    )

    return chain.invoke(data)
    