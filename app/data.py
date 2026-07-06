from io import BytesIO
import pandas as pd
from fastapi import HTTPException

_upLoadedFile = None
_fileName = None

def upload_file(filename: str, data: bytes):
    global _upLoadedFile, _fileName

    _upLoadedFile = BytesIO(data)
    _fileName = filename

def get_dataframe() -> pd.DataFrame:
    if _upLoadedFile is None:
        raise HTTPException(
            status_code=404,
            detail="No dataset found!"
        )

    _upLoadedFile.seek(0)

    return pd.read_csv(_upLoadedFile)

def get_filename() -> str:
    return _fileName

def data_stats():
    df = get_dataframe()
    return df.describe(include="all").fillna("").to_dict()

def data_stats_text():
    df = get_dataframe()
    return {
        "Rows": len(df),
        "Columns": list(df.columns),
        "Numeric": df.describe().round(2).to_dict(),
    }

def dataset_context(df):
    return f"""
    Dataset Information

    Rows: {len(df)}

    Columns:
    {", ".join(df.columns)}
    
    Datset:
    {df.describe(include="all").fillna("").to_dict()}
    """

def max_row(df):
    result = []
    for col in df.select_dtypes(include="number").columns:
        value = df[col].max()
        result.append(f"{col}: {value}")
    return "\n".join(result)

def min_row(df):
    result = []
    for col in df.select_dtypes(include="number").columns:
        value = df[col].min()
        result.append(f"{col}: {value}")
    return "\n".join(result)

def average_row(df):
    result = []
    for col in df.select_dtypes(include="number").columns:
        value = df[col].mean()
        result.append(f"{col}: {value}")
    return "\n".join(result)