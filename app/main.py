from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from io import BytesIO
from .config import settings
""" from data import read_dataframe """

upLoadedFile = None
fileName = None

app = FastAPI()
@app.post("/data/upload")
async def uploadData(file: UploadFile = File(...)):
    global upLoadedFile, fileName
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    
    try:
        result = await file.read()
        upLoadedFile = BytesIO(result)
        fileName = file.filename
        return{
            "filename": fileName,
            "data": upLoadedFile
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/data/stats")
async def  getStats():
    global upLoadedFile, fileName
    try:
        df = pd.read_csv(upLoadedFile)
        stats = df.describe(include="all").fillna("").to_dict()
        return {
            "dataset": fileName,
            "stats": stats
        }
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Dataset could not be found, try uploading one before running this command"
        )
    
@app.get("/health")
async def healthCheck():
    return {
        "status": "Running"
    }

@app.get("/URL_info")
async def getURL():
    return {
        settings.url,
        settings.api_key
    }
    
    
    