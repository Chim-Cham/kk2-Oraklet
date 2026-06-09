from fastapi import FastAPI, UploadFile, File, HTTPException
import pandas as pd
from data import read_dataframe


app = FastAPI()
@app.post("/data/upload")
async def uploadData(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="Only CSV allowed")
    
    try:
        df = pd.read_csv(file.file)
        result = read_dataframe(df)
        return{
            "filename": file.filename,
            "data": result
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

@app.get("/data/stats")
async def  get_stats(dataset: str):
    filepath = f"uploads/{dataset}.csv"
    try:
        df = pd.read_csv(filepath)
        stats = df.describe(include="all").fillna("").to_dict()
        return {
            "dataset": dataset,
            "stats": stats
        }
    
    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Dataset could not be found, try uploading one before running this command"
        )
    
